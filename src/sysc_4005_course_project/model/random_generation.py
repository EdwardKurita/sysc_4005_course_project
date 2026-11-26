"""Random-variate generators for the model inputs."""

import numpy as np


def draw_bags(rng: np.random.Generator, pmf) -> int:
    """Number of checked bags, drawn from pmf = (P(B=0), P(B=1), P(B=2)) in config.bags.

    rng.choice with p= uses discrete inverse transform: it compares a Uniform(0, 1) draw
    against the cumulative probabilities and returns the first bag count that exceeds it.
    """
    return int(rng.choice(len(pmf), p=pmf))
