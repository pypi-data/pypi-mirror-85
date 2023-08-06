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
    parser.add_argument('--learning_rate', type=float, default=1e-3)
    parser.add_argument('--max_epochs', type=int, default=20)
    parser.add_argument('--n_batches_per_epoch', default=50, type=int)
    parser.add_argument('--n_batches_per_step', default=1, type=int)
    parser.add_argument('--patience', type=float, default=10)
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
    )

    Path('config.json').write_text(json.dumps(config))

    train(config)
