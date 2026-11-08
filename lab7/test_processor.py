
import pytest
from hypothesis import given, strategies as st

from processor import target_temperature, hvac_action, energy_alert


# --------------------------------------------------
# 1. FUZZ TESTS FOR target_temperature()
# --------------------------------------------------

@given(st.text().filter(lambda x: x not in ["home", "away", "sleep"]))
def test_invalid_mode(mode):
    with pytest.raises(ValueError):
        target_temperature(mode, True, 10)


@given(st.one_of(
    st.integers().filter(lambda x: x < 0 or x > 23),
    st.text(),
    st.none()
))
def test_invalid_hour(hour):
    with pytest.raises((TypeError, ValueError)):
        target_temperature("home", True, hour)


@given(st.one_of(st.integers(), st.text(), st.none()))
def test_invalid_occupancy(occupied):
    with pytest.raises((TypeError, ValueError)):
        target_temperature("home", occupied, 10)


# --------------------------------------------------
# 2. FUZZ TESTS FOR hvac_action()
# --------------------------------------------------

invalid_values = st.one_of(
    st.text(),
    st.none(),
    st.booleans(),
    st.lists(st.integers())
)


@given(invalid_values)
def test_invalid_current_temperature(current):
    with pytest.raises((TypeError, ValueError)):
        hvac_action(current, 22, 25)


@given(invalid_values)
def test_invalid_target_temperature(target):
    with pytest.raises((TypeError, ValueError)):
        hvac_action(20, target, 25)


@given(invalid_values)
def test_invalid_outside_temperature(outside):
    with pytest.raises((TypeError, ValueError)):
        hvac_action(20, 22, outside)


# --------------------------------------------------
# 3. FUZZ TESTS FOR energy_alert()
# --------------------------------------------------

@given(st.lists(
    st.one_of(st.text(), st.none(), st.booleans()),
    min_size=1
))
def test_invalid_energy_readings(readings):
    with pytest.raises((TypeError, ValueError)):
        energy_alert(readings, 100)


def test_empty_energy_readings():
    with pytest.raises(ValueError):
        energy_alert([], 100)


@given(invalid_values)
def test_invalid_energy_limit(limit):
    with pytest.raises((TypeError, ValueError)):
        energy_alert([10, 20, 30], limit)


@given(st.lists(
    st.floats(allow_nan=False, allow_infinity=False),
    min_size=1
))
def test_energy_alert_valid_readings(readings):
    result = energy_alert(readings, 100)

    assert result in ["ok", "warning", "critical"]
