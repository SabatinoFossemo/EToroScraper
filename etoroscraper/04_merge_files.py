import pandas as pd

pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def save(x):
    x.to_csv(f'download/etoro_{x.CATEGORY.iloc[0]}.csv', index=False)


def rest():
    etoro = pd.read_csv('download/etoro.csv')
    etoro = etoro[etoro.CATEGORY != 'STOCK']
    etoro = etoro.drop('EXCHANGE', axis=1)
    etoro.groupby('CATEGORY').apply(lambda x: save(x))


def stocks():
    info = pd.read_csv('download/new_info.csv')
    etoro = pd.read_csv('download/e_toro.csv')
    etoro = etoro[etoro.CATEGORY == 'STOCK']
    etoro['SECTOR'] = info.SECTOR
    etoro['INDUSTRY'] = info.INDUSTRY
    etoro['EMPLOYEES'] = info.EMPLOYEES
    etoro['YAHOO_TICKER'] = info.YAHOO_TICKER
    found = etoro.SECTOR != 'NotFound'
    etoro = etoro[found]
    etoro.to_csv('download/etoro_EQUITIES.csv', index=False)


if __name__ == '__main__':
    stocks()
    rest()
