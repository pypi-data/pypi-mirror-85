from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Union

from robinhood_commons.util.date_utils import convert_dates
from robinhood_commons.util.num_utils import convert_floats

EXAMPLES: List[Dict[str, Union[str, int, bool]]] = [
    {'ask_price': '6.700000', 'ask_size': 75, 'bid_price': '6.580000', 'bid_size': 10, 'last_trade_price': '6.740000',
     'last_extended_hours_trade_price': '6.560000', 'previous_close': '6.600000', 'adjusted_previous_close': '6.600000',
     'previous_close_date': '2020-06-15', 'symbol': 'MRO', 'trading_halted': False, 'has_traded': True,
     'last_trade_price_source': 'consolidated', 'updated_at': '2020-06-16T21:43:21Z',
     'instrument': 'https://api.robinhood.com/instruments/ab4f79fc-f84a-4f7b-8132-4f3e5fb38075/'}]


@dataclass(frozen=True)
class Quote:
    ask_price: float
    ask_size: int
    bid_price: float
    bid_size: int
    last_trade_price: float
    last_extended_hours_trade_price: float
    previous_close: float
    adjusted_previous_close: float
    previous_close_date: datetime
    symbol: str
    trading_halted: bool
    has_traded: bool
    last_trade_price_source: str
    instrument: str
    updated_at: datetime


def clean_quote(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data = convert_floats(data, ['ask_price', 'bid_price', 'last_trade_price', 'last_extended_hours_trade_price',
                                 'previous_close', 'adjusted_previous_close'])

    data = convert_dates(data, ['previous_close_date'])

    return data


def main() -> None:
    quotes: List[Quote] = [Quote(**clean_quote(e)) for e in EXAMPLES]
    print(quotes)


if __name__ == '__main__':
    main()
