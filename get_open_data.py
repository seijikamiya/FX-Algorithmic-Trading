from oandapyV20.endpoints import instruments
from oandapyV20 import API
import datetime
import pytz
import configparser
import pandas as pd
import logging

formatter = '%(asctime)s:%(message)s'
logging.basicConfig(filename='test.log', level=logging.INFO, format=formatter)
logger = logging.getLogger(__name__)

h = logging.FileHandler('logtest.log')
h_formatter = logging.Formatter('%(asctime)s : %(levelname)s - %(filename)s - %(message)s')
h.setFormatter(h_formatter)

logger.addHandler(h)

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

accountID = config['oanda']['account_id']
access_token = config['oanda']['access_token']

def convert_to_utc(dt):
    return dt.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

access_token = access_token

client = API(access_token=access_token, environment="live")

instrument="USD_JPY"
# params = {
#     "time": convert_to_utc(dt)
# }

def get_orderbook_data(client, instrument, dt):
    
    params = {
    "time": dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    logger.info('run {} orderbook data'.format(params['time']))

    r = instruments.InstrumentsOrderBook(instrument=instrument, params=params)

    client.request(r)

    logger.info('get {} orderbook data'.format(r.response['orderBook']['time']))

    # print(r.response['orderBook']['buckets'])
    df_orderbook = pd.DataFrame(r.response['orderBook']['buckets'])
    df_orderbook = df_orderbook.astype(float)
    # print(df_orderbook.head(-10))

    price = float(r.response['orderBook']['price'])
    df_sort_long = df_orderbook.sort_values('longCountPercent', ascending=False)
    df_sort_long['price'] = df_sort_long['price'].apply(lambda x: x - price)
    df_sort_long = df_sort_long[(-10 < df_sort_long['price']) & (df_sort_long['price']  < 10)]
    # print(df_sort_long.head(20))

    df_sort_short = df_orderbook.sort_values('shortCountPercent', ascending=False)
    df_sort_short['price'] = df_sort_short['price'].apply(lambda x: x - price)
    df_sort_short = df_sort_short[(-10 < df_sort_short['price']) & (df_sort_short['price']  < 10)]
    # print(df_sort_short.head(20).T)

    df_orderbook_final = pd.concat([df_sort_long['price'].head(10), df_sort_long['longCountPercent'].head(10), 
                                    df_sort_short['price'].head(10), df_sort_short['longCountPercent'].head(10)], axis=0)

    return df_orderbook_final

def get_openposition_data(client, instrument, dt):
    
    params = {
    "time": dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    logger.info('run {} position book data'.format(params['time']))

    r = instruments.InstrumentsPositionBook(instrument=instrument, params=params)

    client.request(r)

    logger.info('get {} position book data'.format(r.response['positionBook']['time']))

    # print(r.response['orderBook']['buckets'])
    df_orderbook = pd.DataFrame(r.response['positionBook']['buckets'])
    df_orderbook = df_orderbook.astype(float)
    # print(df_orderbook.head(-10))

    price = float(r.response['positionBook']['price'])
    df_sort_long = df_orderbook.sort_values('longCountPercent', ascending=False)
    df_sort_long['price'] = df_sort_long['price'].apply(lambda x: x - price)
    df_sort_long = df_sort_long[(-10 < df_sort_long['price']) & (df_sort_long['price']  < 10)]
    # print(df_sort_long.head(20))

    df_sort_short = df_orderbook.sort_values('shortCountPercent', ascending=False)
    df_sort_short['price'] = df_sort_short['price'].apply(lambda x: x - price)
    df_sort_short = df_sort_short[(-10 < df_sort_short['price']) & (df_sort_short['price']  < 10)]
    # print(df_sort_short.head(20).T)

    df_orderbook_final = pd.concat([df_sort_long['price'].head(10), df_sort_long['longCountPercent'].head(10), 
                                    df_sort_short['price'].head(10), df_sort_short['longCountPercent'].head(10)], axis=0)

    return df_orderbook_final

dt = datetime.datetime(2022, 12, 1, 0, 0)
end_date = datetime.datetime(2022, 12, 1, 12, 0)
df_openorder = get_orderbook_data(client, instrument, dt).reset_index(drop=True).rename(dt)
df_openposition = get_openposition_data(client, instrument, dt).reset_index(drop=True).rename(dt)

while (dt <= end_date):
    dt += datetime.timedelta(minutes=10)
    df_openorder = pd.concat([df_openorder, get_orderbook_data(client, instrument, dt).reset_index(drop=True).rename(dt)], axis=1)
    df_openposition = pd.concat([df_openposition, get_openposition_data(client, instrument, dt).reset_index(drop=True).rename(dt)], axis=1)

df_openorder.T.to_csv('./data/USD_JPY_open_order.csv')
df_openposition.T.to_csv('./data/USD_JPY_open_position.csv')