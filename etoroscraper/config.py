import pandas as pd


class Config:
    BASE = pd.read_csv('doc/base.csv', index_col=0)

    HOME = BASE.loc['HOME'].LINK
    LOGIN = HOME + BASE.loc['LOGIN'].LINK
    DISCOVER = HOME + BASE.loc['DISCOVER'].LINK

    MARKETS = pd.read_csv('doc/markets.csv')
    MARKETS.LINK = DISCOVER + MARKETS.LINK



