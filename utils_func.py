from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.pricing import PricingStream
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.instruments as instruments

import json
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

# Oandaからcandleデータを取得する。
def getCandleDataFromOanda(instrument, api, date_from, date_to, granularity):
    params = {
        "from": date_from.isoformat(),
        "to": date_to.isoformat(),
        "granularity": granularity,
    }
    r = instruments.InstrumentsCandles(instrument=instrument, params=params)
    return api.request(r)

# JSON形式をpythonの配列に変換する
def oandaJsonToPythonList(JSONRes):
    data = []
    for res in JSONRes['candles']:
        data.append( [
            datetime.datetime.fromisoformat(res['time'][:19]),
            res['volume'],
            res['mid']['o'],
            res['mid']['h'],
            res['mid']['l'],
            res['mid']['c'],
            ])
    return data

# 目的変数（objective variable）の追加
# ここでは、前回の終値より10pips上がったか、下がったか、変化なしかに分類する
def createDiffCloseClassifyer(df):
    df['diff'] = df['Close'].diff()
    df['diff'] = df['diff'].shift(-1)
    df.loc[df['diff'] >= 0.1, 'class'] = 1
    df.loc[df['diff'] < 0.1, 'class'] = 0
    df.loc[df['diff'] <= -0.1, 'class'] = -1
    
    return df

def convert_from_csv_to_pkl(csv_file_name):
    df = pd.read_csv(csv_file_name)
    df.to_pickle(csv_file_name[:-3]+ 'pkl')

# df = pd.read_csv('./USD_JPY_202211-202212_M10.csv', index_col='Datetime')

# df = createDiffCloseClassifyer(df)
# df['diff']

# # グラフにプロット（確認用の暫定コード）
# from matplotlib import dates as mdates

# ax = df['diff'].plot(color="blue", label="Close")
# df['class'].plot(ax=ax, ls="--", color="red", label='class')

# ax.grid()
# ax.legend()
# # todo:時刻の設定を変更
# ax.xaxis.set_major_formatter(mdates.DateFormatter("%y-%m-%d"))
# plt.savefig(f'figure_diff.png')
# plt.clf()

# print('+:'+ str(len(df[df['class']==1]))+ ' 0:' + str(len(df[df['class']==0]))+ ' -:' + str(len(df[df['class']==-1])))

if __name__ == "__main__":
    convert_from_csv_to_pkl("./data/USD_JPY_open_order.csv")
    convert_from_csv_to_pkl("./data/USD_JPY_open_position.csv")
