import pytest

from sysc_4005_course_project.model.config import CONFIG_DIR, load_config

BASELINE = (CONFIG_DIR / "baseline.toml").read_text(encoding="utf-8")


def write_variant(tmp_path, old: str, new: str):
    """Write a copy of the baseline config with one line changed."""
    assert old in BASELINE, f"{old!r} not in baseline.toml"
    path = tmp_path / "variant.toml"
    path.write_text(BASELINE.replace(old, new, 1), encoding="utf-8")
    return path


def test_baseline_matches_assignment():
    cfg = load_config()
    assert cfg.name == "baseline"
    assert cfg.simulation.horizon_min == 7 * 24 * 60
    assert cfg.commuter.arrival_rate_per_hour == 40
    assert cfg.provincial.lead_time.mean == 75
    assert cfg.provincial.lead_time.variance == 50
    assert cfg.bags["provincial"] == (0.30, 0.50, 0.20)
    assert (cfg.checkin.business_counters, cfg.checkin.coach_counters) == (1, 3)
    assert (cfg.security.business_screens, cfg.security.coach_screens) == (1, 2)


def test_variant_changes_only_what_was_edited(tmp_path):
    cfg = load_config(write_variant(tmp_path, "coach_counters = 3", "coach_counters = 4"))
    assert cfg.checkin.coach_counters == 4
    assert cfg.commuter == load_config().commuter


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("coach_counters = 3", "coach_counters = 6"),          # 1 + 6 > max 6
        ("business_counters = 1", "business_counters = 0"),
        ("coach_screens = 2", "coach_screens = 0"),
        ("coach_occupancy = 0.85", "coach_occupancy = 1.5"),
        ("commuter = [0.70, 0.25, 0.05]", "commuter = [0.70, 0.25, 0.10]"),
        ("screening_mean_min = 3.0", "screening_mean_min = 0.0"),
    ],
)
def test_invalid_values_rejected(tmp_path, old, new):
    with pytest.raises(ValueError):
        load_config(write_variant(tmp_path, old, new))


def test_misspelled_key_rejected(tmp_path):
    with pytest.raises(TypeError):
        load_config(write_variant(tmp_path, "coach_screens = 2", "coach_screen = 2"))
