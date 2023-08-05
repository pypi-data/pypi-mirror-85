from dataclasses import dataclass
from typing import Dict, Union

EXAMPLE: Dict[str, Union[str, int]] = {
    'instrument': 'https://api.robinhood.com/instruments/ab4f79fc-f84a-4f7b-8132-4f3e5fb38075/',
    'num_open_positions': 206842, 'symbol': 'MRO'}


@dataclass(frozen=True)
class Popularity:
    instrument: str
    num_open_positions: int
    symbol: str


def main() -> None:
    popularity = Popularity(**EXAMPLE)
    print(popularity)


if __name__ == '__main__':
    main()
