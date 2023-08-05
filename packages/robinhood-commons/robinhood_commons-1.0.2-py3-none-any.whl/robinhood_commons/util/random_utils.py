import random
from typing import Sequence, Set


def random_float(end: float, start: float = 0.0):
    return random.uniform(start, end)


def get_unique_random(iterable: Sequence, count: int) -> Set[str]:
    indices: Set[str] = set()

    while len(indices) < count:
        indices.add(random.choice(iterable))

    return indices


def get_unique_randoms(iterable: Sequence, count: int) -> Set[str]:
    indices: Set[str] = set()
    num_items: int = min(len(iterable), count)

    while len(indices) < num_items:
        indices.add(random.choice(iterable).symbol)

    return indices
