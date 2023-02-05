from oandapyV20 import API
import configparser
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import time
import logging

from utils_func import getCandleDataFromOanda, oandaJsonToPythonList

# --------------------------------------------------
# loggingの設定
# --------------------------------------------------
formatter = '%(asctime)s:%(message)s'
logging.basicConfig(filename='test.log', level=logging.INFO, format=formatter)
logger = logging.getLogger(__name__)

h = logging.FileHandler('logtest.log')
h_formatter = logging.Formatter('%(asctime)s : %(levelname)s - %(filename)s - %(message)s')
h.setFormatter(h_formatter)

logger.addHandler(h)

# --------------------------------------------------
# configparserの宣言とiniファイルの読み込み
# --------------------------------------------------
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

accountID = config['oanda']['account_id']
access_token = config['oanda']['access_token']

print("accoutID is " + accountID)
print("access_token is " + access_token)

api = API(access_token=access_token, environment="live")

all_data = []
# year_months =[
#     [2022, 11], [2022, 12],
#     ]
# # year, monthでループ
# for year, month in year_months:
#     date_from = datetime.datetime(year, month, 1)
#     date_to = date_from + relativedelta(months=+1, day=1)

#     ret = getCandleDataFromOanda("USD_JPY", api, date_from, date_to, "M5")
#     month_data = oandaJsonToPythonList(ret)

#     all_data.extend(month_data)

date = datetime.datetime(2022, 9, 1, 0, 0)
end_date = datetime.datetime(2023, 1, 30, 0, 0)
minutes = 150 #1回のデータ取得が30データ以内に収まるように調整

while (date <= end_date):
    logger.info('run {} get candle data'.format(date))
    time.sleep(0.1)
    date_from = date
    date_to = date + datetime.timedelta(minutes=minutes)

    ret = getCandleDataFromOanda("USD_JPY", api, date_from, date_to, "M5")
    month_data = oandaJsonToPythonList(ret)

    all_data.extend(month_data)
    date += datetime.timedelta(minutes=minutes)
    logger.info('get {} get candle data'.format(date))

# pandas DataFrameへ変換
df = pd.DataFrame(all_data)
df.columns = ['Datetime', 'Volume', 'Open', 'High', 'Low', 'Close']
df = df.set_index('Datetime')

df.to_csv('./data/USD_JPY_202209-202301_M5.csv')
df.to_pickle('./data/USD_JPY_202209-202301_M5.pkl')