import os
import random

import numpy as np
import torch

from .config import DEFAULT_RANDOM_SEED


def fix_random_seed(seed: int = DEFAULT_RANDOM_SEED):
    """
    Fixes the random seed for all pseudo-random number generators,
    including Python-native, Numpy and Pytorch.

    :param seed: Random seed, defaults to DEFAULT_RANDOM_SEED.
    :type seed: int, optional
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
