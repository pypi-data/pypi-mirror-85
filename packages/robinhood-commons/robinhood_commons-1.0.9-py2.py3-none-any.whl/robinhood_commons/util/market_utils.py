from datetime import datetime, time, timedelta
from robinhood_commons.util.date_utils import BASE_TZ, is_holiday, is_weekend, to_est


PRE_MARKET_OPEN_TIME: time = time(hour=8, minute=30, second=0, microsecond=0)
OPEN_TIME: time = time(hour=9, minute=30, second=0, microsecond=0)
CLOSE_TIME: time = time(hour=16, minute=0, second=0, microsecond=0)
POST_MARKET_CLOSE_TIME: time = time(hour=6, minute=0, second=0, microsecond=0)
MARKET_CLOSING_WINDOW: int = 3


def is_market_open(a_time: datetime = to_est()) -> bool:
    return True if in_market_time_window(a_time) and not is_holiday(a_time) and not is_weekend(a_time) else False


def in_market_time_window(a_time: datetime = to_est()) -> bool:
    # If in the 0930-1600 range
    return True if (not in_pre_market_time_window(a_time) and not in_post_market_time_window(a_time)) else False


def in_pre_market_time_window(a_time: datetime = to_est()) -> bool:
    # Before 09:30 range
    return True if a_time.time() < OPEN_TIME else False


def in_post_market_time_window(a_time: datetime = to_est()) -> bool:
    # After 16:00 range
    return True if a_time.time() > CLOSE_TIME else False


# Extended hours methods...
def is_extended_hours_market_open(a_time: datetime = to_est()) -> bool:
    return True if in_extended_hours_market_time_window(a_time) and not is_holiday(a_time) and not is_weekend(
        a_time) else False


def in_extended_hours_market_time_window(a_time: datetime = to_est()) -> bool:
    # If in the 0830-1800 range
    return True if (
                not in_pre_extended_hours_market_time_window(a_time) and not in_post_extended_hours_market_time_window(
            a_time)) else False


def in_pre_extended_hours_market_time_window(a_time: datetime = to_est()) -> bool:
    # After 08:30, but before 09:30
    return True if PRE_MARKET_OPEN_TIME < a_time.time() < OPEN_TIME else False


def in_post_extended_hours_market_time_window(a_time: datetime = to_est()) -> bool:
    # After 16:00, but before 18:00
    return True if CLOSE_TIME < a_time.time() < POST_MARKET_CLOSE_TIME else False


def time_til_close(a_date: datetime = to_est()) -> timedelta:
    if not is_market_open(a_date):
        return timedelta.max

    close_time = BASE_TZ.localize(datetime.combine(date=a_date.date(), time=CLOSE_TIME))
    return close_time - a_date


def within_close_threshold() -> bool:
    time_left = time_til_close(a_date=to_est())
    return time_left < timedelta(minutes=MARKET_CLOSING_WINDOW)


def time_next_open(a_time: datetime = to_est()) -> datetime:
    """Given a time, when will the market be open again?

    Args:
        a_time: a time

    Returns: The next time the market will be open
    """
    if is_market_open(a_time):
        return a_time

    # Calculate days to skip for holidays and weekends based on that start of that day
    n = a_time.replace(hour=0, minute=0, second=0, microsecond=0)
    while is_weekend(n) or is_holiday(n):
        n += timedelta(days=1)

    # If after market close, add a day
    if in_post_market_time_window(a_time):
        n += timedelta(days=1)

    # Add the opening time
    return BASE_TZ.localize(datetime.combine(n.date(), OPEN_TIME))


def time_til_open(a_date: datetime = to_est()) -> timedelta:
    """Given on a time, how long will it be until the market will be open next

    Args:
        a_date: a datetime

    Returns: offset time of when it'll be open
    """
    return time_next_open(a_date) - a_date


if __name__ == '__main__':
    print(is_market_open())
    print(time_next_open(datetime.now(BASE_TZ)))
    print(time_til_open(datetime.now(BASE_TZ)))
    print(time_til_close(datetime.now(BASE_TZ)))
