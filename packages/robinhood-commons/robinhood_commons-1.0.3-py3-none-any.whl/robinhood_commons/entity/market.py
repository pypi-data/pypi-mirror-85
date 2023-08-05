from dataclasses import dataclass
from typing import Dict

EXAMPLE: Dict[str, str] = {'url': 'https://api.robinhood.com/markets/IEXG/',
                           'todays_hours': 'https://api.robinhood.com/markets/IEXG/hours/2020-06-16/', 'mic': 'IEXG',
                           'operating_mic': 'IEXG', 'acronym': 'IEX', 'name': 'IEX Market', 'city': 'New York',
                           'country': 'US - United States of America', 'timezone': 'US/Eastern',
                           'website': 'www.iextrading.com'}


@dataclass(frozen=True)
class Market:
    url: str
    todays_hours: str
    mic: str
    operating_mic: str
    acronym: str
    name: str
    city: str
    country: str
    timezone: str
    website: str


def main() -> None:
    market = Market(**EXAMPLE)
    print(market)


if __name__ == '__main__':
    main()
