from oandapyV20 import API
import configparser
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from utils_func import getCandleDataFromOanda, oandaJsonToPythonList

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
year_months =[
    [2022, 11], [2022, 12],
    ]
# year, monthでループ
for year, month in year_months:
    date_from = datetime.datetime(year, month, 1)
    date_to = date_from + relativedelta(months=+1, day=1)

    ret = getCandleDataFromOanda("USD_JPY", api, date_from, date_to, "M10")
    month_data = oandaJsonToPythonList(ret)

    all_data.extend(month_data)

# pandas DataFrameへ変換
df = pd.DataFrame(all_data)
df.columns = ['Datetime', 'Volume', 'Open', 'High', 'Low', 'Close']
df = df.set_index('Datetime')

df.to_csv('./data/USD_JPY_202211-202212_M10.csv')