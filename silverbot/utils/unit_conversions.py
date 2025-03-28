"""
Utilities that convert units.
"""


def to_celsius(kelvins: float):
    """
    Returns kelvins converted to celsius.
    """
    return round(kelvins - 273.15)


def to_fahrenheit(kelvins: float):
    """
    Returns kelvins converted to fahrenheit.
    """
    return round((kelvins - 273.15) * 1.8 + 32)
