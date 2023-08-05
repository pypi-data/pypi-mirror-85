"""Various helping functions"""
from typing import Callable, Iterable
from time import time


def now(
    secs: int = 0,
    mins: int = 0,
    hrs: int = 0,
    days: int = 0,
    milisecond: bool = False,
):
    """
    Get time in Unix
    Args:
        sec : Seconds
        min : Minutes
        hr  : Hours
        day : Days
        milisecond : miliseconds or seconds
    Returns:
        int : unix time
    """
    current = int(time())
    delta = secs * 1 + mins * 60 + hrs * 3600 + days * 3600 * 24
    result = current + delta
    return result * 1000 if milisecond else result


def find(predicate: Callable, items: Iterable, default=None):
    """Find first item in the iterable
    that matches using predicate function
    - A predicate function must always return a boolean value
    """
    return next((x for x in items if predicate(x) is True), default)
