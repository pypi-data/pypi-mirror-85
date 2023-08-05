"""Abstract Base Classes for Logging Training Metrics

An experiment is composed of multiple training runs. Both experiments and training runs are expressed as abstract base classes in this module. Experiments and their runs are logged using a concrete logger. E.g., torchutils ships with CSV loggers, stdout loggers, etc. Developers who want to implement their own loggers must subclass both the abstract base classes.
"""

from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Dict, Generator

import torch


class MLRun(ABC):
    """The abstract base class representing a run

    The concrete derived class will be instantiated via various class factories and passed to the main training function. The methods of this class can potentially be called for each mini-batch that is trained.

    Args:
        name: Name of the current run. This has to be unique within the experiment.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def log_summary(self, hparams: Dict[str, Any], metrics: Dict[str, float]) -> None:
        """Log the summary of the training run at the end

        Args:
            hparams: The hyperparameters used in this training run.
            metrics: The metric values of all the user specified metrics evaluated on the validation set.
        """
        raise NotImplementedError("Subclass must implement!")

    @abstractmethod
    def log_metric(self, step: int, name: str, val: float) -> None:
        """Log a particular metric at the end of each iteration

        This is typically called after a mini-batch of training is complete. The metrics are computed for both the training and the validation datasets. The metric name will be prefixed with train_ or val_ respectively by the trainer.

        Args:
            step: The iteration number.
            name: Name of the metric with a train_ or a val_ prefix.
            val: Value of the metric.
        """
        raise NotImplementedError("Subclass must implement!")

    @abstractmethod
    def log_params(self, step: int, state: Dict[str, torch.Tensor]) -> None:
        """Log all the trainable parameters of the model

        This is typically called after multiple iterations at some user specified frequency. A common way to implement this method is to calculate the histogram of the parameter values and log those. Attempting to log the parameters as they are might result in very large writes.

        Args:
            step: The iteration number.
            state: The state_dict from the model.
        """
        raise NotImplementedError("Subclass must implement!")

    @abstractmethod
    def log_model(self, step, model) -> None:
        """Save the model

        This is typically called after multiple iterations at some user specified frequency. The subclass is expected to provide some means for the user to retrieve the saved model.

        Args:
            step: The iteration number.
            model: The torch.nn.Moudule object.
        """
        raise NotImplementedError("Subclass must implement!")

    @abstractmethod
    def log_tick(self, step: int) -> None:
        """A no-op log at a set frequency

        The purpose of this log is to show progress in case the user has configured the trainer to not log anything. This is called at the beginning of each epoch. It is useful to calculate the average wall clock time taken by each epoch.

        Args:
            step: The iteration number.
        """
        raise NotImplementedError("Subclass must implement!")


class MLExperiment(ABC):
    """The abstract base class representing an experiment

    An experiment is usually composed of multiple runs. Each experiment is uniquely identified by its name. Its upto the derived class to more concretely define the namespace and enforce uniqueness within it.

    Args:
        name: Name of the experiment.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    @contextmanager
    def start_run(self, name: str) -> Generator[MLRun, None, None]:
        """A context manager to start a new run

        This method is expected to create the right concrete MLRun subclass and yield it. If there is cleanup that is needed at the end of the run, like closing file handles, committing datbase writes, etc. that can be done after the yield statement returns, which will happen at the end of the run.

        Args:
            name: Name of the run. This must be unique within the experiment.
        """
        pass
