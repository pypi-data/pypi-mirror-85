"""Log training metrics to MLFlow

An experiment is composed of multiple training runs typically run with different hyperparameters. There is no clear line between when you would decide to stop an experiment and start a new one. An instance of the experiment class is passed to the Trainer which then uses it to log the metrics. In order to use this logger, user must install mlflow and start the mlflow UI.
"""

import logging
import os
from contextlib import contextmanager
from typing import Any, Dict, Generator, Optional

import mlflow
import mlflow.pytorch
import torch

from ..ml_logger import MLExperiment, MLRun

logger = logging.getLogger(__name__)


class MLFlowMLRun(MLRun):
    def __init__(self, name: str, mlflow_run: mlflow.ActiveRun) -> None:
        super().__init__(name)
        self._run: mlflow.ActiveRun = mlflow_run
        self._last_step = 0

    def log_summary(self, hparams: Dict[str, Any], metrics: Dict[str, float]) -> None:
        mlflow.log_params(hparams)
        for metric_name, metric_val in metrics.items():
            self.log_metric(self._last_step + 1, metric_name, metric_val)

    def log_metric(self, step: int, name: str, val: float) -> None:
        mlflow.log_metric(name, val, step)
        self._last_step = step

    def log_params(self, step: int, state: Dict[str, torch.Tensor]) -> None:
        logger.warning("MLFlow does not support logging parameters.")

    def log_model(self, step, model) -> None:
        mlflow.pytorch.log_model(model, "model")
        self._last_step = step

    def log_tick(self, step: int) -> None:
        pass


class MLFlowMLExperiment(MLExperiment):
    def __init__(self, name: str, dirpath: Optional[str] = None) -> None:
        super().__init__(name)
        if dirpath:
            mlflow.set_tracking_uri(os.path.expanduser(dirpath))
        mlflow.set_experiment(name)

    @contextmanager
    def start_run(self, name: str) -> Generator[MLRun, None, None]:
        with mlflow.start_run(run_name=name) as mlflow_run:
            run = MLFlowMLRun(name, mlflow_run)
            yield run
