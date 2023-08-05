"""Log training metrics to a CSV file

An experiment is composed of multiple training runs typically run with different hyperparameters. There is no clear line between when you would decide to stop an experiment and start a new one. An instance of the experiment class is passed to the Trainer which then uses it to log the metrics.
"""
import json
import logging
import os
import os.path as path
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, Generator

import numpy as np
import torch

from ..ml_logger import MLExperiment, MLRun
from .stdout_logger import StdoutMLRun

logger: logging.Logger = logging.getLogger(__name__)


class CsvMLRun(MLRun):
    """Concrete implementation of the abstract MLRun class

    This class does not need to be instantiated directly. It is instantiated by the experiment class as needed. This class will write the metrics of each run in a different CSV file.
    """

    def __init__(self, name: str, exproot: str) -> None:
        super().__init__(name)
        runroot = path.join(exproot, name.strip().lower())
        if path.exists(runroot):
            raise RuntimeError(f"{runroot} already exists! Choose a different run name.")
        os.mkdir(runroot)

        self._models_root: str = path.join(runroot, "models")
        os.mkdir(self._models_root)
        self._model_loc_file = open(path.join(runroot, "models_loc.csv"), "wt")
        print("timestamp,step,model_path", file=self._model_loc_file)

        self._summary_filename: str = path.join(runroot, "summary.json")

        self._metricsfile = open(path.join(runroot, "metrics.csv"), "wt")
        print("timestamp,step,name,value", file=self._metricsfile)

        # timestamp,step,param_name,bin_0_lower,bin_0_upper,bin_0_mid,bin_0_freq,bin_1_lower,bin_1_upper,...
        self._paramsfile = open(path.join(runroot, "params_hist.csv"), "wt")
        header = ["timestamp", "step", "param_name"]
        for i in range(10):
            header += [f"bin_{i}_lower", f"bin_{i}_upper", f"bin_{i}_mid", f"bin_{i}_count"]
        print(",".join(header), file=self._paramsfile)

    def log_summary(self, hparams: Dict[str, Any], metrics: Dict[str, float]) -> None:
        if path.exists(self._summary_filename):
            raise RuntimeError(f"{self._summary_filename} was already written once!")
        summary = {"hyperparams": hparams, "evaluation_metrics": metrics}
        try:
            with open(self._summary_filename, "wt") as f:
                json.dump(summary, f)
        except Exception as e:
            logger.error("Unable to write summary!", exc_info=e)

    def log_metric(self, step: int, name: str, val: float) -> None:
        print(f"{datetime.now()},{step},{name},{val:.6f}", file=self._metricsfile)

    def log_tick(self, step: int) -> None:
        print(f"{datetime.now()},{step},tick,0", file=self._metricsfile)

    def log_params(self, step: int, state: Dict[str, torch.Tensor]) -> None:
        ts = datetime.now()
        for param_name, params in state.items():
            params = torch.flatten(params).cpu()
            hist, bin_edges = np.histogram(params)
            record = f"{ts},{step},{param_name}"
            for i, freq in enumerate(hist):
                bin_mid = (bin_edges[i] + bin_edges[i + 1]) / 2
                record += f",{bin_edges[i]},{bin_edges[i+1]},{bin_mid},{freq}"
            print(record, file=self._paramsfile)

    def log_model(self, step: int, model: torch.nn.Module) -> None:
        model_filename = f"model-{step}.pkl"
        model_path = path.join(self._models_root, model_filename)
        print(f"{datetime.now()},{step},{model_filename}", file=self._model_loc_file)
        torch.save(model, model_path)

    def close(self) -> None:
        self._metricsfile.close()
        self._paramsfile.close()
        self._model_loc_file.close()


class CsvStdoutMLRun(MLRun):
    """Concrete implementation of the abstract MLRun class

    This class does not need to be instantiated directly. It is instantiated by the experiment class as needed. This class will write the metrics of each run in a different CSV file. Additionally it will also output the metrics to stdout.
    """

    def __init__(self, name: str, exproot: str) -> None:
        super().__init__(name)
        self._csv_run = CsvMLRun(name, exproot)
        self._stdout_run = StdoutMLRun(name)

    def log_summary(self, hparams: Dict[str, Any], metrics: Dict[str, float]) -> None:
        self._csv_run.log_summary(hparams, metrics)
        self._stdout_run.log_summary(hparams, metrics)

    def log_metric(self, step: int, name: str, val: float) -> None:
        self._csv_run.log_metric(step, name, val)
        self._stdout_run.log_metric(step, name, val)

    def log_tick(self, step: int) -> None:
        self._csv_run.log_tick(step)
        self._stdout_run.log_tick(step)

    def log_params(self, step: int, state: Dict[str, torch.Tensor]) -> None:
        self._csv_run.log_params(step, state)
        self._stdout_run.log_params(step, state)

    def log_model(self, step: int, model: torch.nn.Module) -> None:
        # No need to save the model twice. Just use one of the runs for this.
        print(f"\nStep {step}: Checkpointing model")
        self._csv_run.log_model(step, model)

    def close(self) -> None:
        self._csv_run.close()


class CsvMLExperiment(MLExperiment):
    """Concrete implementation of the MLExperiment abstract base class

    It is expected that the user will instantiate this class directly and pass it to the Trainer. This class will log the metrics to the following CSV files all rooted at the user provided {dirpath}/{experiment_name}/{run_name}

      * models/model-{step}.pkl
      * models_loc.csv
      * summary.json
      * metrics.csv
      * param_hist.csv
    Where {step} is the step number provided each time a metric is logged. Typically this lines up with the epoch if metrics are being logged at each epoch.

    models/model-{step}.pkl: This is the serialized model which can be deserialized just like any other PyTorch model.

    models_loc.csv: This is a timestamped record of when each model was saved. It has the following format -
    `timestamp,step,model_filename`

    summary.json: This file contains the hyperparameters used during a run and the final evaluation metrics. This file is written at the end of the run.

    metrics.csv: This file contains the user specified metric at each step in the run. It has the following format-
    `timestamp,step,metric_name,metric_value`

    param_hist.csv: This file contains a histogram of all the parameters in the model. Care must be take to set the right frequency for this call other wise it can result in pretty heavy I/O writes. The histograms all have 10 bins. This file has the following format-
    `timestamp,step,param_name,bin_0_lower,bin_0_upper,bin_0_mid,bin_0_freq,bin_1_lower,bin_1_upper,...`

    In addition to the CSV files, user can choose to log to stdout as well. The format of the stdout logs are a bit different. Refer to the documentation for StdoutMLExperiment.

    Args:
        name (str): The name of the experiment.
        dirpath (str): The root where the experiments will be logged.
        stdout (bool): Whether metrics should be logged to stdout in addition to CSV files.

    Apart from instantiating this class and passing it to the Trainer, the user should not have to call any other methods. Here is an example of the Trainer uses it.

    Example:
    ```
    from torchutils.ml_loggers.csv_logger import CsvMLExperiment

    EXPROOT = path.join("~", "temp", "experiments")
    exp = CsvMLExperiment("multiclass-exp", EXPROOT, stdout=True)

    with exp.start_run(run_name) as run:
        for epoch in range(10):
            run.log_tick(epoch)
    ```

    For a full working example see `examples/multiclass_classification_csv_logger.ipynb`.
    """

    def __init__(self, name: str, dirpath: str, stdout: bool = True) -> None:
        super().__init__(name)
        dirpath = path.expanduser(dirpath)
        self._exproot: str = path.join(dirpath, name.strip().lower())
        if path.exists(self._exproot):
            logger.warning(
                f"{self._exproot} already exists. Will add runs to the existing experiment."
            )
        else:
            os.mkdir(self._exproot)

        self._stdout = stdout

    @contextmanager
    def start_run(self, name: str) -> Generator[MLRun, None, None]:
        if self._stdout:
            run = CsvStdoutMLRun(name, self._exproot)
        else:
            run = CsvMLRun(name, self._exproot)
        yield run
        run.close()
