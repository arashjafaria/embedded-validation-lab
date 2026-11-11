
import pytest
from aeb import Scenario, simulate, time_to_collision


def test_invalid_aeb_configuration():
    """Reject an invalid braking threshold."""
    scenario = Scenario(
        name="Invalid AEB threshold",
        gap_m=30.0,
        ego_speed_mps=15.0,
        lead_speed_mps=0.0,
        ttc_threshold_s=0.0,
    )

    with pytest.raises(ValueError):
        scenario.validate()


def test_negative_ttc_input():
    """Reject a negative distance."""
    with pytest.raises(ValueError):
        time_to_collision(-5.0, 15.0, 0.0)


def test_invalid_simulation_time_step():
    """Reject an invalid simulation time step."""
    scenario = Scenario(
        name="Invalid time step",
        gap_m=30.0,
        ego_speed_mps=15.0,
        lead_speed_mps=0.0,
    )

    with pytest.raises(ValueError):
        simulate(scenario, dt_s=-0.01)


def test_collision_at_initial_gap():
    """Detect a collision already present at simulation start."""
    scenario = Scenario(
        name="Initial collision",
        gap_m=0.0,
        ego_speed_mps=15.0,
        lead_speed_mps=0.0,
    )

    result = simulate(scenario)

    assert result["collision"] is True
    assert result["minimum_gap_m"] == 0.0

