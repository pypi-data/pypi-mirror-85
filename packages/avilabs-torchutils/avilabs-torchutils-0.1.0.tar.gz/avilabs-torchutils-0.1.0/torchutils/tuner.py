import logging
import sys
from typing import Any, Callable, Dict, Optional, Tuple, cast

import torch as t
from ax.service.managed_loop import optimize
from torch.utils.data import Dataset

from .hyperparams import Hyperparams, HyperparamsSpec
from .ml_logger import MLExperiment
from .trainer import Trainer, TrainerArgs

ArgsBuilderType = Callable[[Hyperparams, Dataset, Dataset], TrainerArgs]
MetricFunc = Callable[[t.Tensor, t.Tensor], float]
HparamsFactory = Callable[[Dict[str, Any]], Hyperparams]

logger: logging.Logger = logging.getLogger(__name__)


class Tuner:
    """Class to automatically tune the hyperparameters

    This class uses the hyperparameter tuning library ax.dev which in turn uses Bayesian optimization algorithms to sequentially search the hyperparameter space.

    Args:
        experiment (MLExperiment): The experiment that will be used to log the training metrics.
        trainset (Dataset): The training dataset which will be passed to the user defined function that will build the trainer args.
        valset (Dataset): The validation dataset which will be passed to the user defined function that will build the trainer args.
        obj_metric (MetricFunc): The objective function that the tuner will try to maixmize. It should take in a tuple of 2 tensors and return a float.
        miminize (bool): If the tuner should minimize the objective function, set this to True. Default is False.
    """

    def __init__(
        self,
        experiment: MLExperiment,
        trainset: Dataset,
        valset: Dataset,
        obj_metric: MetricFunc,
        minimize: bool = False,
    ) -> None:
        self._obj_metric: MetricFunc = obj_metric
        self._trainer = Trainer(experiment, trainset, valset, [obj_metric])
        self._trainer.metrics_log_frequency = sys.maxsize
        self._model_log_frequency: int = sys.maxsize
        self._minimize = minimize

        self._hparams_factory: Optional[HparamsFactory] = None
        self._args_builder: Optional[ArgsBuilderType] = None

    @property
    def metrics_log_frequency(self) -> int:
        return self._trainer.metrics_log_frequency

    @metrics_log_frequency.setter
    def metrics_log_frequency(self, freq: int) -> None:
        self._trainer.metrics_log_frequency = freq

    def _train_eval(self, hyper_params: Dict[str, Any]) -> Dict[str, Tuple[float, float]]:
        hparams_factory = cast(HparamsFactory, self._hparams_factory)
        hparams: Hyperparams = hparams_factory(**hyper_params)

        args_builder = cast(ArgsBuilderType, self._args_builder)
        self._trainer.train(hparams, args_builder)
        obj_name = self._obj_metric.__name__
        obj_val: Tuple[float, float] = (self._trainer.final_metrics["val_" + obj_name], 0.0)
        return {obj_name: obj_val}

    def tune(
        self, hparams_spec: HyperparamsSpec, args_builder: ArgsBuilderType, total_trials: int = 20
    ) -> Hyperparams:
        """Method to tune the hyperparameters

        Searches the hyperparameter space based on the hyperparameter spec. Will choose the next set of hyperpareters based on the last trial, and then run the full training for multiple epochs. Each full training run is called a trial. Will run the specified number of trials and choose the best performing hyperparameter.

        Args:
            hparams_spec (HyperparamSpec): The search space within which the tuner will search.
            args_builder (ArgsBuilderType): A function that takes in the training dataset, the validation dataset, and the hyperparams, and returns an instance of TrainerArgs.
            total_trials (int): Number of trials that will be run by the tuner before the best hyperparameters are chosen.

        Returns:
            Hyperparams: The best performing hyperparams.

        Example:
        ```
        import torch as t
        from torchutils import Hyperparams, Trainer, TrainerArgs
        from torchutils.ml_loggers.stdout_logger import StdoutMLExperiment

        @dataclass
        class MyHyperparams(Hyperparams):
            batch_size: int
            learning_rate: float
            n_epochs: int

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
                n_epochs=hparams.n_epochs
            )

        exp = StdoutMLExperiment("awesome-experiment")
        trainset = MyTrainingDataset()
        valset = MyValidationDataset()

        hparams_spec = HyperparamsSpec(
        factory=MyHyperparams,
            spec=[
                {"name": "batch_size", "type": "choice", "value_type": "int", "values": [16, 32, 64]},
                {"name": "n_epochs", "type": "range", "value_type": "int", "bounds": [7, 23]},
                {"name": "lr", "type": "range", "bounds": [1e-4, 0.4], "log_scale": True},
            ],
        )
        tuner = Tuner(exp, trainset, valset, accuracy)
        best_params = tuner.tune(hparams_spec, build_trainer, total_trials=10)
        ```

        See full example in `examples/tune_binary_classification.ipynb`.
        """
        self._hparams_factory = hparams_spec.factory
        self._args_builder = args_builder

        best_params, values, _, _ = optimize(
            hparams_spec.spec,
            evaluation_function=self._train_eval,  # pyre-ignore
            objective_name=self._obj_metric.__name__,
            total_trials=total_trials,
            minimize=self._minimize,
        )

        logger.info(f"best_params={best_params} values={values}")
        return hparams_spec.factory(**best_params)  # pyre-ignore
