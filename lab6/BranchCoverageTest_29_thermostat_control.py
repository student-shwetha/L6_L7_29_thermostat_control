from thermostat_control import target_temperature, hvac_action, energy_alert


# Branch tests for target_temperature()

def test_away_mode():
    assert target_temperature("away", True, 12) == 16

def test_sleep_night_before_6():
    assert target_temperature("sleep", True, 5) == 18

def test_sleep_night_after_22():
    assert target_temperature("sleep", True, 22) == 18

def test_sleep_day():
    assert target_temperature("sleep", True, 12) == 20

def test_unoccupied():
    assert target_temperature("home", False, 12) == 18

def test_morning():
    assert target_temperature("home", True, 7) == 22

def test_not_morning():
    assert target_temperature("home", True, 12) == 20

def test_evening():
    assert target_temperature("home", True, 19) == 21

def test_not_evening():
    assert target_temperature("home", True, 12) == 20


# Branch tests for hvac_action()

def test_idle():
    assert hvac_action(20, 20.5, 15) == "idle"

def test_heat_boost():
    assert hvac_action(15, 22, 2) == "heat_boost"

def test_heat():
    assert hvac_action(15, 22, 10) == "heat"

def test_cool_boost():
    assert hvac_action(25, 20, 35) == "cool_boost"

def test_cool():
    assert hvac_action(25, 20, 25) == "cool"


# Branch tests for energy_alert()

def test_empty_readings():
    assert energy_alert([], 10) == "ok"

def test_all_within_limit():
    assert energy_alert([5, 7, 8], 10) == "ok"

def test_warning():
    assert energy_alert([12, 8, 9], 10) == "warning"

def test_critical():
    assert energy_alert([12, 15, 20], 10) == "critical"