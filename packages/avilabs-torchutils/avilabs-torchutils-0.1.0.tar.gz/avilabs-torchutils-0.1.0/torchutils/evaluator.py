"""Function to Evaluate a Trained Model

Use this function to get the evaluation metrics for a trained model. The model is usually evaluated on a test dataset that was not part of the training dataset.

Example:
    ```
    from torchutils import evaluate

    def my_first_metric(y_true, y_hat):
        pass

    def my_second_metric(y_true, y_hat):
        pass

    model = MyTrainedModel()
    testset = MyTestDataset()

    testdl = DataLoader(testset, batch_size=len(testset))
    results = evaluate(model, testdl, [my_first_metric, my_second_metric])

    print(results["my_first_metric"])
    print(results["my_second_metric"])
    ```

    See a full example in `examples/binary_classification_stdout_logger.ipynb`.
"""

from typing import Callable, Dict, Sequence, Union

import torch as t
from torch.utils.data import DataLoader

MetricFunc = Callable[[t.Tensor, t.Tensor], float]
DEVICE = t.device("cuda" if t.cuda.is_available() else "cpu")


def evaluate(
    model: t.nn.Module, dataloader: DataLoader, metric_functions: Sequence[MetricFunc]
) -> Dict[str, Union[float, t.Tensor]]:
    """Function that evaluates a model

    Args:
        model (t.nn.Module): The model that is to be evaluated.
        dataloader (DataLoader): An iterator that will yield a mini-batch, a tuple of inputs and targets.
        metric_functions (Callables): A list of function pointers. Each function should take in two arguments, the targets and the outputs, and
        output a single float value that is the metric.

    Returns:
        A dictionary with each metric function name as a key. It will have two additional keys, the "targets" and "outputs" of the evaluation.
    """
    model.eval()

    _, tmp = next(iter(dataloader))
    target_dtype = tmp.dtype

    outputs = t.Tensor([]).to(DEVICE)  # pyre-ignore
    targets = t.Tensor([]).to(target_dtype).to(DEVICE)  # pyre-ignore

    with t.no_grad():
        for batch_inputs, batch_targets in dataloader:
            batch_inputs = batch_inputs.to(DEVICE)
            batch_targets = batch_targets.to(DEVICE)

            batch_outputs = model(batch_inputs)
            outputs = t.cat((outputs, batch_outputs))
            targets = t.cat((targets, batch_targets))

    outputs = outputs.cpu()
    targets = targets.cpu()
    metrics: Dict[str, Union[float, t.Tensor]] = {}
    for metric_func in metric_functions:
        metrics[metric_func.__name__] = metric_func(targets, outputs)

    metrics["outputs"] = outputs
    metrics["targets"] = targets

    return metrics
