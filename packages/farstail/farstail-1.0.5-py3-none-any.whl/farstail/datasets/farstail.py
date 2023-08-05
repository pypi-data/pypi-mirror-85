"""FarsTail Persian Natural Language Inference(NLI) and Auestion Answering (QA) dataset.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ..utils.data_utils import get_file
from ..preprocessing.sequence import _remove_long_seq
import numpy as np
import pandas as pd
import json
import warnings


def load_indexed_data(path='Indexed-FarsTail.npz'):
    """Loads the indexed FarsTail dataset.
    # Arguments
        path: where to cache the data (relative to `~/.FarsTail/dataset`).
    # Returns
        *indexed FarsTail for non-Persian language researchers*
        1) Numpy arrays for indexed Train, Validation and Test data of Farstail 
        2) A dictionary mapping word indexes to their word

        train_ind, val_ind, test_ind, dictionary
    """
    path = get_file(path,
                    origin='https://raw.githubusercontent.com/dml-qom/FarsTail/master/data/Indexed-FarsTail.npz',
                    file_hash='ea86da737108bf4bdc74bd98eeec823c')

    with np.load(path, allow_pickle=True) as f:
        train_ind, val_ind, test_ind, dictionary = f['train_ind'], f['val_ind'], f['test_ind'], f['dictionary'].item()

    return train_ind, val_ind, test_ind, dictionary


def load_original_data(train_path='Train-word.csv', val_path='Val-word.csv', test_path='Test-word.csv'):
    """Loads the original FarsTail dataset.
    # Arguments
        path: where to cache the data (relative to `~/.FarsTail/dataset`).
    # Returns
        *original FarsTail for persian language researchers*
        Numpy arrays for original Train, Validation and Test data of Farstail:

        train_data, val_data, test_data
    """
    train_path = get_file(
        train_path,
        origin='https://raw.githubusercontent.com/dml-qom/FarsTail/master/data/Train-word.csv',
        file_hash='b25152d69420fa9543d2e3155c91a046')

    val_path = get_file(
        val_path,
        origin='https://raw.githubusercontent.com/dml-qom/FarsTail/master/data/Val-word.csv',
        file_hash='6686f1ff8dd0a64b519466589a686ec9')

    test_path = get_file(
        test_path,
        origin='https://raw.githubusercontent.com/dml-qom/FarsTail/master/data/Test-word.csv',
        file_hash='07d01f54f3a4991bc7067e2b68d84ab1')

    train_data = pd.read_csv(train_path, sep='\t')
    val_data = pd.read_csv(val_path, sep='\t')
    test_data = pd.read_csv(test_path, sep='\t')

    return train_data, val_data, test_data