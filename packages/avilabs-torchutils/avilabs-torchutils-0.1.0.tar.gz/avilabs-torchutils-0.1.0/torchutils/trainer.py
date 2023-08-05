"""Classes for Configuring and Running Training

The main class is the Trainer which runs the actual training run. The accompanying dataclass is TrainerArgs that can be used to configure a training run. Users are expected to write a function that will take in the hyper parameters, the training set, and the validation set and will return the TrainerArgs. This function is passed to the train method of Trainer which will call it to get the training args before starting the training run. The reason for not giving the TrainerArgs directly to the train method is because the typical usage is to use the same trainer for multiple training runs. The user defined function can be programmed to generate different training args for different runs.
"""
import logging
import sys
from collections import namedtuple
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Sequence, Tuple, cast

import numpy as np
import torch as t
from torch.optim import Optimizer
from torch.utils.data import DataLoader, Dataset

from .hyperparams import Hyperparams
from .ml_logger import MLExperiment
from .schedulers import LRScheduler

MetricFunc = Callable[[t.Tensor, t.Tensor], float]
logger = logging.getLogger(__name__)

Metric = namedtuple("Metric", ["name", "value"])


@dataclass
class TrainerArgs:
    """Configuration for a single training run

    Attributes:
        run_name: Name of the training run. This is expected to be unique within the scope of an experiment.
        model: Model to be trained.
        optimizer: Optimizer to use. It should already be set with the model parameters.
        loss_fn: Loss function to use. It should take in the output tensor and the input tensor and is expected to return a float.
        trainloader: An instance of dataloader that is set with the underlying training dataset.
        valloader: An instance of dataloader that is set with the underlying validation dataset.
        n_epochs: The number of epochs to train for.
        grad_warning_threshold (optional): The Trainer will log a warning if any of the parameter gradients are more than this threshold. The default value is 1000.
        loss_warning_threshold (optional): The Trainer will log a warning if the loss is higher than this threshold. The default value is 10_000.
        clip_grads (optional): The abolute value beyond with the gradients will be clipped in both directions. The default value is set to infinity, i.e., no clipping will occur.
        lr_scheduler (optional): A learning rate scheduler. It is expected that it is set with the optimizer.
    """

    run_name: str
    model: t.nn.Module
    optimizer: Optimizer
    loss_fn: Callable[[t.Tensor, t.Tensor], t.Tensor]
    trainloader: DataLoader
    valloader: DataLoader
    n_epochs: int
    grad_warning_threshold: float = 1000
    loss_warning_threshold: float = 10_000
    clip_grads: float = float("inf")
    lr_scheduler: Optional[LRScheduler] = None


ArgsBuilderType = Callable[[Hyperparams, Dataset, Dataset], TrainerArgs]

DEVICE = t.device("cuda" if t.cuda.is_available() else "cpu")


class Trainer:
    """The main class that does the training. Training is configured in two ways, one is at the constructor level. This configuration applies to all the training runs run by this Trainer. Another is for each training run.

    Args:
        experiment (MLExperiment): A derived class of MLExperiment that is used to log the training metrics.
        trainset (Dataset): The training dataset which will be passed to the user defined function that will build the trainer args.
        valset (Dataset): The validation dataset which will be passed to the user defined function that will build the trainer args.
        metric_functions (Sequence[MetricFunc]): A list of functions, each of which will take in the targets and outputs as input, and will return a float. The function names should be descriptive enough because they will be used as the name of the metric.
        verbose (bool): When set to True, will set the log frequency of the metrics logging, model logging, and params logging to log every step, which in most cases will mean to log on every epoch.
    """

    def __init__(
        self,
        experiment: MLExperiment,
        trainset: Dataset,
        valset: Dataset,
        metric_functions: Sequence[MetricFunc],
        verbose: bool = False,
    ) -> None:
        self._trainset = trainset
        self._valset = valset

        tempdl = DataLoader(self._trainset, batch_size=2)
        _, batch_target = next(iter(tempdl))
        self._target_dtype = batch_target.dtype

        self._metric_functions = metric_functions
        self._experiment = experiment
        self._args: Optional[TrainerArgs] = None

        # Does not log anything by default
        self.metrics_log_frequency: int = 1 if verbose else sys.maxsize
        self.model_log_frequency: int = 1 if verbose else sys.maxsize
        self.params_log_frequency: int = 1 if verbose else sys.maxsize

        self.model: Optional[t.nn.Module] = None
        self.final_metrics: Dict[str, float] = {}

    def _train(self, calc_metrics: bool = False,) -> Tuple[float, Dict[str, float]]:
        args = cast(TrainerArgs, self._args)
        model = cast(t.nn.Module, self.model)

        traindl = args.trainloader
        optim = args.optimizer
        loss_fn = args.loss_fn
        clip_grads = args.clip_grads

        model.train()
        losses = []
        outputs = t.Tensor([]).to(DEVICE)  # pyre-ignore
        targets = t.Tensor([]).to(self._target_dtype).to(DEVICE)  # pyre-ignore
        with t.enable_grad():
            for batch_inputs, batch_targets in traindl:
                batch_inputs = batch_inputs.to(DEVICE)
                batch_targets = batch_targets.to(DEVICE)

                optim.zero_grad()
                batch_outputs = model.forward(batch_inputs)
                loss = loss_fn(batch_outputs, batch_targets)
                loss.backward()

                if clip_grads < float("inf"):
                    t.nn.utils.clip_grad_value_(model.parameters(), clip_grads)

                optim.step()

                losses.append(loss.detach().item())

                if calc_metrics:
                    outputs = t.cat((outputs, batch_outputs.detach()))
                    targets = t.cat((targets, batch_targets))

        loss = np.mean(losses)
        outputs = outputs.cpu()
        targets = targets.cpu()
        metrics: Dict[str, float] = {}
        if calc_metrics:
            metrics["train_loss"] = loss
            for metric_func in self._metric_functions:
                metrics["train_" + metric_func.__name__] = metric_func(targets, outputs)

        return loss, metrics

    def _validate(self):
        args = cast(TrainerArgs, self._args)
        model = cast(t.nn.Module, self.model)

        valdl = args.valloader
        loss_fn = args.loss_fn

        model.eval()
        losses = []
        outputs = t.Tensor([]).to(DEVICE)
        targets = t.Tensor([]).to(self._target_dtype).to(DEVICE)
        with t.no_grad():
            for batch_inputs, batch_targets in valdl:
                batch_inputs = batch_inputs.to(DEVICE)
                batch_targets = batch_targets.to(DEVICE)
                batch_outputs = model(batch_inputs)
                loss = loss_fn(batch_outputs, batch_targets)
                losses.append(loss.detach().item())
                outputs = t.cat((outputs, batch_outputs))
                targets = t.cat((targets, batch_targets))

        loss = np.mean(losses)
        outputs = outputs.cpu()
        targets = targets.cpu()
        metrics: Dict[str, float] = {}
        metrics["val_loss"] = loss
        for metric_func in self._metric_functions:
            metrics["val_" + metric_func.__name__] = metric_func(targets, outputs)

        return loss, metrics

    def train(self, hparams: Hyperparams, args_builder: ArgsBuilderType) -> None:
        """Method to run one training run

        First calls the args_builder to get an object of type TrainerArgs. Then runs the training for the number of epochs specified in the trainer args, all the while gathering the metrics that were provided to the Trainer's constructor.

        Args:
            hparams (Hyperparams): The set of hyperparameters to use for this training run.
            args_builder (AgrsBuilderType): A function that takes in the training dataset, the validation dataset, and the hyperparams, and returns an instance of TrainerArgs.

        Example:
        ```
        import torch as t
        from torchutils import Hyperparams, Trainer, TrainerArgs
        from torchutils.ml_loggers.stdout_logger import StdoutMLExperiment

        @dataclass
        class MyHyperparams(Hyperparams):
            batch_size: int
            learning_rate: float

        def build_trainer(hparams, trainset, valset):
            run_name = "my awesome run"
            model = MyAwesomeModel()
            optim = t.optim.Adam(model.parameters(), lr=hparams.learning_rate)
            loss_fn = t.nn.BCELoss()
            traindl = DataLoader(trainset, batch_size=hparams.batch_size, shuffle=True)
            valdl = DataLoader(valset, batch_size=hparams.batch_size)
            return TrainerArgs(
                run_name=run_name,
                model=model,
                optimizer=optim,
                loss_fn=loss_fn,
                trainloader=traindl,
                valloader=valdl,
                n_epochs=10
            )

        exp = StdoutMLExperiment("awesome-experiment")
        trainset = MyTrainingDataset()
        valset = MyValidationDataset()

        hparams = MyHyperparams(learning_rate=0.005, batch_size=32)
        trainer = Trainer(exp, trainset, valset, metric_functions=[metric])
        trainer.train(hparams, build_trainer)
        ```

        See full example in `examples/binary_classification_stdout_logger.ipynb`.
        """
        args = args_builder(hparams, self._trainset, self._valset)
        model = args.model.to(DEVICE)

        self._args = args
        self.model = model

        with self._experiment.start_run(args.run_name) as run:
            for epoch in range(1, args.n_epochs + 1):
                run.log_tick(epoch)
                train_loss: float = 0.0
                val_loss: float = 0.0
                if epoch % self.metrics_log_frequency == 0:
                    train_loss, metrics = self._train(calc_metrics=True)
                    val_loss, val_metrics = self._validate()
                    metrics.update(val_metrics)
                    for metric_name, metric_value in metrics.items():
                        run.log_metric(epoch, metric_name, metric_value)
                else:
                    train_loss, _ = self._train()

                if args.lr_scheduler is not None:
                    lr = args.lr_scheduler.get_last_lr()[0]
                    run.log_metric(epoch, "scheduled_lr", lr)
                    args.lr_scheduler.step()

                # Warn about high loss values
                if train_loss > args.loss_warning_threshold:
                    logger.warning(f"Epoch {epoch}: Training loss {train_loss:.3f} is too high!")
                if val_loss > args.loss_warning_threshold:
                    logger.warning(f"Epoch {epoch}: Validation loss {val_loss:.3f} is too high!")

                # Warn about high gradients
                # pyre-ignore
                max_grad = t.max(t.Tensor([t.max(param) for param in self.model.parameters()]))
                if max_grad > args.grad_warning_threshold:
                    logger.warning(f"Epoch {epoch}: Gradient {max_grad:.3f} is too high!")

                # Checkpoint the model if needed
                if epoch % self.model_log_frequency == 0:
                    run.log_model(epoch, model)

                # Log the parameters histogram if needed
                if epoch % self.params_log_frequency == 0:
                    run.log_params(epoch, self.model.state_dict())

            # Calculate the final metrics on the validation dataset and log them
            # as part of run summary along with the hyperparams
            _, self.final_metrics = self._validate()
            run.log_summary(hparams.to_dict(), self.final_metrics)
