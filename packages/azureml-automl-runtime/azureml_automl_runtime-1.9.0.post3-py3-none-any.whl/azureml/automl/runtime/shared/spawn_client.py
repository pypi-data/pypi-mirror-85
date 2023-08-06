# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Functionality to execute a function in a child process created using "spawn".

This file contains the client portion.
"""
from typing import Any, Callable, cast, Dict, Optional, Tuple, Union
from pathlib import Path
import dill
import logging
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile

from . import subprocess_utilities
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared import log_server
from azureml.automl.core.shared.exceptions import AutoMLException, MemorylimitException, PipelineRunException
from azureml.automl.core.shared.limit_function_call_exceptions import CpuTimeoutException, SubprocessException
from azureml.automl.core.shared.fake_traceback import FakeTraceback
from .types import T


logger = logging.getLogger(__name__)


def touch_file(base_path: str, filename: str) -> str:
    """
    Given the base path and the file name, touch the file.

    :param base_path: directory containing the file
    :param filename: the name of the file
    :return: the path to the file
    """
    path = Path(base_path).joinpath(filename)
    path.touch()
    return os.path.join(base_path, filename)


def run_in_proc(working_dir: Optional[str],
                timeout: Optional[int],
                f: 'Callable[..., Tuple[T, Optional[BaseException]]]',
                args: Any, **kwargs: Any) -> T:
    """
    Invoke f with the given arguments in a new process. f must return a (result, error) tuple.

    :param working_dir: the working directory to use
    :param timeout: optional amount of time after which the process will be killed
    :param f: the function to run
    :param args: the positional arguments for the function
    :param kwargs: the keyword arguments for the function
    :return: the result from the (result, error) tuple returned by the function if successful
    """

    process = None
    # Create a folder for temporary files, used to communicate across
    # processes and to persist stdout/stderr.
    with tempfile.TemporaryDirectory(dir=working_dir) as tempdir:
        try:
            # Create all files used for data exchange across client and server.
            config_file_name = touch_file(tempdir, 'config')
            input_file_name = touch_file(tempdir, 'input')
            output_file_name = touch_file(tempdir, 'output')
            stdout_file_name = touch_file(tempdir, 'stdout')
            stderr_file_name = touch_file(tempdir, 'stderr')

            # Create a configuration object to pass to the target process. This
            # configuration is applied prior to deserialization of the input,
            # thus it can influence the environment code gets loaded in.
            config = {
                'path': sys.path,
                'log_verbosity': logging.getLogger().getEffectiveLevel()
            }

            # Use dill to store configuration information needed to set up
            # the target process.
            with open(config_file_name, 'wb') as file:
                dill.dump(config, file, protocol=dill.HIGHEST_PROTOCOL)

            # Use dill to store the function and arguments to run in the target
            # process.
            with open(input_file_name, 'wb') as file:
                dill.dump((f, args, kwargs), file, protocol=dill.HIGHEST_PROTOCOL)

            # Locate the Python executable, working directory, our sibling
            # spawn_server, and the environment variables.
            python_executable = sys.executable
            curdir = os.path.dirname(__file__)
            srv_script_file = os.path.join(curdir, "spawn_server.py")

            env = os.environ.copy()
            env[log_server.HOST_ENV_NAME] = log_server.server_host
            env[log_server.PORT_ENV_NAME] = str(log_server.server_port)

            # Open files to redirect stdout and stderr to.
            with open(stdout_file_name, 'w') as stdout, open(stderr_file_name, 'w') as stderr:
                # Spawn child process and wait for completion.
                cmd = [
                    python_executable,
                    srv_script_file,
                    config_file_name,
                    input_file_name,
                    output_file_name]

                process = subprocess.Popen(cmd, cwd=working_dir, env=env, stdout=stdout, stderr=stderr)
                try:
                    process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    # Attempt to kill the process and its children, and report
                    # the exception.
                    subprocess_utilities.kill_process_tree(process.pid)
                    raise

            check_process_success(process, stderr_file_name)

            # Read the output and use dill to deserialize the result into a
            # (value, error) pair.
            with open(output_file_name, 'rb') as output_file:
                val, err, tb = cast(Tuple[T, Optional[BaseException], Optional[Dict[str, Any]]],
                                    dill.load(output_file))
            if err is not None:
                # We MUST log the traceback here, because it is not possible to reraise with this fake traceback
                # without additional interpreter hacks involving manually constructing similar stack frames.
                # See python-tblib source code for an example of this hackery in action.
                # However, this will result in duplicate logging of child process errors.

                # For safety reasons, run this in a try-except to avoid weird edge cases that might have been missed.
                try:
                    logging_utilities.log_traceback(err, logger, tb=FakeTraceback.deserialize(tb))
                except Exception as e:
                    logging_utilities.log_traceback(e, logger)

                if isinstance(err, AutoMLException):
                    # If it's one of ours, throw it as is
                    raise err
                # We don't have the original traceback for the exception, so wrap it in one of ours and mark as PII.
                raise PipelineRunException\
                    .from_exception(err,
                                    'Pipeline execution failed with {}: {}'.format(err.__class__.__name__, str(err)),
                                    'spawn_client',
                                    has_pii=True)\
                    .with_generic_msg('Pipeline execution failed with {}'.format(err.__class__.__name__))

            return val

        finally:
            if process is not None:
                for i in range(5):
                    try:
                        # poll() returns None if the process is still running (no returncode)
                        if process.poll() is None:
                            subprocess_utilities.kill_process_tree(process.pid)
                        break
                    except Exception:
                        pass


def check_linux_oom_killed(pid: int) -> None:
    """
    Check to see if the Linux out of memory killer sent SIGKILL to this process. Raise an exception if killed by OOM.

    :param pid: process pid
    :return: None
    """
    oom_killed = False
    mem_usage = 0
    try:
        out = subprocess.run(['dmesg', '-l', 'err'],
                             stdout=subprocess.PIPE, universal_newlines=True)
        log_lines = out.stdout.strip().lower().split('\n')
        for line in log_lines:
            if 'out of memory: kill process {}'.format(pid) in line:
                oom_killed = True
            else:
                match = re.search(r'killed process {} .+? anon-rss:(\d+)kb'.format(pid), line)
                if match is not None:
                    mem_usage = int(match.group(1)) * 1024
    except Exception:
        pass

    if oom_killed:
        raise MemorylimitException.create_without_pii(str(mem_usage))


def check_process_success(process: 'subprocess.Popen[bytes]', stderr_file_name: str) -> None:
    """
    Check to see if this process exited successfully. In case of a positive non-zero exit code, stderr is logged.

    :param process: the process object from subprocess.Popen
    :param stderr_file_name: the path to the file containing stderr
    :return:
    """
    returncode = process.returncode

    if returncode < 0:
        # Note: negative return codes only occur on POSIX platforms and are caused by unhandled signals
        errorcode = -returncode
        errorname = signal.Signals(errorcode).name

        if sys.platform == 'linux' and errorcode == signal.SIGKILL:
            # On Linux, the kernel memory allocator overcommits memory by default. If we attempt to
            # actually use all that memory, then the OOM killer will kick in and send SIGKILL. We
            # have to check the kernel logs to see if this is the case.
            check_linux_oom_killed(process.pid)

        if errorname in ['SIGKILL', 'SIGABRT']:
            raise MemorylimitException.create_without_pii(
                'Subprocess (pid {}) killed by unhandled signal {} ({}). This is most likely due to an out of memory '
                'condition; please retry after increasing available memory.'.format(
                    process.pid, errorcode, errorname))

        raise SubprocessException.create_without_pii(
            'Subprocess (pid {}) killed by unhandled signal {} ({}).'.format(
                process.pid, errorcode, errorname))
    elif returncode > 0:
        if sys.platform == 'win32':
            # ntstatus.h STATUS_QUOTA_EXCEEDED
            if returncode == 0xc0000044:
                raise CpuTimeoutException()

        # Ideally we would like to capture stderr here since it will have the real exception
        # when the returncode is 1, but it might have PII.
        with open(stderr_file_name, 'r') as stderr:
            message = 'Subprocess (pid {}) exited with non-zero exit status {}.'.format(process.pid, returncode)
            message_with_stderr = '{} stderr output: \n{}'.format(message, '\n'.join(stderr.readlines()))
            raise SubprocessException(message_with_stderr).with_generic_msg(message)
