from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from robinhood_commons.util.date_utils import convert_dates
from robinhood_commons.util.num_utils import convert_floats

EXAMPLE: Dict[str, str] = {
    'instrument_url': 'https://api.robinhood.com/instruments/3c582020-d702-4c8a-b69a-4df7c57d0f49/', 'symbol': 'PVH',
    'updated_at': '2020-06-12T21:16:58.252906Z',
    'price_movement': {'market_hours_last_movement_pct': '-5.90', 'market_hours_last_price': '49.6100'},
    'description': 'PVH Corp. engages in the design and marketing of branded dress shirts, neckwear, sportswear, jeans wear, intimate apparel, swim products, handbags, footwear, and other related products. It operates through the following segments: Calvin Klein North America, Calvin Klein International, Tommy Hilfiger North America, Tommy Hilfiger International, Heritage Brands Wholesale, and Heritage Brands Retail. The Calvin Klein North America and Calvin Klein International segment operates in North America; and Europe, Asia, and Brazil respectively. It sells its products under the brand names CALVIN KLEIN 205 W39 NYC, CK Calvin Klein, and CALVIN KLEIN. The Tommy Hilfiger North America and Tommy Hilfiger International segment wholesales in North America; and Europe and China respectively. It consists of Tommy Hilfiger, Hilfiger Denim, Hilfiger Collection, and Tommy Hilfiger Tailored brands. The Heritage Brands Wholesale segment markets its products to department, chain, and specialty stores, digital commerce sites operated by select wholesale partners and pure play digital commerce retailers in North America. The Heritage Brands Retail segment manages retail stores, primarily located in outlet centers throughout the United States and Canada. PVH was founded in 1881 and is headquartered in New York, NY.'}


@dataclass(frozen=True)
class Mover:
    instrument_url: str
    symbol: str
    updated_at: datetime
    price_movement: PriceMovement
    description: str


@dataclass(frozen=True)
class PriceMovement:
    market_hours_last_movement_pct: float
    market_hours_last_price: float


def clean_mover(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data['price_movement'] = PriceMovement(**clean_price_movement(data['price_movement']))

    data = convert_dates(data)

    return data


def clean_price_movement(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data = convert_floats(data, ['market_hours_last_movement_pct', 'market_hours_last_price'])

    return data


def main() -> None:
    mover = Mover(**clean_mover(EXAMPLE))
    print(mover)


if __name__ == '__main__':
    main()
