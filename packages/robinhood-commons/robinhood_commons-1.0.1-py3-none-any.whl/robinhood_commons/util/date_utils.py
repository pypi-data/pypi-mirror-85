from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any, Dict, List

import pytz
from dateutil import parser
from holidays.countries.united_states import US as US_holidays

BASE_TZ = pytz.timezone(zone='US/Eastern')
UPDATED_AT: str = 'updated_at'
CREATED_AT: str = 'created_at'


def to_est() -> datetime:
    return datetime.now(tz=BASE_TZ)


def date_parse(date_str: str) -> datetime:
    return parser.isoparse(date_str) if date_str is not None else None


def to_date(date_str: str) -> datetime:
    return datetime.strptime(date_string=date_str, format='%Y%m%d')


def date_to_str(a_date: datetime = to_est()) -> str:
    """ Provides a day representation.

    Returns:
        A year, month, and day string
    """
    return a_date.strftime('%Y%m%d')


def str_to_iso_8601(a_str: str) -> datetime:
    return datetime.strptime(a_str, '%Y-%m-%d %H:%M:%S.%f')


def str_to_datetime(a_str: str = to_est()) -> datetime:
    return datetime.strptime(a_str, date_time_format())
    # return datetime.strptime(date_string=a_str, format=date_time_format())


def datetime_to_str(a_date: datetime = to_est()) -> str:
    """ Provides a minute representation.

    Returns:
        A year, month, day, hour, minute string
    """
    return a_date.strftime(date_time_format())


def second_to_str(a_date: datetime = to_est()) -> str:
    """ Provides a second representation.

    Returns:
        A year, month, day, hour, minute, second string
    """
    return a_date.strftime('%Y%m%d%H%M%S')


def time_to_str(a_date: datetime = to_est()) -> str:
    """Provides a time string based representation.

    Args:
        a_date: a date

    Returns:
        A hour, minute string
    """
    return a_date.strftime('%H%M')


def readable_datetime_to_str(a_date: datetime = to_est()) -> str:
    """ Provides a minute representation.

    Returns: a year, month, day, hour, minute string
    """
    return a_date.strftime('%Y-%m-%d %H:%M:00')


def readable_date_to_str(a_date: datetime = to_est()) -> str:
    """ Provides a minute representation.

    Returns: a year, month, day
    """
    return a_date.strftime('%Y-%m-%d')


def timeoffset_as_str(seconds: int, a_datetime=to_est()) -> str:
    """ Provides a minute representation.

    Returns: a year, month, day, hour, minute string
    """
    return time_to_str(a_datetime - timedelta(seconds=seconds))


def date_time_format() -> str:
    return '%Y%m%d%H%M'


def time_floor(a_date: datetime = to_est(), window: int = 10) -> datetime:
    return a_date - timedelta(minutes=a_date.minute % window,
                              seconds=a_date.second,
                              microseconds=a_date.microsecond)


def convert_dates(input_data: Dict[str, Any], keys: List[str] = []) -> Dict[str, Any]:
    all_keys = keys + [UPDATED_AT, CREATED_AT]

    if any(k in input_data for k in all_keys):
        data = deepcopy(input_data)

        for key in all_keys:
            if key in input_data:
                data[key] = date_parse(data[key])

        return data

    return input_data


def is_holiday(a_time: datetime = to_est()) -> bool:
    return True if a_time.strftime('%Y-%m-%d') in US_holidays() else False


def is_weekend(a_time: datetime = to_est()) -> bool:
    return True if a_time.date().weekday() > 4 else False


if __name__ == '__main__':
    print(datetime_to_str())
