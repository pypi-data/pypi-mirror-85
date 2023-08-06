import argparse
import os
from pathlib import Path
import json
import logging
from functools import partial
import torch
from workflow.functional import starcompose
from workflow.ignite import worker_init
from workflow.ignite.handlers.learning_rate import (
    LearningRateScheduler, warmup, cyclical
)

from {{cookiecutter.package_name}} import train

logging.getLogger('ignite').setLevel(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--eval_batch_size', type=int, default=128)
    parser.add_argument('--minimum_learning_rate', type=float, default=1e-7)
    parser.add_argument('--n_batches', default=200, type=int)
    parser.add_argument('--n_batches_per_step', default=1, type=int)
    parser.add_argument('--patience', type=float, default=1)
    parser.add_argument('--n_workers', default=2, type=int)

    try:
        __IPYTHON__
        args = parser.parse_known_args()[0]
    except NameError:
        args = parser.parse_args()

    config = vars(args)
    config.update(
        seed=1,
        use_cuda=torch.cuda.is_available(),
        run_id=os.getenv('RUN_ID'),
        search_learning_rate=True,
        learning_rate=config['minimum_learning_rate'],
        max_epochs=1,
        n_batches_per_epoch=config['n_batches'],
    )

    Path('config.json').write_text(json.dumps(config))

    train(config)
