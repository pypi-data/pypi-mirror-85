from typing import Any, Optional
from typing import Dict, List, Union

import pandas_datareader.data as data_reader
import robin_stocks as rh
from pandas import DataFrame

from robinhood_commons.dao.robinhood_base_dao import RobinhoodBaseDao
from robinhood_commons.dao.stock_dao import StockDao
from robinhood_commons.dao.user_dao import UserDao
from robinhood_commons.entity.direction import Direction
from robinhood_commons.entity.earnings import Earnings, clean_earnings
from robinhood_commons.entity.fundamentals import Fundamentals, clean_fundamentals
from robinhood_commons.entity.historicals import Historicals, clean_historicals
from robinhood_commons.entity.market import Market
from robinhood_commons.entity.mover import Mover, clean_mover
from robinhood_commons.entity.news import News, clean_news
from robinhood_commons.entity.offer import Offers, clean_offers
from robinhood_commons.entity.popularity import Popularity
from robinhood_commons.entity.quote import Quote, clean_quote
from robinhood_commons.entity.ratings import Ratings, clean_ratings
from robinhood_commons.entity.user import User
from robinhood_commons.util.constants import MAIN_EMAIL


NUM_ATTEMPTS: int = 10


class StockDaoImpl(StockDao, RobinhoodBaseDao):

    def get_symbol(self, url: str) -> str:
        return rh.get_symbol_by_url(url=url)

    # TODO: Not in use...use older API
    def get_historicals(self, symbol: str) -> List[Historicals]:
        return [Historicals(**clean_historicals(i)) for i in rh.get_historicals(inputSymbols=symbol)]

    def stock_prices(self, symbol: str) -> DataFrame:
        dataframe: DataFrame = data_reader.DataReader(name=symbol, data_source='yahoo')
        dataframe = dataframe.reset_index()
        return dataframe

    def latest_price(self, symbol: str) -> Optional[float]:
        attempts: int = 0
        while attempts < NUM_ATTEMPTS:
            try:
                value: str = rh.get_latest_price(inputSymbols=symbol)
                return float(value[0]) if value is not None and len(value) > 0 and value[0] is not None else None
            except ConnectionResetError as inst:
                attempts += 1
                StockDaoImpl(UserDao.get_user_by_email(MAIN_EMAIL))
                print(f'Attempt {attempts} for {symbol}: {inst}')

    def get_markets(self) -> List[Market]:
        return [Market(**m) for m in rh.get_markets()]

    def get_offers(self, symbol: str) -> Optional[Offers]:
        offers: Dict[str, Any] = rh.get_pricebook_by_symbol(symbol=symbol)
        return Offers(**clean_offers(offers)) if offers is not None else None

    def get_quotes(self, symbol: str) -> List[Quote]:
        return [Quote(**clean_quote(q)) for q in rh.get_quotes(inputSymbols=symbol)]

    def get_ratings(self, symbol: str) -> Ratings:
        return Ratings(**clean_ratings(rh.get_ratings(symbol=symbol)))

    def get_earnings(self, symbol: str) -> List[Earnings]:
        return [Earnings(**clean_earnings(e)) for e in rh.get_earnings(symbol=symbol)]

    def get_fundamentals(self, symbol: str) -> Fundamentals:
        return Fundamentals(**clean_fundamentals(rh.get_fundamentals(inputSymbols=symbol)[0]))

    def get_sp500_up_movers(self) -> List[Mover]:
        return [Mover(**clean_mover(m)) for m in rh.get_top_movers_sp500(direction=Direction.UP.value())]

    def get_sp500_down_movers(self) -> List[Mover]:
        return [Mover(**clean_mover(m)) for m in rh.get_top_movers_sp500(direction=Direction.DOWN.value())]

    def get_movers(self) -> List[Mover]:
        return [Mover(**clean_mover(m)) for m in rh.get_top_movers()]

    # TODO: Not in use...use older API
    def get_popularity(self, symbol: str) -> Popularity:
        popularity: Dict[str, Union[str, int]] = rh.get_popularity(symbol=symbol)
        popularity['symbol'] = rh.get_symbol_by_url(url=popularity['instrument'])
        return Popularity(**popularity)

    def get_news(self, symbol: str) -> List[News]:
        return [News(**clean_news(n)) for n in rh.get_news(symbol=symbol)]


if __name__ == '__main__':
    user: User = UserDao.get_user_by_email(email=MAIN_EMAIL)
    dao = StockDaoImpl(user)
    print(dao.get_fundamentals(symbol='AMZN'))
    print(dao.stock_prices(symbol='AMZN'))
    print(dao.stock_prices(symbol='AMZN').columns)


    # print(dao.latest_price(symbol='AMZN'))
    # print(dao.get_fundamentals(symbol='AMZN'))
    # print(dao.get_earnings(symbol='AMZN'))
    # print(dao.get_news(symbol='AMZN'))
    # print(dao.get_ratings(symbol='AMZN'))
    # print(dao.get_quotes(symbol='AMZN'))
    # print(dao.get_markets())
    # print(dao.get_offers(symbol='AMZN'))
