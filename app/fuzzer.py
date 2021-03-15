"""Fuzzer.
"""
import random
import tempfile


def set_random_seed(seed):
    """Self-explanatory."""
    random.seed(seed)


def random_element(seq):
    """Returns a random single element from input sequence."""
    choice = random.choice(seq)
    return choice


def random_int(min_value, max_value):
    """min_value <= N <= max_value"""
    return random.randint(min_value, max_value)


def random_float(min_value, max_value):
    """min_value <= N <= max_value or min_value <= N < max_value (depending on rounding)."""
    return random.uniform(min_value, max_value)


def random_path(prefix="tmp", suffix=""):
    """Generates random path."""
    return tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix).name
