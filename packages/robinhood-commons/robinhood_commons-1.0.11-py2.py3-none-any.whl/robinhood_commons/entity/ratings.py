from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List

from robinhood_commons.entity.printable import Printable
from robinhood_commons.util.date_utils import convert_dates

EXAMPLE: Dict[str, Any] = {'summary': {'num_buy_ratings': 7, 'num_hold_ratings': 18, 'num_sell_ratings': 3},
                           'ratings': [{'published_at': '2020-06-06T00:55:32Z', 'type': 'buy',
                                        'text': b'Marathon was one of the first U.S. shale companies to establish a track record for free cash flow generation.'},
                                       {'published_at': '2020-06-06T00:55:32Z', 'type': 'buy',
                                        'text': b'Marathon\'s acreage in the Bakken and Eagle Ford plays overlaps the juiciest "sweet spots" and enables the firm to deliver initial production rates far above the respective averages.'},
                                       {'published_at': '2020-06-06T00:55:32Z', 'type': 'buy',
                                        'text': b'Holding acreage in the top four liquids-rich shale plays enables management to sidestep transport bottlenecks and avoid overpaying for equipment and services in areas experiencing temporary demand surges. '},
                                       {'published_at': '2020-06-06T00:55:32Z', 'type': 'sell',
                                        'text': b"Marathon's Delaware Basin acreage is relatively fragmented, limiting the scope to boost profitability by utilizing longer laterals."},
                                       {'published_at': '2020-06-06T00:55:32Z', 'type': 'sell',
                                        'text': b'Not all of Marathon\'s acreage is ideally located--well productivity could decline when the firm runs out of drilling opportunities in "sweet spots."'},
                                       {'published_at': '2020-06-06T00:55:32Z', 'type': 'sell',
                                        'text': b'Marathon is unable to earn its cost of capital due to prior investments in higher-cost resources.'}],
                           'instrument_id': 'ab4f79fc-f84a-4f7b-8132-4f3e5fb38075',
                           'ratings_published_at': '2020-06-06T00:55:32Z'}


@dataclass(frozen=True)
class Ratings:
    summary: Dict[RatingType, int]
    ratings: List[Rating]
    instrument_id: str
    ratings_published_at: datetime


@dataclass(frozen=True)
class Rating:
    published_at: datetime
    type: RatingType
    text: str


class RatingType(Printable, Enum):
    BUY = auto()
    SELL = auto()
    HOLD = auto()

    @staticmethod
    def to_enum(value: str) -> RatingType:
        v: str = value.upper()
        return RatingType[v]


def clean_ratings(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data['ratings'] = [Rating(**clean_rating(r)) for r in data['ratings']]

    # Map summary keys to RatingType enum
    mapping = {'num_buy_ratings': RatingType.BUY,
               'num_hold_ratings': RatingType.HOLD,
               'num_sell_ratings': RatingType.SELL}

    summary: Dict[RatingType, int] = {}
    for summary_key, value in data['summary'].items():
        if summary_key in mapping.keys():
            summary[mapping[summary_key]] = value
        else:
            print(f"WARNING: Rating Summary Type: {summary_key} not found.")
    data['summary'] = summary

    data = convert_dates(data, ['ratings_published_at'])

    return data


def clean_rating(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data['type'] = RatingType.to_enum(data['type'])

    data = convert_dates(data, ['published_at'])

    return data


def main() -> None:
    ratings = Ratings(**EXAMPLE)
    print(ratings)


if __name__ == '__main__':
    main()
