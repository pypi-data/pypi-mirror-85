from abc import ABC, abstractmethod
from typing import List, Optional

from pandas import DataFrame

from robinhood_commons.entity.earnings import Earnings
from robinhood_commons.entity.fundamentals import Fundamentals
from robinhood_commons.entity.historicals import Historicals
from robinhood_commons.entity.market import Market
from robinhood_commons.entity.mover import Mover
from robinhood_commons.entity.news import News
from robinhood_commons.entity.offer import Offers
from robinhood_commons.entity.popularity import Popularity
from robinhood_commons.entity.quote import Quote
from robinhood_commons.entity.ratings import Ratings


class StockDao(ABC):

    @abstractmethod
    def get_symbol(self, url: str) -> str:
        pass

    @abstractmethod
    def get_historicals(self, symbol: str) -> List[Historicals]:
        pass

    @abstractmethod
    def stock_prices(self, symbol: str) -> DataFrame:
        pass

    @abstractmethod
    def latest_price(self, symbol: str) -> Optional[float]:
        pass

    @abstractmethod
    def get_markets(self) -> List[Market]:
        pass

    @abstractmethod
    def get_earnings(self, symbol: str) -> List[Earnings]:
        pass

    @abstractmethod
    def get_fundamentals(self, symbol: str) -> Fundamentals:
        pass

    @abstractmethod
    def get_sp500_up_movers(self) -> List[Mover]:
        pass

    @abstractmethod
    def get_sp500_down_movers(self) -> List[Mover]:
        pass

    @abstractmethod
    def get_movers(self) -> List[Mover]:
        pass

    @abstractmethod
    def get_popularity(self, symbol: str) -> Popularity:
        pass

    @abstractmethod
    def get_news(self, symbol: str) -> List[News]:
        pass

    @abstractmethod
    def get_offers(self, symbol: str) -> Optional[Offers]:
        pass

    @abstractmethod
    def get_quotes(self, symbol: str) -> List[Quote]:
        pass

    @abstractmethod
    def get_ratings(self, symbol: str) -> Ratings:
        pass
