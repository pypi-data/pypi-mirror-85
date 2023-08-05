"""Log training metrics to stdout

While other loggers group runs together under and experiment, the experiment does not matter for this logger. Each run is logged to stdout. This logger does not support logging the parameter histograms. When logging the model, it is saved to ./models directory.
"""

import os
from contextlib import contextmanager
from pprint import pprint
from typing import Any, Dict, Generator, List

import torch

from ..ml_logger import MLExperiment, MLRun


class StdoutMLRun(MLRun):
    """Concrete implementation of the abstract MLRun class

    This class does not need to be instantiated directly. It is instantiaged by the experiment class.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._models_root: str = os.path.join(".", "models")
        os.makedirs(self._models_root, exist_ok=True)
        self._curr_step = 0
        self._buffer: List[str] = []

    def log_summary(self, hparams: Dict[str, Any], metrics: Dict[str, float]) -> None:
        summary = {"hyperparams": hparams, "evaluation_metrics": {}}
        for metric_name, metric_value in metrics.items():
            summary["evaluation_metrics"][metric_name] = round(metric_value, 3)
        print("\nSummary:")
        pprint(summary)

    def log_tick(self, step: int) -> None:
        print(f"\nStep {step}")

    def log_metric(self, step: int, name: str, val: float) -> None:
        print(f"\t{name} = {val:.3f}")

    def log_params(self, step: int, state: Dict[str, torch.Tensor]) -> None:
        print("[WARN] Stdout does not support logging parameters")

    def log_model(self, step: int, model: torch.nn.Module) -> None:
        model_filename = f"{self.name}-model-{step}.pkl"
        model_path = os.path.join(self._models_root, model_filename)
        print(f"\nStep {step}: Checkpointing model at {model_filename}")
        torch.save(model, model_path)


class StdoutMLExperiment(MLExperiment):
    """Concrete implementation of the MLExperiment abstract base class

    It is expected that the user will instantiate this class directly and pass it to the Trainer. For a full working example see `examples/regression_stdout_logger.ipynb`.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)

    @contextmanager
    def start_run(self, name: str) -> Generator[MLRun, None, None]:
        run = StdoutMLRun(name)
        print(f"Starting run {name}")
        yield run
        # run.close()
