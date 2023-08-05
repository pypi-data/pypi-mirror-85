"""
Not all schedulers have a common base class. Most schedulers seem to derive from a private
class _LRScheduler, but there are some schedulers like ReduceLROnPlateau that don't. This
abstract base class registers all known schedulers as its subsclass.
"""

from abc import ABC
import torch.optim.lr_scheduler as lrs


class LRScheduler(ABC):
    pass


LRScheduler.register(lrs.LambdaLR)
# LRScheduler.register(lrs.MultiplicativeLR)
LRScheduler.register(lrs.StepLR)
LRScheduler.register(lrs.MultiStepLR)
LRScheduler.register(lrs.ExponentialLR)
LRScheduler.register(lrs.CosineAnnealingLR)
LRScheduler.register(lrs.ReduceLROnPlateau)
LRScheduler.register(lrs.CyclicLR)
# LRScheduler.register(lrs.OneCycleLR)
LRScheduler.register(lrs.CosineAnnealingWarmRestarts)
