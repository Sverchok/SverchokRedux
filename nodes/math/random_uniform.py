import numpy as np


def random_uniform(low: float = 0.0, top: float = 1.0, count: int = 10) -> [("rnd uniform", np.ndarray)]:
    return np.random.uniform(low, top, count)

random_uniform.label = "Random uniform"

SvRxFunc = [random_uniform]
