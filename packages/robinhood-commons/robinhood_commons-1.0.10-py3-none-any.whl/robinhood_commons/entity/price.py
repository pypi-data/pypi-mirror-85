from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Optional

from robinhood_commons.util.num_utils import convert_floats

EXAMPLE: Dict[str, str] = {'currency_id': '1072fc76-1862-41ab-82c2-485837590762', 'currency_code': 'USD',
                           'amount': '33.53'}


@dataclass(frozen=True)
class Price:
    amount: float
    currency_code: Optional[str] = None
    currency_id: Optional[str] = None


def clean_price(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data = convert_floats(data, ['amount'])

    return data


def main() -> None:
    execution = Price(**clean_price(EXAMPLE))
    print(execution)


if __name__ == '__main__':
    main()
