import numpy as np

from .extra.arithematic import SAMPLE_X


def add_fn(array1, array2):
    array1 = np.array(array1)
    array2 = np.array(array2)
    return array1 + array2


def sub_fn(array1, array2):
    array1 = np.array(array1)
    array2 = np.array(array2)
    return array1 - array2
