import numpy as np
import pandas as pd
from datastream import Datastream

from {{cookiecutter.package_name}} import problem


def evaluate_datastreams():
    evaluate_datasets = problem.evaluate_datasets()
    evaluate_datasets['train'] = evaluate_datasets['train'].split(
        key_column='index',
        proportions=dict(gradient=0.8, early_stopping=0.2),
        stratify_column='class_name',
        filepath='{{cookiecutter.package_name}}/splits/early_stopping.json',
    )

    return {
        split_name: Datastream(dataset)
        for split_name, dataset in dict(
            gradient=evaluate_datasets['train']['gradient'],
            early_stopping=evaluate_datasets['train']['early_stopping'],
            compare=evaluate_datasets['compare'],
        ).items()
    }
