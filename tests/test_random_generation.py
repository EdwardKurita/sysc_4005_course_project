import numpy as np
import pytest

from sysc_4005_course_project.model.config import load_config
from sysc_4005_course_project.model.random_generation import draw_bags

BAGS = load_config().bags
N = 100_000


@pytest.mark.parametrize(("ptype", "mean"), [("commuter", 0.35), ("provincial", 0.90)])
def test_bag_draws_match_distribution(ptype, mean):
    rng = np.random.default_rng(12345)
    pmf = np.array(BAGS[ptype])
    draws = np.array([draw_bags(rng, pmf) for _ in range(N)])

    assert set(draws) == {0, 1, 2}
    # Within 4 standard errors of the theoretical values: a false failure is very unlikely.
    observed = np.bincount(draws, minlength=3) / N
    assert np.all(np.abs(observed - pmf) <= 4 * np.sqrt(pmf * (1 - pmf) / N))
    assert abs(draws.mean() - mean) <= 4 * draws.std(ddof=1) / np.sqrt(N)
