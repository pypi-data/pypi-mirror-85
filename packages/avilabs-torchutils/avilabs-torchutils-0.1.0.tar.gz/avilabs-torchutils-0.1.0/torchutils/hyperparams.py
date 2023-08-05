"""Classes for Organizing Hyper Parameters

There are two classes for organizing hyper parameters for a training run. The first is `Hyperparams`, which is used to organize the hyper parameter values for single training run. The second class is the `HyperparamsSpec` class that is used to specify a range of values for each hyper parameter that will be used by the auto-tuner module to doing a Bayesian search for optimal hyper parameters.
"""

import dataclasses as dc
import os.path as path
from configparser import ConfigParser
from typing import Any, Callable, Dict, List


@dc.dataclass
class Hyperparams:
    """Class to organize all the hyper parameters used in a training run in a single place

    Example:
        ```
        from torchutils import Hyperparams

        @dataclass
        class MyHyperparams(Hyperparams):
            n_epochs: int
            batch_size: int
            lr: float
        ```
        All the examples use this pattern. Specifically see `binary_classification_stdout_logger.ipynb`.

        It is now possible to load the hyperparams either in the program, or from a INI config file.
        ```
        [HYPERPARAMS]
        n_epochs = 5
        batch_size = 32
        lr = 0.0001
        ```
    """

    def to_dict(self):
        ret = {}
        for fld in dc.fields(self):
            ret[fld.name] = getattr(self, fld.name)
        return ret

    @classmethod
    def load(cls, conffile: str) -> "Hyperparams":
        conf = ConfigParser()
        if not path.exists(conffile):
            raise ValueError(f"Unable to find {conffile}")
        conf.read(conffile)
        confgetters = {int: conf.getint, float: conf.getfloat, bool: conf.getboolean, str: conf.get}
        kwargs = {}
        for fld in dc.fields(cls):
            if fld.name in conf["HYPERPARAMS"]:
                kwargs[fld.name] = confgetters[fld.type]("HYPERPARAMS", fld.name)
        return cls(**kwargs)


@dc.dataclass
class HyperparamsSpec:
    """Class to specify a range of values for different hyper parameters

    Objects of this class are only needed if the hyper parameters need to be auto-tuned. This class must be accompanied by a child class of `Hyperparams`.

    Args:
        spec: This is a list of dictionaries specifying the domain for each hyper parameter that will be used to sample values. This follows the same format as the [ax.dev documentation](https://ax.dev/api/storage.html?highlight=range#ax.storage.utils.DomainType)
        factory: This is the concrete `Hyperparams` class.

    Example:
        ```
        from torchutils import Hyperparams, HyperparamsSpec

        @dataclass
        class MyHyperparams(Hyperparams):
            n_epochs: int
            batch_size: int
            lr: float

        hparams_spec = HyperparamsSpec(
            factory=MyHyperparams,
            spec=[
                {"name": "batch_size", "type": "choice", "value_type": "int", "values": [16, 32, 64]},
                {"name": "n_epochs", "type": "range", "value_type": "int", "bounds": [7, 23]},
                {"name": "lr", "type": "range", "bounds": [1e-4, 0.4], "log_scale": True},
            ],
        )
        ```
        For a full working example see `examples/tune_binary_classification.ipynb`.
    """

    spec: List[Dict[str, Any]]
    factory: Callable[[Dict[str, Any]], Hyperparams]
