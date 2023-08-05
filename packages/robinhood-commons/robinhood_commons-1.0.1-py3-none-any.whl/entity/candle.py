from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from json import JSONEncoder
from typing import Dict, List, Union


@dataclass
class Candle:
    cu: float = 0.0
    o: float = 0.0
    c: float = 0.0
    h: float = 0.0
    l: float = 0.0
    dh: float = 0.0
    dl: float = 0.0
    do: float = 0.0


def to_picklable(candles: Dict[str, Dict[str, Candle]]) -> List[Dict[str, Union[str, Candle]]]:
    data = []

    for symbol, candle_data in candles.items():
        cdata = deepcopy(candle_data)
        cdata['s'] = symbol
        data.append(cdata)
    return data


def from_picklable(candles: List[Dict[str, Union[str, Candle]]]) -> Dict[str, Dict[str, Candle]]:
    data = defaultdict(lambda: defaultdict(Candle))

    for candle_data in candles:
        symbol = candle_data['s']
        del candle_data['s']

        data[symbol] = candle_data
    return data


class CandleEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def main() -> None:
    candle = Candle(cu=1.0, o=1.0, c=2.0, h=4.0, l=0.5, dh=1.0, dl=0.5, do=0.0)
    print(candle)


if __name__ == '__main__':
    main()
