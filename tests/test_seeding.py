import pytest

from sysc_4005_course_project.model import seeding
from sysc_4005_course_project.model.seeding import STREAMS, load_base_seed, replication_streams


@pytest.fixture
def base_seed() -> int:
    return load_base_seed()


def first_draws(streams, n=5):
    return {name: tuple(rng.random(n)) for name, rng in streams.items()}


def test_seed_file_holds_one_integer(base_seed):
    assert base_seed > 0


def test_same_replication_is_reproducible(base_seed):
    assert first_draws(replication_streams(base_seed, 3)) == first_draws(replication_streams(base_seed, 3))


def test_replications_differ(base_seed):
    a = first_draws(replication_streams(base_seed, 0))
    b = first_draws(replication_streams(base_seed, 1))
    assert all(a[name] != b[name] for name in STREAMS)


def test_streams_within_a_replication_differ(base_seed):
    draws = first_draws(replication_streams(base_seed, 0))
    assert len(set(draws.values())) == len(STREAMS)


def test_appending_a_stream_keeps_existing_streams(base_seed, monkeypatch):
    old = first_draws(replication_streams(base_seed, 0))
    monkeypatch.setattr(seeding, "STREAMS", STREAMS + ("new_stream",))
    new = first_draws(seeding.replication_streams(base_seed, 0))
    assert all(old[name] == new[name] for name in STREAMS)


def test_negative_replication_rejected(base_seed):
    with pytest.raises(ValueError):
        replication_streams(base_seed, -1)
