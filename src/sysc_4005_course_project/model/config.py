"""Model parameters, loaded from a config file (e.g. config/baseline.toml).

Each TOML section maps to one dataclass.
"""

import tomllib
from dataclasses import dataclass
from pathlib import Path

import numpy as np

CONFIG_DIR = Path(__file__).resolve().parents[3] / "config"


@dataclass(frozen=True)
class SimulationParams:
    horizon_min: float
    replications: int


@dataclass(frozen=True)
class CommuterParams:
    arrival_rate_per_hour: float
    first_departure_min: float
    departure_interval_min: float
    seats: int
    ticket_price: float
    flight_operating_cost: float


@dataclass(frozen=True)
class LeadTimeParams:
    mean: float
    variance: float


@dataclass(frozen=True)
class ProvincialParams:
    first_departure_min: float
    departure_interval_min: float
    business_seats: int
    coach_seats: int
    business_occupancy: float
    coach_occupancy: float
    business_ticket_price: float
    coach_ticket_price: float
    flight_operating_cost: float
    refund_min_lead_min: float
    lead_time: LeadTimeParams


@dataclass(frozen=True)
class CheckinParams:
    business_counters: int
    coach_counters: int
    max_counters: int
    boarding_pass_mean_min: float
    per_bag_mean_min: float
    other_delay_mean_min: float
    agent_wage_per_hour: float


@dataclass(frozen=True)
class SecurityParams:
    business_screens: int
    coach_screens: int
    screening_mean_min: float


@dataclass(frozen=True)
class FinanceParams:
    staffing_cap_fraction: float


@dataclass(frozen=True)
class Config:
    name: str
    simulation: SimulationParams
    commuter: CommuterParams
    provincial: ProvincialParams
    bags: dict[str, tuple[float, ...]]
    checkin: CheckinParams
    security: SecurityParams
    finance: FinanceParams


def load_config(path: str | Path = CONFIG_DIR / "baseline.toml") -> Config:
    """Read and validate a config file."""
    path = Path(path)
    with open(path, "rb") as f:
        data = tomllib.load(f)

    provincial = dict(data["provincial"])
    provincial["lead_time"] = LeadTimeParams(**provincial["lead_time"])

    cfg = Config(
        name=path.stem,
        simulation=SimulationParams(**data["simulation"]),
        commuter=CommuterParams(**data["commuter"]),
        provincial=ProvincialParams(**provincial),
        bags={ptype: tuple(pmf) for ptype, pmf in data["bags"].items()},
        checkin=CheckinParams(**data["checkin"]),
        security=SecurityParams(**data["security"]),
        finance=FinanceParams(**data["finance"]),
    )
    _validate(cfg)
    return cfg


def _validate(cfg: Config) -> None:
    p, c, s = cfg.provincial, cfg.checkin, cfg.security

    for name, prob in [("business_occupancy", p.business_occupancy),
                       ("coach_occupancy", p.coach_occupancy)]:
        if not 0 <= prob <= 1:
            raise ValueError(f"provincial.{name} must be in [0, 1], got {prob}")

    if set(cfg.bags) != {"commuter", "provincial"}:
        raise ValueError(f"[bags] needs exactly 'commuter' and 'provincial', got {list(cfg.bags)}")
    for ptype, pmf in cfg.bags.items():
        if any(prob < 0 for prob in pmf) or not np.isclose(sum(pmf), 1.0):
            raise ValueError(f"bags.{ptype} must be non-negative and sum to 1, got {pmf}")

    if c.business_counters < 1 or c.coach_counters < 1:
        raise ValueError("each check-in pool needs at least 1 counter")
    if c.business_counters + c.coach_counters > c.max_counters:
        raise ValueError(f"check-in counters exceed max_counters ({c.max_counters})")
    if cfg.simulation.replications < 1:
        raise ValueError("simulation.replications must be >= 1")
    if s.business_screens < 1 or s.coach_screens < 1:
        raise ValueError("each security pool needs at least 1 screen")

    positive = {
        "simulation.horizon_min": cfg.simulation.horizon_min,
        "commuter.arrival_rate_per_hour": cfg.commuter.arrival_rate_per_hour,
        "provincial.lead_time.variance": p.lead_time.variance,
        "checkin.boarding_pass_mean_min": c.boarding_pass_mean_min,
        "checkin.per_bag_mean_min": c.per_bag_mean_min,
        "checkin.other_delay_mean_min": c.other_delay_mean_min,
        "security.screening_mean_min": s.screening_mean_min,
    }
    for name, value in positive.items():
        if value <= 0:
            raise ValueError(f"{name} must be > 0, got {value}")
