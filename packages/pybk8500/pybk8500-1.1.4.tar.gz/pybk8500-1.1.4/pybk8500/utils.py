import re
import datetime


__all__ = ['parse_number', 'TIME_FORMATS', 'NUMBER_UNIT_REGEX', 'UNIT_CONVERT']


TIME_FORMATS = [
    '%I:%M:%S %p',     # '02:24:55 PM'
    '%I:%M:%S.%f %p',  # '02:24:55.000200 PM'
    '%I:%M %p',        # '02:24 PM'
    '%H:%M:%S',        # '14:24:55'
    '%H:%M:%S.%f',     # '14:24:55.000200'
    '%H:%M',           # '14:24'
    ]


NUMBER_UNIT_REGEX = re.compile(r'^(?P<num>\d*\.?\d*) ?(?P<unit>\w*)')
UNIT_CONVERT = {
    'T': 10**12, 'Terra': 10**12,
    'G': 10**9, 'Giga': 10**9,
    'M': 10**6, 'Mega': 10**6,
    'k': 10**3, 'kilo': 10**3,
    'c': 10**-2, 'centi': 10**-2,
    'm': 10**-3, 'milli': 10**-3,
    'µ': 10**-6, 'micro': 10**-6,
    'n': 10**-9, 'nano': 10**-9,
    'p': 10**-12, 'pico': 10**-12,
    'min': 60, 'minute': 60, 'minutes': 60,
    'h': 60*60, 'hour': 60*60, 'hours': 60*60,
    }


FIRST_DT = datetime.datetime(1970, 1, 1)
ZERO_DT = datetime.datetime(1900, 1, 1)


def parse_number(value):
    """Try parsing the value into a number.

    If units are given convert to the base unit. If HH:MM:SS then return the number of seconds.
    """
    if ":" in str(value):
        # Check for date time
        for fmt in TIME_FORMATS:
            try:
                dt = datetime.datetime.strptime(value, fmt)
                if dt.year == ZERO_DT.year:
                    return (dt - ZERO_DT).total_seconds()
                else:
                    return (dt - FIRST_DT).total_seconds()
            except (ValueError, TypeError, Exception):
                pass

    elif '0x' in str(value):
        # Check hex value
        try:
            return int(value, 16)
        except (ValueError, TypeError, Exception):
            pass

    # Check regex
    d = NUMBER_UNIT_REGEX.match(value).groupdict()
    num = d['num']
    unit = d['unit']
    if not num:
        return value

    # Convert to number
    try:
        num = int(num)
    except (ValueError, TypeError, Exception):
        try:
            num = float(num)
        except (ValueError, TypeError, Exception):
            return num  # Cannot get a real number

    # Find unit converter
    for name, scale in UNIT_CONVERT.items():
        if unit.startswith(name):
            try:
                return num * scale
            except (ValueError, TypeError, Exception):
                pass

    return num
