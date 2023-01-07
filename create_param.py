import pandas as pd
import matplotlib.pyplot as plt
#機械学習に用いるパラメータを生成

# 暫定的にcsvから読み込む形で実施
df = pd.read_csv('./USD_JPY_202211-202212_M10.csv', index_col='Datetime')

# 移動平均、ボリンジャーバンドを追加
move_ave_setting = [5, 25, 60, 120]

for num, ave in enumerate(move_ave_setting):
    df_ma = df['Close'].rolling(window=ave).mean()
    std = df['Close'].rolling(window=ave).std()
    df_ma =df_ma.rename(f'{ave}_ma')
    band1_upper = df_ma + std
    band1_lower = df_ma - std
    band2_upper = df_ma + 2 * std
    band2_lower = df_ma - 2 * std
    band3_upper = df_ma + 3 * std
    band3_lower = df_ma - 3 * std
    df = pd.concat([df, df_ma, band1_upper.rename(f'{ave}_band1_upper'), band1_lower.rename(f'{ave}_band1_lower'), 
    band2_upper.rename(f'{ave}_band2_upper'), band2_lower.rename(f'{ave}_band2_lower'), 
    band3_upper.rename(f'{ave}_band3_upper'), band3_lower.rename(f'{ave}_band3_lower'), ], axis=1)

# 移動平均線の傾きを追加
df_diff = df.diff()

for ave in move_ave_setting:
    ds = df_diff[f'{ave}_ma'].rename(f'{ave}_ma_diff')
    df = pd.concat([df, ds], axis=1)

# グラフにプロット（確認用の暫定コード）
from matplotlib import dates as mdates

for ave in move_ave_setting:
    ax = df['Close'].plot(color="blue", label="Close")
    df[f'{ave}_ma'].plot(ax=ax, ls="--", color="red", label=f"{ave}MA")
    df[f'{ave}_band1_upper'].plot(ax=ax, ls="--", color="blue", label=f"{ave} Band1 Upper")
    df[f'{ave}_band2_upper'].plot(ax=ax, ls="--", color="green", label=f"{ave} Band2 Upper")
    df[f'{ave}_band3_upper'].plot(ax=ax, ls="--", color="orange", label=f"{ave} Band3 Upper")
    ax.grid()
    ax.legend()
    # todo:時刻の設定を変更
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%y-%m-%d"))
    plt.savefig(f'figure_{ave}.png')
    plt.clf()