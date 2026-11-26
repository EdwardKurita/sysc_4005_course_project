"""Random-number streams for each replication.

seeds/seeds.txt holds one base seed, generated once with numpy.random.SeedSequence().entropy.
Replication r uses SeedSequence(base_seed, spawn_key=(r,)), split into one generator per stream
in STREAMS. This gives:
  - independent replications (different r -> independent streams),
  - one stream per source of randomness, so a policy change in one station doesn't shift the
    random numbers used elsewhere,
  - the same streams for replication r under every config (common random numbers).
"""

from pathlib import Path

import numpy as np

SEED_FILE = Path(__file__).resolve().parents[3] / "seeds" / "seeds.txt"

# Only ever append to this list: reordering or inserting changes every existing stream.
STREAMS = (
    "commuter_arrivals",
    "provincial_occupancy",
    "provincial_lead_time",
    "bags",
    "checkin_service",
    "security_service",
)


def load_base_seed(path: str | Path = SEED_FILE) -> int:
    """Read the base seed (a single integer) from the seed file."""
    return int(Path(path).read_text(encoding="utf-8").strip())


def replication_streams(base_seed: int, replication: int) -> dict[str, np.random.Generator]:
    """Return one independent Generator per stream name for a replication."""
    if replication < 0:
        raise ValueError("replication index must be >= 0")
    children = np.random.SeedSequence(base_seed, spawn_key=(replication,)).spawn(len(STREAMS))
    return {name: np.random.default_rng(child) for name, child in zip(STREAMS, children, strict=True)}
