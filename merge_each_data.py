import pandas as pd
from utils_func import createDiffCloseClassifyer

# 暫定的にcsvから読み込む形で実施
df_past_data = pd.read_csv('./data/USD_JPY_202211-202212_M10_add_parameter.csv', index_col='Datetime')
df_openposition = pd.read_csv('./data/USD_JPY_202211-202212_M10_openposition.csv', index_col=0)

df_all = pd.concat([df_past_data, df_openposition],axis=1, join='inner')

df_all = createDiffCloseClassifyer(df_all)

df_all.to_csv('./data/USD_JPY_for_learning.csv')