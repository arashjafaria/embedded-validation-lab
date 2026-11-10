"""Educational 1-D AEB system-test model, NOT a real safety controller."""
from dataclasses import dataclass
from math import inf


@dataclass(frozen=True)
class Scenario:
    name: str
    gap_m: float
    ego_speed_mps: float
    lead_speed_mps: float
    ttc_threshold_s: float = 2.0
    response_delay_s: float = 0.2
    braking_mps2: float = 8.0

    def validate(self):
        if self.gap_m < 0 or self.ego_speed_mps < 0 or self.lead_speed_mps < 0:
            raise ValueError("Gap and vehicle speeds must be nonnegative")
        if self.ttc_threshold_s <= 0 or self.response_delay_s < 0 or self.braking_mps2 <= 0:
            raise ValueError("Invalid AEB threshold, delay, or deceleration")


def time_to_collision(gap_m: float, ego_speed_mps: float, lead_speed_mps: float) -> float:
    """Constant-relative-speed TTC. Returns inf when vehicles aren't closing."""
    if gap_m < 0 or ego_speed_mps < 0 or lead_speed_mps < 0:
        raise ValueError("Gap and speeds must be nonnegative")
    closing_speed = ego_speed_mps - lead_speed_mps
    return gap_m / closing_speed if closing_speed > 0 else inf


def simulate(s: Scenario, dt_s: float = 0.01, max_time_s: float = 10.0) -> dict:
    """Fixed-step, simple longitudinal model; no sensors, slip, or road dynamics."""
    s.validate()
    if dt_s <= 0 or max_time_s <= 0:
        raise ValueError("Time step and horizon must be positive")
    gap = s.gap_m
    min_gap = gap
    ego = s.ego_speed_mps
    triggered_at = None
    brake_started_at = None
    collision = gap == 0
    first_ttc = time_to_collision(gap, ego, s.lead_speed_mps)
    steps = int(max_time_s / dt_s)

    for i in range(steps):
        if collision:
            break
        t = i * dt_s
        ttc = time_to_collision(gap, ego, s.lead_speed_mps)
        if triggered_at is None and ttc <= s.ttc_threshold_s:
            triggered_at = t
        braking = triggered_at is not None and t + 1e-9 >= triggered_at + s.response_delay_s
        if braking and brake_started_at is None:
            brake_started_at = t
        next_ego = max(ego - s.braking_mps2 * dt_s, 0.0) if braking else ego
        ego_travel = (ego + next_ego) * 0.5 * dt_s
        lead_travel = s.lead_speed_mps * dt_s
        gap += lead_travel - ego_travel
        ego = next_ego
        min_gap = min(min_gap, gap)
        if gap <= 0:
            gap = 0.0
            collision = True
            break
        if ego <= s.lead_speed_mps and triggered_at is not None:
            break

    return {
        "scenario": s.name,
        "initial_ttc_s": round(first_ttc, 3) if first_ttc != inf else None,
        "aeb_triggered": triggered_at is not None,
        "trigger_at_s": round(triggered_at, 3) if triggered_at is not None else None,
        "braking_started_s": round(brake_started_at, 3) if brake_started_at is not None else None,
        "collision": collision,
        "minimum_gap_m": round(max(min_gap, 0.0), 3),
        "final_ego_speed_mps": round(ego, 3),
    }
