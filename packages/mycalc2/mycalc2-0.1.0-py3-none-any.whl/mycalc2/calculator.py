"""
Calculator library containing basic math operations.
"""

from mycalc2.utils import SAMPLE_VAR, subtract_fn
from mycalc2.utils.numerical_utils import add_fn

# from .utils import SAMPLE_VAR
# from mycalc2.utils import sub_fn


def scale(x):
    return SAMPLE_VAR * x


def add(first_term, second_term):
    return first_term + second_term


def subtract(first_term, second_term):
    return first_term - second_term


def add_numpy(array1, array2):
    return add_fn(array1, array2)


def sub_numpy(array1, array2):
    return subtract_fn(array1, array2)
    # return sub_fn(array1, array2)
