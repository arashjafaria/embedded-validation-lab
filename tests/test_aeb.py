import pytest
from aeb import Scenario, simulate, time_to_collision


def test_ttc_known_value():
    assert time_to_collision(30, 15, 0) == 2.0


def test_ttc_infinite_if_not_closing():
    assert time_to_collision(25, 10, 10) == float("inf")


def test_safe_stop_avoids_collision():
    result = simulate(Scenario("safe", 30, 15, 0))
    assert result["aeb_triggered"] is True
    assert result["collision"] is False
    assert result["minimum_gap_m"] > 0


def test_very_short_gap_causes_collision():
    result = simulate(Scenario("unsafe", 8, 20, 0, response_delay_s=0.5, braking_mps2=4))
    assert result["aeb_triggered"] is True
    assert result["collision"] is True


def test_same_speed_does_not_brake():
    result = simulate(Scenario("equal", 25, 10, 10))
    assert result["aeb_triggered"] is False
    assert result["collision"] is False


def test_invalid_scenario_rejected():
    with pytest.raises(ValueError):
        simulate(Scenario("bad", -2, 10, 0))
def test_ttc_moving_lead_vehicle():
    # Test TTC when both vehicles are moving
    distance = 40
    ego_speed = 20
    lead_speed = 10

    expected_ttc = 4.0

    actual_ttc = time_to_collision(
        distance, ego_speed, lead_speed
    )

    assert actual_ttc == expected_ttc
def test_aeb_above_threshold():
    result = simulate(Scenario("above", 31.5, 15, 0))

    assert result["initial_ttc_s"] == 2.1
    assert result["trigger_at_s"] > 0


def test_aeb_exactly_at_threshold():
    result = simulate(Scenario("at_threshold", 30, 15, 0))

    assert result["initial_ttc_s"] == 2.0
    assert result["trigger_at_s"] == 0.0


def test_aeb_below_threshold():
    result = simulate(Scenario("below", 28.5, 15, 0))

    assert result["initial_ttc_s"] == 1.9
    assert result["trigger_at_s"] == 0.0

def test_aeb_default_response_delay():
    result = simulate(Scenario("default_delay", 30, 15, 0))

    assert result["trigger_at_s"] == 0.0
    assert result["braking_started_s"] == 0.2


def test_aeb_custom_response_delay():
    result = simulate(
        Scenario("custom_delay", 30, 15, 0, response_delay_s=0.5)
    )

    assert result["trigger_at_s"] == 0.0
    assert result["braking_started_s"] == 0.5

def test_aeb_response_delay_tolerance():
    dt = 0.07
    expected_delay = 0.2

    scenario = Scenario(
        "timing_tolerance",
        30, 15, 0
    )

    result = simulate(scenario, dt_s=dt)

    actual_start = result["braking_started_s"]

    assert result["trigger_at_s"] == 0.0
    assert actual_start is not None

    # Braking must not start before the expected delay
    assert actual_start >= expected_delay

    # Braking must start within one simulation time step
    assert actual_start < expected_delay + dt

