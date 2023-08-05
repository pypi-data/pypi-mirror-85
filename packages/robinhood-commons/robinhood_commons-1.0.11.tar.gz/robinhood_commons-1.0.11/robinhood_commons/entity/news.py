from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from robinhood_commons.util.date_utils import convert_dates

EXAMPLES: List[Dict[str, str]] = [{'api_source': 'cnbc', 'author': '', 'num_clicks': 0,
                                   'preview_image_url': 'https://images.robinhood.com/SFqNLCoF0LN_p9jvvLLKKhBWzSM/aHR0cHM6Ly9pbWFnZXMucm9iaW5ob29kLmNvbS9DaEVMNWZvcXJKaXZxYmhoZ0szS3hpcjJBdWcvYUhSMGNITTZMeTlwYldGblpTNWpibUpqWm0wdVkyOXRMMkZ3YVM5Mk1TOXBiV0ZuWlM4eE1EWTFOelEyTWpjdE1UVTVNVGt3T0RVd056QTROWFJ5ZFcxd0xtcHdaejkyUFRFMU9URTVNRGcxTmpF',
                                   'published_at': '2020-06-16T12:35:00Z',
                                   'relay_url': 'https://news.robinhood.com/9c430c3c-d458-3a61-960a-e1ee4ead69d0/',
                                   'source': 'CNBC', 'summary': '',
                                   'title': 'Dow futures soar higher by 800 points after a record retail sales jump',
                                   'updated_at': '2020-06-16T12:45:16.285881Z',
                                   'url': 'https://www.cnbc.com/2020/06/15/stock-market-futures-open-to-close-news.html',
                                   'uuid': '9c430c3c-d458-3a61-960a-e1ee4ead69d0',
                                   'related_instruments': ['8f92e76f-1e0e-4478-8580-16a6ffcfaef5',
                                                           'bab3b12b-4216-4b01-b2d8-9587ee5f41cf'],
                                   'preview_text': 'Futures contracts tied to the major U.S. stock indexes rose sharply early Tuesday, pointing to further gains after a big comeback in the previous session.\n\nDow',
                                   'currency_id': 'None'}, {'api_source': 'cnbc', 'author': '', 'num_clicks': 0,
                                                            'preview_image_url': 'https://images.robinhood.com/8kZOCFXHoWLpCqTxCSugAp4Z-uI/aHR0cHM6Ly9pbWFnZXMucm9iaW5ob29kLmNvbS9jZ2tfNzNMeXVUZVFZUHVuYnBNY1ZCWkNjOHcvYUhSMGNITTZMeTlwYldGblpTNWpibUpqWm0wdVkyOXRMMkZ3YVM5Mk1TOXBiV0ZuWlM4eE1EWTFOemM0TVRBdE1UVTVNakl4T1RJNE1EVTRNbWRsZEhSNWFXMWhaMlZ6TFRFeU1UZzBORGd4TWpjdWFuQmxaejkyUFRFMU9USXlNVGt6TkRr',
                                                            'published_at': '2020-06-15T13:30:00Z',
                                                            'relay_url': 'https://news.robinhood.com/e7822901-8b45-306f-b1f5-91e8cfb72ea4/',
                                                            'source': 'CNBC', 'summary': '',
                                                            'title': 'Dow drops more than 600 points as Wall Street adds to last week’s sharp losses',
                                                            'updated_at': '2020-06-15T13:36:58.465376Z',
                                                            'url': 'https://www.cnbc.com/2020/06/14/stock-market-futures-open-to-close-news.html',
                                                            'uuid': 'e7822901-8b45-306f-b1f5-91e8cfb72ea4',
                                                            'related_instruments': [
                                                                'bab3b12b-4216-4b01-b2d8-9587ee5f41cf',
                                                                '8f92e76f-1e0e-4478-8580-16a6ffcfaef5'],
                                                            'preview_text': 'Stocks dropped on Monday as investors grapple with signs of a second wave of coronavirus cases as the U.S. economy reopens.\n\nThe Dow Jones Industrial Average fe',
                                                            'currency_id': 'None'},
                                  {'api_source': 'cnbc', 'author': '', 'num_clicks': 0,
                                   'preview_image_url': 'https://images.robinhood.com/FIcrAly-yZks69vv-0eCb6cIrL4/aHR0cHM6Ly9pbWFnZXMucm9iaW5ob29kLmNvbS9kU2Zaa0gxbzdSdFFWTWliRVJSTGZiYzAtR3MvYUhSMGNITTZMeTlwYldGblpTNWpibUpqWm0wdVkyOXRMMkZ3YVM5Mk1TOXBiV0ZuWlM4eE1EWTFOelUyTlRRdE1UVTVNVGs0TXpjNE1UVTBNMmx0WjE4eE1GODFOMTh5TURGZk1UVTROelkxTlY4eE1EQXdMVEUxT1RFNU9ETTJNRFUyTXpJdWFuQm5QM1k5TVRVNU1UazRNemd3TWc',
                                   'published_at': '2020-06-12T17:45:00Z',
                                   'relay_url': 'https://news.robinhood.com/831bb0bf-e1cd-38d6-8a76-f1bd61cb995d/',
                                   'source': 'CNBC', 'summary': '',
                                   'title': 'Friday’s comeback evaporates as S&P 500 turns negative, heads for big losing week',
                                   'updated_at': '2020-06-12T17:49:43.327940Z',
                                   'url': 'https://www.cnbc.com/2020/06/11/stock-market-futures-open-to-close-news.html',
                                   'uuid': '831bb0bf-e1cd-38d6-8a76-f1bd61cb995d',
                                   'related_instruments': ['8f92e76f-1e0e-4478-8580-16a6ffcfaef5'],
                                   'preview_text': 'The S&P 500 and Nasdaq Composite gave up earlier gains on Friday as Wall Street struggled to recover from its worst session in three months. Stocks were on pace',
                                   'currency_id': 'None'}, {'api_source': 'cnbc', 'author': '', 'num_clicks': 0,
                                                            'preview_image_url': 'https://images.robinhood.com/wTdBSpqBFoa8aJVLbTJv1MtMlS4/aHR0cHM6Ly9pbWFnZXMucm9iaW5ob29kLmNvbS9zRE5zaXhDWFN2cTdQQ25wSHVSRTJsWEhFd00vYUhSMGNITTZMeTlwYldGblpTNWpibUpqWm0wdVkyOXRMMkZ3YVM5Mk1TOXBiV0ZuWlM4eE1EWTFOVFU0TWpNdE1UVTVNRFk1TXpRNU1UYzBOV2RsZEhSNWFXMWhaMlZ6TFRFeU1qY3hPVGcxTVRrdWFuQmxaejkyUFRFMU9URTVNVE01TURV',
                                                            'published_at': '2020-06-12T13:30:00Z',
                                                            'relay_url': 'https://news.robinhood.com/3b45b8ed-7b87-34b4-ab6f-768e052d2a8c/',
                                                            'source': 'CNBC', 'summary': '',
                                                            'title': 'Dow jumps more than 600 points as Wall Street rebounds from its biggest sell-off since March',
                                                            'updated_at': '2020-06-12T13:32:02.738958Z',
                                                            'url': 'https://www.cnbc.com/2020/06/11/stock-market-futures-open-to-close-news.html',
                                                            'uuid': '3b45b8ed-7b87-34b4-ab6f-768e052d2a8c',
                                                            'related_instruments': [
                                                                'bab3b12b-4216-4b01-b2d8-9587ee5f41cf',
                                                                '8f92e76f-1e0e-4478-8580-16a6ffcfaef5'],
                                                            'preview_text': "Stocks rallied on Friday, clawing back some of the sharp losses from Wall Street's worst day since March.\n\nThe Dow Jones Industrial Average traded 684 points hi",
                                                            'currency_id': 'None'},
                                  {'api_source': '', 'author': '', 'num_clicks': 0,
                                   'preview_image_url': 'https://images.robinhood.com/XBBlea2sb1NCkWYIfsxUm039QDg/aHR0cHM6Ly9pbWFnZXMucm9iaW5ob29kLmNvbS92Z3VKd1ZkcVdRbHF4NXlQQmNXQmp3aUR0R3cvYUhSMGNITTZMeTlwYldGblpYTXVZM1JtWVhOelpYUnpMbTVsZEM5dGQzQm9lbmx4TmpsdmMyOHZOMGxhZERScVJrMXNla3RqWkU1MU1VSjBOakZMWVM4d1l6VmlOR00wT1RBelkySmxZbVU0WkdGaU1UVXlaRGM0T0RkbU5qVmpZaTlOUTBSVFFWQkJYMFZETURVeUxtcHdadw',
                                   'published_at': '2020-06-12T11:00:00Z',
                                   'relay_url': 'https://news.robinhood.com/882570b0-31b5-3e91-bec1-2e94477ba872/',
                                   'source': 'Robinhood Snacks', 'summary': '',
                                   'title': "Stocks have their worst day since March on investors' worst fear: A 2nd outbreak",
                                   'updated_at': '2020-06-12T11:13:07.745923Z',
                                   'url': 'https://snacks.robinhood.com/newsletters/6PR0xbLSMdv6hGEyPZHPHD/articles/6PO7UWvf1aF3lIwGXwx8OA',
                                   'uuid': '882570b0-31b5-3e91-bec1-2e94477ba872',
                                   'related_instruments': ['8f92e76f-1e0e-4478-8580-16a6ffcfaef5',
                                                           'bab3b12b-4216-4b01-b2d8-9587ee5f41cf'],
                                   'preview_text': 'Our Editorial Principles\n\nRobinhood Financial LLC and Robinhood Crypto, LLC are wholly-owned subsidiaries of Robinhood Markets, Inc. Equities and options are of',
                                   'currency_id': 'None'}, {'api_source': 'cnbc', 'author': '', 'num_clicks': 0,
                                                            'preview_image_url': 'https://images.robinhood.com/wTdBSpqBFoa8aJVLbTJv1MtMlS4/aHR0cHM6Ly9pbWFnZXMucm9iaW5ob29kLmNvbS9zRE5zaXhDWFN2cTdQQ25wSHVSRTJsWEhFd00vYUhSMGNITTZMeTlwYldGblpTNWpibUpqWm0wdVkyOXRMMkZ3YVM5Mk1TOXBiV0ZuWlM4eE1EWTFOVFU0TWpNdE1UVTVNRFk1TXpRNU1UYzBOV2RsZEhSNWFXMWhaMlZ6TFRFeU1qY3hPVGcxTVRrdWFuQmxaejkyUFRFMU9URTVNVE01TURV',
                                                            'published_at': '2020-06-12T10:00:00Z',
                                                            'relay_url': 'https://news.robinhood.com/5fc3fe9b-db96-369d-bfd4-90e316034927/',
                                                            'source': 'CNBC', 'summary': '',
                                                            'title': 'Dow futures bounce 600 points higher as Wall Street tries to recover from its worst day since March',
                                                            'updated_at': '2020-06-12T10:33:13.976215Z',
                                                            'url': 'https://www.cnbc.com/2020/06/11/stock-market-futures-open-to-close-news.html',
                                                            'uuid': '5fc3fe9b-db96-369d-bfd4-90e316034927',
                                                            'related_instruments': [
                                                                '8f92e76f-1e0e-4478-8580-16a6ffcfaef5',
                                                                'bab3b12b-4216-4b01-b2d8-9587ee5f41cf'],
                                                            'preview_text': "The Dow, S&P 500 and Nasdaq on Thursday all recorded their biggest one-day losses since mid-March, posting losses of at least 5.3%. Thursday's declines put the",
                                                            'currency_id': 'None'},
                                  {'api_source': '', 'author': '', 'num_clicks': 0,
                                   'preview_image_url': 'https://images.robinhood.com/JelKNdPB2krIqCEryoCWGwCyUT4/aHR0cHM6Ly9pbWFnZXMucm9iaW5ob29kLmNvbS9BRzVBeTFIWllWSWc5TG0zYkY1WVZSNjFJMTgvYUhSMGNITTZMeTl0WldScFlTNXVjSEl1YjNKbkwyRnpjMlYwY3k5cGJXY3ZNakF5TUM4d05pOHhNUzluWlhSMGVXbHRZV2RsY3kweE1qRTFNVGs1TWpFd0xURXRYM2RwWkdVdE1ERTJNREUxTm1Ga05EVTFNVEppWlRjMk9HSXpOek0yTWpZeE5tSTFaamd5TkRSalltRmxOaTVxY0djX2N6MHhOREF3',
                                   'published_at': '2020-06-11T17:00:00Z',
                                   'relay_url': 'https://news.robinhood.com/f896a88b-2ea7-3cd7-8f77-bb2772215cba/',
                                   'source': 'NPR', 'summary': '',
                                   'title': 'Dow Tumbles 1,500 Points On Worries Of 2nd Wave As Coronavirus Cases Spike',
                                   'updated_at': '2020-06-11T19:01:24.454573Z',
                                   'url': 'https://www.npr.org/sections/coronavirus-live-updates/2020/06/11/874600108/stocks-tumble-as-the-fed-warns-of-a-long-recovery-coronavirus-cases-spike',
                                   'uuid': 'f896a88b-2ea7-3cd7-8f77-bb2772215cba',
                                   'related_instruments': ['8f92e76f-1e0e-4478-8580-16a6ffcfaef5',
                                                           'bab3b12b-4216-4b01-b2d8-9587ee5f41cf'],
                                   'preview_text': 'Dow Tumbles 1,500 Points On Worries Of 2nd Wave As Coronavirus Cases Spike\n\nEnlarge this image toggle caption Johannes Eisele/AFP via Getty Images Johannes Eise',
                                   'currency_id': 'None'}, {'api_source': 'cnbc', 'author': '', 'num_clicks': 0,
                                                            'preview_image_url': 'https://images.robinhood.com/VqYWBBN7DP7UM1lFV0x8PM5NhfM/aHR0cHM6Ly9pbWFnZXMucm9iaW5ob29kLmNvbS80QWd4emVtbTJIanlsYzBpbi1GWWVJWlA4VHMvYUhSMGNITTZMeTlwYldGblpTNWpibUpqWm0wdVkyOXRMMkZ3YVM5Mk1TOXBiV0ZuWlM4eE1EWTFOelF3TVRFdE1UVTVNVGc0TnpRM056WXlNbWx0WjE4eE1GODFOMTh4T1RKZk9UVTNOalUxWHpFd01EQXRNVFU1TVRnNE56STNOekV6TWk1cWNHY19kajB4TlRreE9EZzNOVEV4',
                                                            'published_at': '2020-06-11T14:40:00Z',
                                                            'relay_url': 'https://news.robinhood.com/52fa19aa-1002-337b-87fd-de7de74ee3db/',
                                                            'source': 'CNBC', 'summary': '',
                                                            'title': 'Dow plunges 1,000 points, heads for worst day since April as airlines and retailers drop',
                                                            'updated_at': '2020-06-11T14:59:23.092528Z',
                                                            'url': 'https://www.cnbc.com/2020/06/10/stock-market-futures-open-to-close-news.html',
                                                            'uuid': '52fa19aa-1002-337b-87fd-de7de74ee3db',
                                                            'related_instruments': [
                                                                '8f92e76f-1e0e-4478-8580-16a6ffcfaef5',
                                                                'bab3b12b-4216-4b01-b2d8-9587ee5f41cf'],
                                                            'preview_text': 'Stocks fell sharply on Thursday as coronavirus cases increased in some states that are reopening up from lockdowns. Shares that have surged recently on hopes fo',
                                                            'currency_id': 'None'},
                                  {'api_source': 'cnbc', 'author': '', 'num_clicks': 0,
                                   'preview_image_url': 'https://images.robinhood.com/l-hiORv0qMrcwuJBg99RCsdEtBc/aHR0cHM6Ly9pbWFnZXMucm9iaW5ob29kLmNvbS9MM2xsVjd0ZGYzc2s3M1lTNjM0RWxtOHZISjQvYUhSMGNITTZMeTlwYldGblpTNWpibUpqWm0wdVkyOXRMMkZ3YVM5Mk1TOXBiV0ZuWlM4eE1EWTBPRFl6T0RRdE1UVTROamc1T1RNek56TTNOM2RoYkd3dWFuQm5QM1k5TVRVNE9ESTFNamcxTmc',
                                   'published_at': '2020-06-10T09:11:00Z',
                                   'relay_url': 'https://news.robinhood.com/d2d056fd-7de0-3303-8434-e338e5b99b46/',
                                   'source': 'CNBC', 'summary': '',
                                   'title': 'Dow futures little changed as investors await Fed’s forecast on the economy',
                                   'updated_at': '2020-06-10T10:11:46.220319Z',
                                   'url': 'https://www.cnbc.com/2020/06/09/stock-market-futures-open-to-close-news.html',
                                   'uuid': 'd2d056fd-7de0-3303-8434-e338e5b99b46',
                                   'related_instruments': ['8f92e76f-1e0e-4478-8580-16a6ffcfaef5',
                                                           'bab3b12b-4216-4b01-b2d8-9587ee5f41cf'],
                                   'preview_text': 'Around 6 a.m. ET, Dow futures implied an opening loss of about 120 points. The S&P 500 and Nasdaq were also lower.\n\nU.S. stock futures fell in early trading Wed',
                                   'currency_id': 'None'}]


@dataclass(frozen=True)
class News:
    api_source: str
    author: str
    num_clicks: int
    preview_image_url: str
    published_at: datetime
    relay_url: str
    source: str
    summary: str
    title: str
    updated_at: datetime
    url: str
    uuid: str
    related_instruments: List[str]
    preview_text: str
    currency_id: str


def clean_news(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data = convert_dates(data, ['published_at'])

    return data


def main() -> None:
    news = [News(**clean_news(n)) for n in EXAMPLES]
    print(news)


if __name__ == '__main__':
    main()
