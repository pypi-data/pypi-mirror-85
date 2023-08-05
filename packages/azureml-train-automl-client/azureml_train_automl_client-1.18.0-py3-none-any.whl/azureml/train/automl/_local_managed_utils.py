# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods used in local managed submission for automated ML in Azure Machine Learning."""
import logging
import os
import pickle as pkl
import shutil
import subprocess
import time
from typing import Any, Dict, List, Optional, Tuple

from azureml.automl.core._run import run_lifecycle_utilities

from . import constants
from .exceptions import ClientException

from azureml._common._error_definition import AzureMLError
from azureml._restclient.constants import RunStatus
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    AutoMLInternal,
    InvalidInputDatatype,
    ManagedLocalScriptError,
    ManagedLocalUserError)
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared.constants import TelemetryConstants
from azureml.train.automl import _azureautomlclient, _logging
from azureml.train.automl._environment_utilities import modify_run_configuration
from azureml.train.automl.constants import _DataArgNames, SupportedInputDatatypes
from azureml.core import Dataset, Environment, Run
from azureml.core.workspace import Workspace
from azureml.data.abstract_dataset import AbstractDataset
from azureml.automl.core.shared.exceptions import UserException, ValidationException
from azureml.automl.core.shared.pickler import DefaultPickler


logger = logging.getLogger(__name__)


def get_data_args(workspace: Workspace, fit_params: Dict[str, Any], local_path: str) -> \
        Tuple[Dict[str, Any], List[str]]:
    """
    Extract data parameters, pickle them, and get args to pass to local managed script.
    This will either be Dataset IDs, or paths to pickle objects.
    """
    fit_params, data_dict = _extract_data(fit_params)
    dataset_args = handle_data(data_dict, local_path)

    return fit_params, dataset_args


def _save_inmem(path: str, name: str, data: Any) -> str:
    file_name = name + ".pkl"
    file_path = os.path.join(path, file_name)
    pickler = DefaultPickler()
    pickler.dump(data, file_path)
    return file_name


def _compose_args(dataset_args: List[Any], name: str, data_type: str, value: Optional[Any]) -> List[str]:
    arg = "--{}"
    arg_type = "--{}-dtype"

    if value is not None:
        dataset_args.append(arg.format(name))
        dataset_args.append(value)
        dataset_args.append(arg_type.format(name))
        dataset_args.append(data_type)

    return dataset_args


def _extract_data(fit_params: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Remove data params from fit params."""
    data_dict = {_DataArgNames.X: fit_params.pop(_DataArgNames.X, None),
                 _DataArgNames.y: fit_params.pop(_DataArgNames.y, None),
                 _DataArgNames.sample_weight: fit_params.pop(_DataArgNames.sample_weight, None),
                 _DataArgNames.X_valid: fit_params.pop(_DataArgNames.X_valid, None),
                 _DataArgNames.y_valid: fit_params.pop(_DataArgNames.y_valid, None),
                 _DataArgNames.sample_weight_valid: fit_params.pop(_DataArgNames.sample_weight_valid, None),
                 _DataArgNames.training_data: fit_params.pop(_DataArgNames.training_data, None),
                 _DataArgNames.validation_data: fit_params.pop(_DataArgNames.validation_data, None)}
    return fit_params, data_dict


def handle_data(data_dict: Dict[str, Any],
                local_path: str) -> List[str]:
    """
    Register datasets and create script arguments to pass to the child job.

    :param data_dict: Dictionary of names of data inputs and corresponding data.
    :param local_path: The path to save pickled data to.
    :return: List of arguments to pass to a ScriptRun with locations/ids of all data needed.
    """
    dataset_args = []  # type: List[str]
    has_pandas = False
    has_numpy = False
    try:
        import pandas as pd
        has_pandas = True
    except ImportError:
        pass
    try:
        import numpy as np
        has_numpy = True
    except ImportError:
        pass
    logger.info("Pandas present: {}. Numpy present: {}".format(has_pandas, has_numpy))
    for data_name, data_value in data_dict.items():
        if isinstance(data_value, AbstractDataset):
            logger.info("Saving Dataset for script run submission.")
            # ScriptRunConfig will translate the DatasetConsumptionConfig into a dataset id
            dataset_args = _compose_args(dataset_args,
                                         data_name,
                                         "dataset",
                                         data_value.as_named_input(data_name))
        elif has_pandas and isinstance(data_value, pd.DataFrame):
            logger.info("Saving Pandas for script run submission.")
            dataset_args = _compose_args(dataset_args,
                                         data_name,
                                         "pandas",
                                         _save_inmem(local_path, data_name, data_value))
        elif has_numpy and isinstance(data_value, np.ndarray):
            logger.info("Saving Numpy for script run submission.")
            dataset_args = _compose_args(dataset_args,
                                         data_name,
                                         "numpy",
                                         _save_inmem(local_path, data_name, data_value))
        elif data_value is not None:
            raise ValidationException._with_error(
                AzureMLError.create(
                    InvalidInputDatatype, target=data_name, input_type=type(data_value),
                    supported_types=", ".join(SupportedInputDatatypes.ALL)
                )
            )

    return dataset_args


def modify_managed_run_config(run_config, parent_run, experiment, settings_obj):
    _logging.set_run_custom_dimensions(
        automl_settings=settings_obj,
        parent_run_id=parent_run.id,
        child_run_id=None)
    properties = parent_run.get_properties()
    env_name = properties.get("environment_cpu_name")
    env_version = properties.get("environment_cpu_version")
    if env_version == "":
        env_version = None
    logger.info("Running local managed run on curated environment: {} version: {}".format(env_name, env_version))

    if env_name is None or env_name is "":
        run_config.environment.python.user_managed_dependencies = False
        run_config = modify_run_configuration(settings_obj, run_config, logger)
    else:
        run_config.environment = Environment.get(experiment.workspace, env_name, env_version)

    return run_config


def prepare_managed_inputs(experiment, local_path, settings_obj, fit_params, run_config):
    package_dir = os.path.dirname(os.path.abspath(__file__))

    script_path = os.path.join(package_dir, constants.LOCAL_SCRIPT_NAME)
    shutil.copy(script_path, os.path.join(local_path, constants.LOCAL_SCRIPT_NAME))

    automl_estimator = _azureautomlclient.AzureAutoMLClient(experiment, settings_obj)

    parent_run = automl_estimator._create_parent_run_for_local_managed()

    logger.info("Pickling data and settings for local managed.")

    settings = settings_obj.as_serializable_dict()

    settings[constants.MANAGED_RUN_ID_PARAM] = parent_run.id
    fit_params['run_configuration'] = None
    fit_params, dataset_args = get_data_args(experiment.workspace, fit_params, local_path)

    run_config = modify_managed_run_config(run_config, parent_run, experiment, settings_obj)
    with open(os.path.join(local_path, constants.AUTOML_SETTINGS_PATH), 'wb') as fp:
        pkl.dump(settings, fp)
    with open(os.path.join(local_path, constants.AUTOML_FIT_PARAMS_PATH), 'wb') as fp:
        pkl.dump(fit_params, fp)

    return parent_run, dataset_args, settings, run_config


def handle_script_run_error(parent_run: Run, script_run: Optional[Run]) -> None:
    bad_states = [RunStatus.FAILED, RunStatus.CANCELED]
    terminal_states = bad_states + [RunStatus.COMPLETED]
    is_running = parent_run is not None and parent_run.get_status() not in terminal_states

    if script_run is None:
        ex_wrapped = ClientException._with_error(
            AzureMLError.create(
                AutoMLInternal,
                error_details="Local managed failed before submission.",
            )
        )
        if is_running and parent_run is not None:
            run_lifecycle_utilities.fail_run(parent_run, ex_wrapped, is_aml_compute=False)
        raise ex_wrapped

    # Wait for the script_run to propagate all of the errors
    with logging_utilities.log_activity(
            logger,
            activity_name=TelemetryConstants.ScriptRunFinalizing,
            custom_dimensions={'run_id': parent_run.id, "script_run_id": script_run.id}):
        while script_run.get_status() == "Finalizing":
            time.sleep(5)

    failed = script_run.get_status() in bad_states

    error = script_run.get_details().get('error')

    if failed and error is not None:
        if 'User program failed with' in error["error"].get('message'):
            ex_wrapped = ClientException._with_error(
                AzureMLError.create(
                    ManagedLocalScriptError,
                    error_type=error["error"].get('debugInfo', {}).get('type')
                )
            )
            if is_running and parent_run is not None:
                run_lifecycle_utilities.fail_run(parent_run, ex_wrapped, is_aml_compute=False)
            raise ex_wrapped
        else:
            # let the script_run error handling take over as we know this issue wasn't caused by us.
            error_type = error["error"].get('debugInfo', {}).get('type')
            if error_type is None:
                error_type = error["error"].get("code")
            user_exception = UserException._with_error(
                AzureMLError.create(
                    ManagedLocalUserError,
                    error_type=error_type
                )
            )
            if is_running and parent_run is not None:
                run_lifecycle_utilities.fail_run(parent_run, user_exception, is_aml_compute=False)
            script_run.wait_for_completion()


def _get_dataset(workspace: Workspace, dataset_id: str) -> Optional[AbstractDataset]:
    try:
        logger.info("Fetching dataset {}.".format(dataset_id))
        return Dataset.get_by_id(workspace=workspace, id=dataset_id)
    except Exception:
        logger.info("Failed to fetch dataset {}.".format(dataset_id))
        return None


def _get_inmem(file_path):
    logger.info("Fetching in memory data.")
    pickler = DefaultPickler()
    return pickler.load(file_path)


def get_data(workspace: Workspace, location: str, dtype: str) -> Any:
    if dtype == "numpy" or dtype == "pandas":
        return _get_inmem(location)
    else:
        return _get_dataset(workspace, location)


def is_docker_installed() -> bool:
    try:
        version = subprocess.check_output(["docker", "--version"]).decode('utf8')
        logger.info("Docker is installed with {}.".format(version))
    except Exception:
        logger.info("Docker is not installed.")
        return False
    return True
