"""Convenience functions to visualize metrics logged in CSV files

These functions are used for quick analysis inside a Jupyter notebook. For a full working example see `examples/transfer_learning.ipynb`.

Please install `pip install termcolor` if you want to use this visualizer.
"""
import json
import os
import os.path as path
from typing import Any, Dict, Tuple
from collections import defaultdict, namedtuple

import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
from termcolor import cprint

Plot = namedtuple("Plot", ["name", "color"])


def _calc_layout(n: int) -> Tuple[int, int]:
    nrows = max(1, int(np.ceil(n / 3)))
    ncols = 3
    assert nrows * ncols >= n
    return nrows, ncols


def _next_cell(row, col, ncols) -> Tuple[int, int]:
    if col > ncols:
        return row + 1, 1
    else:
        return row, col + 1


def _train_val_split(name) -> Tuple[str, str]:
    flds = name.split("_")
    if len(flds) > 1 and (flds[0] == "train" or flds[0] == "val"):
        return flds[0], flds[1]
    else:
        return "", name


def _display_summary(runroot: str) -> None:
    summary_file = path.join(runroot, "summary.json")

    summary: Dict[str, Any] = {}
    with open(summary_file, "rt") as f:
        summary = json.load(f)

    eval_metric_names = list(summary["evaluation_metrics"].keys())
    cprint("Evaluation Metrics", attrs=["bold"])
    width = max(len(name) for name in eval_metric_names) + 2
    for eval_metric_name in eval_metric_names:
        eval_metric_val = np.around(summary["evaluation_metrics"][eval_metric_name], 3)
        cprint(f"  {eval_metric_name: <{width}}: {eval_metric_val}")

    print("\n")

    hparam_names = list(summary["hyperparams"].keys())
    cprint("Hyper Parameters", attrs=["bold"])
    width = max(len(name) for name in hparam_names) + 2
    for hparam_name in hparam_names:
        if isinstance(summary["hyperparams"][hparam_name], float):
            hparam_val = np.around(summary["hyperparams"][hparam_name], 3)
        else:
            hparam_val = summary["hyperparams"][hparam_name]
        cprint(f"  {hparam_name: <{width}}: {hparam_val}")


def _display_metrics(runroot: str) -> None:
    file = path.join(runroot, "metrics.csv")
    df = pd.read_csv(file, parse_dates=["timestamp"])
    names = set(df.name.unique())
    names.remove("tick")
    graphs = defaultdict(list)
    colors = {"train": "red", "val": "blue"}
    for name in names:
        prefix, metric_name = _train_val_split(name)
        color = colors.get(prefix, "green")
        graphs[metric_name].append(Plot(name=name, color=color))

    metric_names = list(graphs.keys())
    nrows, ncols = _calc_layout(len(metric_names))
    metric_names = list(graphs.keys())
    fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=metric_names)
    row, col = 1, 0
    for metric_name in metric_names:
        row, col = _next_cell(row, col, ncols)
        plots = graphs[metric_name]
        for plot in plots:
            metric_df = df[df.name == plot.name]
            fig.add_scatter(
                x=metric_df.step.values,
                y=metric_df.value.values,
                name=plot.name,
                row=row,
                col=col,
                line_color=plot.color,
            )

    fig.show()


def analyze(*, exproot: str, run_name: str) -> None:
    """Analyze a specific run

    This function will print out the summary stats of a run, i.e,. its evaluation metrics and the hyperparameters used. Additionally it will graph all the metric logs for both training as well validation datasets.

    Args:
        exproot (str): The experiment directory.
        run_name (str): The run that needs to be analyzed. It is assumed that the run files will be under the exproot directory.
    """
    runroot = path.expanduser(path.join(exproot, run_name))
    _display_summary(runroot)
    _display_metrics(runroot)


def compare(exproot: str) -> pd.DataFrame:
    """Compare all the runs in an experiment

    This function gathers all the summary from all the runs under the experiment and creates a pandas dataframe with the run_name and all the evaluation metrics as columns.
    """
    exproot = path.expanduser(exproot)
    # run_names = os.listdir(exproot)
    run_names = [x.name for x in sorted(os.scandir(exproot), key=lambda x: x.stat().st_ctime)]
    summary_file = path.join(exproot, run_names[0], "summary.json")
    summary = {}
    with open(summary_file, "rt") as f:
        summary = json.load(f)

    eval_metric_names = list(summary["evaluation_metrics"].keys())
    hparam_names = list(summary["hyperparams"].keys())

    data = {"run_names": []}
    for eval_metric_name in eval_metric_names:
        data[eval_metric_name] = []
    for hparam_name in hparam_names:
        data[hparam_name] = []

    for run_name in run_names:
        summary_file = path.join(exproot, run_name, "summary.json")
        if not path.exists(summary_file):
            cprint(f"Ignoring empty run {run_name}.", "yellow")
            continue
        with open(summary_file, "rt") as f:
            summary = json.load(f)
        data["run_names"].append(run_name)

        for eval_metric_name in eval_metric_names:
            eval_metric_val = summary["evaluation_metrics"][eval_metric_name]
            data[eval_metric_name].append(eval_metric_val)

        for hparam_name in hparam_names:
            hparam_val = summary["hyperparams"][hparam_name]
            data[hparam_name].append(hparam_val)

    disp_metric_name = eval_metric_names[0].replace("val_", "").capitalize()
    cprint("To plot using this dataframe:", attrs=["bold"])
    cprint(
        f"fig = go.Figure(layout_title_text='{disp_metric_name}', layout_xaxis_title='Runs'", "blue"
    )
    cprint(f"fig.add_bar(x=summary.run_names, y=summary.{eval_metric_names[0]})\n", "blue")
    return pd.DataFrame(data)
