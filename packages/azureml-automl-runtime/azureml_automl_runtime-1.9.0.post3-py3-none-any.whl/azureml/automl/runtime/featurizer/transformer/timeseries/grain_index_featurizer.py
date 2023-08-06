# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Featurize the grain columns."""
import pandas as pd

from typing import Dict
from warnings import warn

from azureml.automl.core.shared.forecasting_exception import (NotTimeSeriesDataFrameException,
                                                              ForecastingTransformException)
from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from azureml.automl.core.shared.time_series_data_frame import TimeSeriesDataFrame
from .forecasting_base_estimator import AzureMLForecastTransformerBase


class GrainIndexFeaturizer(AzureMLForecastTransformerBase):
    """Transform that adds grain related features to a TimeSeriesDataFrame.

    By default, the transforms adds a new categorical
    column for each level in the time series grain index.
    """

    def __init__(self, grain_feature_prefix='grain',
                 prefix_sep='_',
                 overwrite_columns=False,
                 ts_frequency=None):
        """
        Construct a GrainIndexFeaturizer.

        :param grain_feature_prefix:
            Prefix to apply to names of columns created for grain features.
            Defaults to `grain`
        :type grain_feature_prefix: str

        :param prefix_sep:
            Separator to use in new grain/horizon column names between
            the prefix and the name of the relevant index level.
            Defaults to `_`.
            Ex: If the grain index has levels `store` and `brand`,
            the new grain features will be named `grain_store` and
            `grain_brand` by default.
        :type prefix_sep: str

        :param overwrite_columns:
            Flag that permits the transform to overwrite existing columns in the
            input TimeSeriesDataFrame for features that are already present in it.
            If True, prints a warning and overwrites columns.
            If False, throws a ClientException.
            Defaults to False to protect user data.
        :type overwrite_columns: boolean

        :param ts_frequency:
            The frequency of the time series that this transform will be applied to.
            This parameter is used to construct the horizon feature.
            If ts_frequency=None, the fit method will attempt to infer the frequency
            from the input TimeSeriesDataFrame.
        :type ts_frequency: str (pandas offset alias), pd.DateOffset
        """
        super().__init__()
        self.grain_feature_prefix = grain_feature_prefix
        self.prefix_sep = prefix_sep
        self.overwrite_columns = overwrite_columns
        self.ts_frequency = ts_frequency

    def _check_input(self, X):
        if not isinstance(X, TimeSeriesDataFrame):
            raise NotTimeSeriesDataFrameException(
                'GrainIndexFeaturizer: X must be a TimeSeriesDataFrame', has_pii=False,
                reference_code='grain_index_featurizer.GrainIndexFeaturizer._check_input')

    def preview_grain_feature_names(self, X):
        """
        Get the grain features names produced by the transform.

        :param X: Input data
        :type X: TimeSeriesDataFrame

        :return: grain feature names
        :rtype: list of strings
        """
        if X.grain_colnames is None:
            return []
        grain_cols = X.grain_index.names
        feat_names = [self.grain_feature_prefix +
                      self.prefix_sep + idx
                      for idx in grain_cols]

        return feat_names

    @function_debug_log_wrapped('info')
    def fit(self, X, y=None):
        """
        Fit the grain featurizer.

        :param X: Input data
        :type X: TimeSeriesDataFrame

        :param y:
            Ignored. Included for pipeline compatibility

        :return: self
        :rtype: GrainIndexFeaturizer
        """
        self._check_input(X)

        if self.ts_frequency is None:
            self.ts_frequency = X.infer_freq()

        return self

    @function_debug_log_wrapped('info')
    def transform(self, X):
        """
        Transform the input data.

        :param X: Input data
        :type X: TimeSeriesDataFrame

        :return: Transformed data
        :rtype:TimeSeriesDataFrame
        """
        self._check_input(X)

        new_columns = {}    # type: Dict[str, pd.Categorical]
        if X.grain_colnames is not None:
            grain_names = self.preview_grain_feature_names(X)
            grain_cols = X.grain_index.names
            new_columns = {nm:
                           pd.Categorical(X.index.get_level_values(idx))
                           for nm, idx in zip(grain_names, grain_cols)}

        if len(new_columns) == 0:
            warn('No grain is set and horizon features were not created; ' +
                 'data will be unchanged', UserWarning)
        # Check for existing columns of the same names
        overlap = set(new_columns).intersection(set(X.columns))
        if len(overlap) > 0:
            message = ('Some of the existing columns in X will be ' +
                       'overwritten by the transform.')
            # if told to overwrite - warn
            if self.overwrite_columns:
                warn(message, UserWarning)
            else:
                # if not told to overwrite - raise exception
                error_message = message + ("Set 'overwrite_columns' to True " +
                                           'to overwrite columns in X.')
                raise ForecastingTransformException(
                    error_message,
                    target='GrainIndexFeaturizer',
                    has_pii=False,
                    reference_code='grain_index_featurizer.GrainIndexFeaturizer.transform')

        return X.assign(**new_columns)
