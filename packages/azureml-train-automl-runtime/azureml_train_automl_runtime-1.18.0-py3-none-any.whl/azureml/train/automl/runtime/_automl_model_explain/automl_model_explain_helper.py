# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Optional, Tuple
import logging
import time

from sklearn.model_selection import train_test_split
from nimbusml import DprepDataStream

from azureml._common._error_definition import AzureMLError
from azureml._restclient.constants import RunStatus
from azureml.automl.core.shared._diagnostics.automl_error_definitions import ExplainabilityPackageMissing
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.runtime import data_cleaning
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.automl.runtime.shared.streaming_dataset import StreamingDataset
from azureml.automl.runtime.shared.types import DataInputType, DataSingleColumnInputType
from azureml.automl.runtime.training_utilities import _upgrade_sparse_matrix_type, _is_sparse_matrix_int_type
from azureml.automl.runtime.training_utilities import LargeDatasetLimit
from azureml.train.automl.exceptions import ConfigException
from azureml.train.automl.runtime.automl_explain_utilities import MaximumEvaluationSamples, NumberofBestRunRetries
from azureml.train.automl.runtime.run import AutoMLRun


logger = logging.getLogger(__name__)


def _automl_auto_mode_get_explainer_data(
        dataset: DatasetBase) -> Tuple[DataInputType, DataInputType,
                                       DataSingleColumnInputType,
                                       DataSingleColumnInputType]:
    """Get X, X_valid, y, y_valid data to explain from the DatasetBase object."""
    X = dataset.get_X()
    X_valid = dataset.get_X_valid()
    y = dataset.get_y()
    y_valid = dataset.get_y_valid()
    if _is_sparse_matrix_int_type(X):
        logger.info("Integer type detected for X, need to upgrade to float type")
    if _is_sparse_matrix_int_type(X_valid):
        logger.info("Integer type detected for X_valid, need to upgrade to float type")
    # If the training data is in integer format, then the data needs to reformatted into float data
    # for LightGBM surrogate model. For different types of workloads, following needs to done:-
    # 1. If this is non-preprocessing/non-timeseries experiment then copy needs to be made via this
    #    conversion.
    # 2. If this is preprocessing/timeseries, then we should read from file cache and update the type
    #    in inplace. Currently we can't. TODO: Once the training data is read from the cache, then update
    #    the code below to change the type inplace.
    explainer_data_X = _upgrade_sparse_matrix_type(X)
    explainer_data_X_valid = _upgrade_sparse_matrix_type(X_valid)
    explainer_data_y = y
    explainer_data_y_valid = y_valid
    return explainer_data_X, explainer_data_X_valid, explainer_data_y, explainer_data_y_valid


def _automl_auto_mode_get_raw_data(
    dataset: DatasetBase
) -> Tuple[DataInputType, DataInputType, DataSingleColumnInputType, DataSingleColumnInputType]:
    """Get X, X_valid, y, y_valid raw data to upload with explanations from the DatasetBase object."""
    X_raw = dataset.get_X_raw()
    X_valid_raw = dataset.get_X_valid_raw()
    y_raw = dataset.get_y_raw()
    y_valid_raw = dataset.get_y_valid_raw()

    X_raw, y_raw, _ = data_cleaning._remove_nan_rows_in_X_y(X_raw, y_raw, logger=logger)
    X_valid_raw, y_valid_raw, _ = data_cleaning._remove_nan_rows_in_X_y(X_valid_raw, y_valid_raw, logger=logger)

    return X_raw, X_valid_raw, y_raw, y_valid_raw


def _automl_auto_mode_get_explainer_data_streaming(
        dataset: StreamingDataset) -> Tuple[DataInputType,
                                            DataInputType,
                                            DataSingleColumnInputType,
                                            DataSingleColumnInputType]:
    """Get X, X_valid, y, y_valid data to explain from the StreamingDataset object."""
    X = dataset.get_X()
    X_valid = dataset.get_X_valid()
    y = dataset.get_y()
    y_valid = dataset.get_y_valid()

    # Obtain a subsample of the data to pass to Azure explainability library
    # (since the library requires all data to fit in memory).
    # TODO: Right now, for classification datasets, subsampling might leave out some
    # classes. One possible fix is to subsample the data stratified by label column
    X = X.take(LargeDatasetLimit.MAX_ROWS_TO_SUBSAMPLE)
    X_valid = X_valid.take(LargeDatasetLimit.MAX_ROWS_TO_SUBSAMPLE)
    preprocessor = dataset.get_preprocessor()
    if preprocessor is None:
        explainer_data_X = X.to_pandas_dataframe(extended_types=False)
        explainer_data_X_valid = X_valid.to_pandas_dataframe(extended_types=False)
    else:
        logger.debug("Transforming subsampled raw X for streaming explainability")
        explainer_data_X = preprocessor.transform(DprepDataStream(X), as_csr=True)
        logger.debug("Transforming subsampled raw X_valid for streaming explainability")
        explainer_data_X_valid = preprocessor.transform(DprepDataStream(X_valid), as_csr=True)
    explainer_data_y = y.take(LargeDatasetLimit.MAX_ROWS_TO_SUBSAMPLE).to_pandas_dataframe(
        extended_types=False).values
    explainer_data_y_valid = y_valid.take(LargeDatasetLimit.MAX_ROWS_TO_SUBSAMPLE).to_pandas_dataframe(
        extended_types=False).values
    return explainer_data_X, explainer_data_X_valid, explainer_data_y, explainer_data_y_valid


def _automl_auto_mode_get_raw_data_streaming(
        dataset: StreamingDataset) -> Tuple[DataInputType,
                                            DataInputType,
                                            DataSingleColumnInputType,
                                            DataSingleColumnInputType]:
    """Get X, X_valid, y, y_valid raw data to upload with explanations from the StreamingDataset object."""
    X_raw = dataset.get_X_raw().take(LargeDatasetLimit.MAX_ROWS_TO_SUBSAMPLE).to_pandas_dataframe(
        extended_types=False)
    X_valid_raw = dataset.get_X_valid_raw().take(LargeDatasetLimit.MAX_ROWS_TO_SUBSAMPLE).to_pandas_dataframe(
        extended_types=False)
    y_raw = dataset.get_y_raw().take(LargeDatasetLimit.MAX_ROWS_TO_SUBSAMPLE).to_pandas_dataframe(
        extended_types=False).values
    y_valid_raw = dataset.get_y_valid_raw().take(LargeDatasetLimit.MAX_ROWS_TO_SUBSAMPLE).to_pandas_dataframe(
        extended_types=False).values
    return X_raw, X_valid_raw, y_raw, y_valid_raw


def _automl_pick_evaluation_samples_explanations(featurized_X_data: DataInputType,
                                                 y: DataSingleColumnInputType,
                                                 featurized_X_valid_data: Optional[DataInputType] = None,
                                                 y_valid: Optional[DataSingleColumnInputType] = None,
                                                 is_classification: Optional[bool] = False) -> DataInputType:
    """
    Pick subsamples of featurized data if the number of rows in featurized data is large.

    :param featurized_X_data: The featurized version of training data.
    :type featurized_X_data: DataInputType
    :param y: Training target column.
    :type y: DataSingleColumnInputType
    :param featurized_X_valid_data: The featurized version of validation data.
    :type featurized_X_valid_data: DataInputType
    :param y_valid: Validation target column.
    :type y_valid: DataSingleColumnInputType
    :param is_classification: Bool to capture if this split is needed for classification or otherwise.
    :type is_classification: bool
    :return: Sub-sample of featurized train/validation data
    """
    if featurized_X_valid_data is None:
        featurized_X = featurized_X_data
        target = y
    else:
        featurized_X = featurized_X_valid_data
        target = y_valid

    if featurized_X.shape[0] > MaximumEvaluationSamples:
        sample_fraction = 1.0 * MaximumEvaluationSamples / featurized_X.shape[0]
        stratify_target = target if is_classification else None
        try:
            featurized_X_sampled, _, target_sampled, _ = train_test_split(
                featurized_X, target, train_size=sample_fraction, random_state=None,
                stratify=stratify_target)
            logger.info("Successfully down sampled the evaluation samples using stratified split")
        except ValueError:
            # in case stratification fails, fall back to non-stratify train/test split
            featurized_X_sampled, _, target_sampled, _ = train_test_split(
                featurized_X, target, train_size=sample_fraction, random_state=None, stratify=None)
            logger.info("Successfully down sampled the evaluation samples using random split")
    else:
        featurized_X_sampled = featurized_X

    return featurized_X_sampled


def _check_model_explain_packages() -> None:
    """Check if model explain packages are importable."""
    try:
        from interpret_community.mimic.models.lightgbm_model import LGBMExplainableModel
        from interpret_community.mimic.models.linear_model import LinearExplainableModel
        from interpret_community.common.constants import MimicSerializationConstants, ResetIndex
        from azureml.interpret.mimic_wrapper import MimicWrapper
        logger.info("All dependent explainability packages are importable")
    except ImportError as e:
        logger.warning("Package {0} not importable".format(str(e.name)))
        raise ConfigException._with_error(AzureMLError.create(
            ExplainabilityPackageMissing, target="explain_model", missing_packages=e.name,
            reference_code=ReferenceCodes._MODEL_EXPLAIN_MISSING_DEPENDENCY_EXCEPTION),
            inner_exception=e
        ) from e


def _should_query_for_best_run(parent_run: AutoMLRun) -> bool:
    """
    Check if we can query the run history to find the best run.

    :param parent_run: The automated ML parent run.
    :type parent_run: azureml.train.automl.run.AutoMLRun
    :return: bool
    """
    number_of_child_runs_in_artifacts = len(parent_run.get_metrics(recursive=True))
    number_of_complete_child_runs = 0
    children = parent_run.get_children(_rehydrate_runs=False)
    for child in children:
        if child._run_dto['status'] == RunStatus.COMPLETED:
            number_of_complete_child_runs += 1

    number_of_retries = 0
    time_to_wait = 10
    back_off_factor = 2
    while number_of_retries < NumberofBestRunRetries and \
            number_of_complete_child_runs > number_of_child_runs_in_artifacts:
        logger.info('The number of completed child runs {0} is greater than child runs in artifacts {1}'.format(
            number_of_complete_child_runs, number_of_child_runs_in_artifacts))
        time.sleep(time_to_wait)
        time_to_wait *= back_off_factor
        number_of_child_runs_in_artifacts = len(parent_run.get_metrics(recursive=True))
        number_of_retries += 1

    if number_of_retries >= NumberofBestRunRetries:
        return False
    return True
