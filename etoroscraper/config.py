import pandas as pd


class Config:
    BASE = pd.read_csv('doc/base.csv', index_col=0)

    HOME = BASE.loc['HOME'].LINK
    LOGIN = HOME + BASE.loc['LOGIN'].LINK

    MARKETS = pd.read_csv('doc/markets.csv', index_col=0)
    MARKETS.LINK = HOME + MARKETS.LINK

    EXCHANGES = pd.read_csv('doc/exchanges.csv', index_col=0)
    EXCHANGES.LINK = MARKETS.loc['STOCKS'].LINK + EXCHANGES.LINK

