from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Union

from robinhood_commons.util.date_utils import convert_dates
from robinhood_commons.util.num_utils import convert_floats

EXAMPLE: Dict[str, Union[str, int]] = dict(open='6.310000', high='6.785000', low='6.192000', volume='42124974.000000',
                                           average_volume_2_weeks='57372131.900000', average_volume='57372131.900000',
                                           high_52_weeks='14.700000', dividend_yield='2.610970',
                                           float='787326991.576000', low_52_weeks='3.020000',
                                           market_cap='4947353120.000000', pb_ratio='0.501716', pe_ratio='23.915100',
                                           shares_outstanding='790312000.000000',
                                           description='Marathon Oil Corp. engages in the exploration, production, and marketing of liquid hydrocarbons and natural gas. It operates through the following two segments: United States (U. S.) and International. The U. S. segment engages in oil and gas exploration, development and production activities in the U.S. The International segment engages in oil and gas development and production across international locations primarily in Equatorial Guinea and the United Kingdom. The company was founded in 1887 and is headquartered in Houston, TX.',
                                           instrument='https://api.robinhood.com/instruments/ab4f79fc-f84a-4f7b-8132-4f3e5fb38075/',
                                           ceo='Lee M. Tillman', headquarters_city='Houston',
                                           headquarters_state='Texas', sector='Energy Minerals',
                                           industry='Oil & Gas Production', num_employees=2000, year_founded=1887,
                                           symbol='MRO')


@dataclass(frozen=True)
class Fundamentals:
    open: float
    high: float
    low: float
    volume: float
    average_volume_2_weeks: float
    average_volume: float
    high_52_weeks: float
    dividend_yield: float
    float: float
    low_52_weeks: float
    market_cap: float
    pb_ratio: float
    pe_ratio: float
    shares_outstanding: float
    description: str
    instrument: str
    ceo: str
    headquarters_city: str
    headquarters_state: str
    sector: str
    industry: str
    num_employees: int
    year_founded: int
    symbol: str


def clean_fundamentals(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data = convert_floats(data,
                          ['open', 'high', 'low', 'volume', 'average_volume_2_weeks', 'average_volume', 'high_52_weeks',
                           'low_52_weeks', 'market_cap', 'shares_outstanding'])
    data = convert_floats(data, ['dividend_yield', 'float', 'pb_ratio', 'pe_ratio'], 0.00)
    data = convert_dates(data, ['datetime'])

    return data


def main() -> None:
    fundamentals = Fundamentals(**clean_fundamentals(EXAMPLE))
    print(fundamentals)


if __name__ == '__main__':
    main()
