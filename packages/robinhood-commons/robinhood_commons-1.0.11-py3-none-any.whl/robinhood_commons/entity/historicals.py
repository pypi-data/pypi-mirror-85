from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Union

from robinhood_commons.util.date_utils import convert_dates
from robinhood_commons.util.num_utils import convert_floats

EXAMPLES: List[Dict[str, Union[str, int, bool]]] = [
    {'begins_at': '2020-06-08T13:30:00Z', 'open_price': '8.430000', 'close_price': '8.130000', 'high_price': '8.440000',
     'low_price': '7.850000', 'volume': 3377827, 'session': 'reg', 'interpolated': False, 'symbol': 'MRO'},
    {'begins_at': '2020-06-08T13:40:00Z', 'open_price': '8.112100', 'close_price': '8.130000', 'high_price': '8.190000',
     'low_price': '8.020000', 'volume': 1929658, 'session': 'reg', 'interpolated': False, 'symbol': 'MRO'}]


@dataclass(frozen=True)
class Historicals:
    begins_at: datetime
    open_price: float
    close_price: float
    high_price: float
    low_price: float
    volume: int
    session: str
    interpolated: bool
    symbol: str


def clean_historicals(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data = convert_floats(data, ['open_price', 'close_price', 'high_price', 'low_price'])
    data = convert_dates(data, ['begins_at'])

    return data


def main() -> None:
    historicals = [Historicals(**clean_historicals(i)) for i in EXAMPLES]
    print(historicals)


if __name__ == '__main__':
    main()
