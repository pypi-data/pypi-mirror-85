from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List

from robinhood_commons.entity.price import Price, clean_price
from robinhood_commons.entity.printable import Printable
from robinhood_commons.util.date_utils import convert_dates

EXAMPLE: Dict[str, List[Dict[Any]]] = {
    'asks': [{'side': 'ask', 'price': {'amount': '6.730000', 'currency_code': 'USD'}, 'quantity': 125},
             {'side': 'ask', 'price': {'amount': '6.800000', 'currency_code': 'USD'}, 'quantity': 500},
             {'side': 'ask', 'price': {'amount': '6.810000', 'currency_code': 'USD'}, 'quantity': 22},
             {'side': 'ask', 'price': {'amount': '6.850000', 'currency_code': 'USD'}, 'quantity': 1500},
             {'side': 'ask', 'price': {'amount': '6.860000', 'currency_code': 'USD'}, 'quantity': 10000},
             {'side': 'ask', 'price': {'amount': '6.990000', 'currency_code': 'USD'}, 'quantity': 200},
             {'side': 'ask', 'price': {'amount': '7.000000', 'currency_code': 'USD'}, 'quantity': 5152},
             {'side': 'ask', 'price': {'amount': '7.010000', 'currency_code': 'USD'}, 'quantity': 84},
             {'side': 'ask', 'price': {'amount': '7.100000', 'currency_code': 'USD'}, 'quantity': 500},
             {'side': 'ask', 'price': {'amount': '7.150000', 'currency_code': 'USD'}, 'quantity': 76},
             {'side': 'ask', 'price': {'amount': '7.190000', 'currency_code': 'USD'}, 'quantity': 6980},
             {'side': 'ask', 'price': {'amount': '7.200000', 'currency_code': 'USD'}, 'quantity': 800},
             {'side': 'ask', 'price': {'amount': '7.210000', 'currency_code': 'USD'}, 'quantity': 400},
             {'side': 'ask', 'price': {'amount': '7.240000', 'currency_code': 'USD'}, 'quantity': 250},
             {'side': 'ask', 'price': {'amount': '7.250000', 'currency_code': 'USD'}, 'quantity': 950},
             {'side': 'ask', 'price': {'amount': '7.400000', 'currency_code': 'USD'}, 'quantity': 100},
             {'side': 'ask', 'price': {'amount': '7.470000', 'currency_code': 'USD'}, 'quantity': 200},
             {'side': 'ask', 'price': {'amount': '7.500000', 'currency_code': 'USD'}, 'quantity': 300},
             {'side': 'ask', 'price': {'amount': '7.650000', 'currency_code': 'USD'}, 'quantity': 2000},
             {'side': 'ask', 'price': {'amount': '7.750000', 'currency_code': 'USD'}, 'quantity': 655},
             {'side': 'ask', 'price': {'amount': '8.000000', 'currency_code': 'USD'}, 'quantity': 800},
             {'side': 'ask', 'price': {'amount': '8.080000', 'currency_code': 'USD'}, 'quantity': 975},
             {'side': 'ask', 'price': {'amount': '8.090000', 'currency_code': 'USD'}, 'quantity': 16000},
             {'side': 'ask', 'price': {'amount': '8.200000', 'currency_code': 'USD'}, 'quantity': 1000},
             {'side': 'ask', 'price': {'amount': '8.210000', 'currency_code': 'USD'}, 'quantity': 100},
             {'side': 'ask', 'price': {'amount': '8.280000', 'currency_code': 'USD'}, 'quantity': 1233},
             {'side': 'ask', 'price': {'amount': '8.300000', 'currency_code': 'USD'}, 'quantity': 1400},
             {'side': 'ask', 'price': {'amount': '8.460000', 'currency_code': 'USD'}, 'quantity': 500},
             {'side': 'ask', 'price': {'amount': '8.500000', 'currency_code': 'USD'}, 'quantity': 120},
             {'side': 'ask', 'price': {'amount': '8.550000', 'currency_code': 'USD'}, 'quantity': 70},
             {'side': 'ask', 'price': {'amount': '8.780000', 'currency_code': 'USD'}, 'quantity': 520},
             {'side': 'ask', 'price': {'amount': '8.900000', 'currency_code': 'USD'}, 'quantity': 100},
             {'side': 'ask', 'price': {'amount': '9.000000', 'currency_code': 'USD'}, 'quantity': 50},
             {'side': 'ask', 'price': {'amount': '9.250000', 'currency_code': 'USD'}, 'quantity': 538},
             {'side': 'ask', 'price': {'amount': '9.500000', 'currency_code': 'USD'}, 'quantity': 215},
             {'side': 'ask', 'price': {'amount': '9.980000', 'currency_code': 'USD'}, 'quantity': 21499},
             {'side': 'ask', 'price': {'amount': '10.000000', 'currency_code': 'USD'}, 'quantity': 20010},
             {'side': 'ask', 'price': {'amount': '10.930000', 'currency_code': 'USD'}, 'quantity': 3},
             {'side': 'ask', 'price': {'amount': '12.000000', 'currency_code': 'USD'}, 'quantity': 2410},
             {'side': 'ask', 'price': {'amount': '12.250000', 'currency_code': 'USD'}, 'quantity': 300}],
    'bids': [{'side': 'bid', 'price': {'amount': '6.500000', 'currency_code': 'USD'}, 'quantity': 900},
             {'side': 'bid', 'price': {'amount': '6.420000', 'currency_code': 'USD'}, 'quantity': 60},
             {'side': 'bid', 'price': {'amount': '6.360000', 'currency_code': 'USD'}, 'quantity': 8000},
             {'side': 'bid', 'price': {'amount': '6.300000', 'currency_code': 'USD'}, 'quantity': 500},
             {'side': 'bid', 'price': {'amount': '6.200000', 'currency_code': 'USD'}, 'quantity': 500},
             {'side': 'bid', 'price': {'amount': '6.120000', 'currency_code': 'USD'}, 'quantity': 140},
             {'side': 'bid', 'price': {'amount': '6.000000', 'currency_code': 'USD'}, 'quantity': 110},
             {'side': 'bid', 'price': {'amount': '5.990000', 'currency_code': 'USD'}, 'quantity': 1669},
             {'side': 'bid', 'price': {'amount': '5.900000', 'currency_code': 'USD'}, 'quantity': 40},
             {'side': 'bid', 'price': {'amount': '5.540000', 'currency_code': 'USD'}, 'quantity': 1500},
             {'side': 'bid', 'price': {'amount': '5.500000', 'currency_code': 'USD'}, 'quantity': 190},
             {'side': 'bid', 'price': {'amount': '4.750000', 'currency_code': 'USD'}, 'quantity': 5},
             {'side': 'bid', 'price': {'amount': '4.100000', 'currency_code': 'USD'}, 'quantity': 200},
             {'side': 'bid', 'price': {'amount': '4.000000', 'currency_code': 'USD'}, 'quantity': 800},
             {'side': 'bid', 'price': {'amount': '3.500000', 'currency_code': 'USD'}, 'quantity': 800},
             {'side': 'bid', 'price': {'amount': '3.020000', 'currency_code': 'USD'}, 'quantity': 165},
             {'side': 'bid', 'price': {'amount': '3.000000', 'currency_code': 'USD'}, 'quantity': 255},
             {'side': 'bid', 'price': {'amount': '1.500000', 'currency_code': 'USD'}, 'quantity': 50}],
    'instrument_id': 'ab4f79fc-f84a-4f7b-8132-4f3e5fb38075', 'updated_at': '2020-06-16T17:22:36.399570266-04:00'}


@dataclass(frozen=True)
class Offers:
    asks: List[Offer]
    bids: List[Offer]
    instrument_id: str
    updated_at: datetime


@dataclass(frozen=True)
class Offer:
    side: str
    price: Price
    quantity: int


class OfferType(Printable, Enum):
    ASK = auto()
    BID = auto()

    @staticmethod
    def to_enum(value: str) -> OfferType:
        v: str = value.upper()
        return OfferType[v]


def clean_offers(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data['asks'] = [Offer(**clean_offer(o)) for o in data['asks']]
    data['bids'] = [Offer(**clean_offer(o)) for o in data['bids']]

    data = convert_dates(data)

    return data


def clean_offer(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data['price'] = Price(**clean_price(data['price']))

    return data


def main() -> None:
    offers: Offers = Offers(**clean_offers(EXAMPLE))
    print(offers)


if __name__ == '__main__':
    main()
