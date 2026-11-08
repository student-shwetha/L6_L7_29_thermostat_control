import math


def _is_valid_number(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def target_temperature(mode, occupied, hour):

    if not isinstance(mode, str):
        raise TypeError("Mode must be a string")

    if mode not in ["home", "away", "sleep"]:
        raise ValueError("Mode must be home, away, or sleep")

    if not isinstance(occupied, bool):
        raise TypeError("Occupied must be True or False")

    if not isinstance(hour, int) or isinstance(hour, bool):
        raise TypeError("Hour must be an integer")

    if hour < 0 or hour > 23:
        raise ValueError("Hour must be between 0 and 23")

    if mode == "away":
        return 16

    if mode == "sleep":
        if hour < 6 or hour >= 22:
            return 18
        return 20

    if not occupied:
        return 18

    if 6 <= hour < 9:
        return 22

    if 17 <= hour < 22:
        return 21

    return 20


def hvac_action(current, target, outside):

    if not all(_is_valid_number(value) for value in [current, target, outside]):
        raise ValueError("Temperatures must be valid finite numbers")

    diff = target - current

    if abs(diff) < 1:
        return "idle"

    if diff > 0:
        if outside < 5:
            return "heat_boost"
        return "heat"

    if outside > 30:
        return "cool_boost"

    return "cool"


def energy_alert(readings, limit):

    if not isinstance(readings, (list, tuple)):
        raise TypeError("Readings must be a list or tuple")

    if len(readings) == 0:
        raise ValueError("Readings cannot be empty")

    if not all(_is_valid_number(reading) for reading in readings):
        raise ValueError("Every reading must be a valid finite number")

    if not _is_valid_number(limit):
        raise ValueError("Limit must be a valid finite number")

    over = 0

    for reading in readings:
        if reading > limit:
            over += 1

    if over == 0:
        return "ok"

    if over * 2 > len(readings):
        return "critical"

    return "warning"


if __name__ == "__main__":
    print("THERMOSTAT CONTROL SYSTEM")
    print("-------------------------")

    print("Target Temperature:",
          target_temperature("home", True, 8))

    print("HVAC Action:",
          hvac_action(18, 22, 3))

    print("Energy Alert:",
          energy_alert([10, 20, 30, 40], 25))