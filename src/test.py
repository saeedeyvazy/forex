import multiprocessing
from itertools import product
import itertools
from backtesting import Strategy
from backtesting import Backtest
import pandas as pd
import pandas_ta as ta

df = pd.read_csv('clean15.csv')
df.rename(columns={'datetime': 'Gmt time', 'close': 'Close', 'high': 'High', 'open': 'Open', 'low': 'Low'},
          inplace=True)
# df = pd.read_csv("EURUSD_Candlestick_5_M_ASK_30.09.2019-30.09.2022.csv")
df["Gmt time"] = df["Gmt time"].str.replace(".000", "")
df['Gmt time'] = pd.to_datetime(df['Gmt time'], format='%Y-%m-%d %H:%M:%S')
df = df[df.High != df.Low]
df.set_index("Gmt time", inplace=True)

from tqdm import tqdm


class ScalpingStrategyBasedEMABollingerBand:

    def __init__(self, df: pd.DataFrame, ema_slow_length: int, ema_fast_length: int, back_candle_no: int,
                 last_candle_num_to_processing: int):
        self.ema_slow_length = ema_slow_length
        self.ema_fast_length = ema_fast_length
        self.back_candle_no = back_candle_no
        self.last_candle_num_to_processing = last_candle_num_to_processing
        self.df = df[-last_candle_num_to_processing:-1]

        self.df["EMA_slow"] = ta.ema(self.df.Close, length=self.ema_slow_length)
        self.df["EMA_fast"] = ta.ema(self.df.Close, length=self.ema_fast_length)
        self.df['RSI'] = ta.rsi(self.df.Close, length=10)
        my_bbands = ta.bbands(self.df.Close, length=15, std=1.5)
        self.df['ATR'] = ta.atr(self.df.High, self.df.Low, self.df.Close, length=back_candle_no)
        self.df = self.df.join(my_bbands)
        self.calculate_ema_signal()

    def ema_signal(self, current_candle):
        df_slice = self.df.reset_index().copy()
        # Get the range of candles to consider
        start = max(0, current_candle - self.back_candle_no)
        end = current_candle
        relevant_rows = df_slice.iloc[start:end]

        # Check if all EMA_fast values are below EMA_slow values
        if all(relevant_rows["EMA_fast"] < relevant_rows["EMA_slow"]):
            return 1
        elif all(relevant_rows["EMA_fast"] > relevant_rows["EMA_slow"]):
            return 2
        else:
            return 0

    def calculate_ema_signal(self):
        tqdm.pandas()
        self.df.reset_index(inplace=True)
        self.df['EMASignal'] = self.df.progress_apply(lambda row: self.ema_signal(row.name),
                                                      axis=1)  # if row.name >= 20 else 0

    def total_signal(self, current_candle):
        if (self.ema_signal(current_candle) == 2
                and self.df.Close[current_candle] <= self.df['BBL_15_1.5'][current_candle]
        ):
            return 2

        if (self.ema_signal(current_candle) == 1
                and self.df.Close[current_candle] >= self.df['BBU_15_1.5'][current_candle]
        ):
            return 1

        return 0

    def calc_total_signal(self):
        self.df['TotalSignal'] = self.df.progress_apply(lambda row: self.total_signal(row.name), axis=1)


class MyStrat(Strategy):
    mysize = 3000
    slcoef = 1.894736
    TPSLRatio = 1.05263
    rsi_length = 16

    def init(self):
        super().init()
        self.signal1 = self.data.TotalSignal

    def next(self):
        super().next()
        slatr = self.slcoef * self.data.ATR[-1]
        TPSLRatio = self.TPSLRatio

        if self.data.TotalSignal == 2 and len(self.trades) == 0:
            sl1 = self.data.Close[-1] - slatr
            tp1 = self.data.Close[-1] + slatr * TPSLRatio
            self.buy(sl=sl1, tp=tp1, size=self.mysize)

        elif self.data.TotalSignal == 1 and len(self.trades) == 0:
            sl1 = self.data.Close[-1] + slatr
            tp1 = self.data.Close[-1] - slatr * TPSLRatio
            self.sell(sl=sl1, tp=tp1, size=self.mysize)


def test(ema1, ema2, back, no):
    a = ScalpingStrategyBasedEMABollingerBand(df, ema1, ema2, back, no)
    a.calc_total_signal()
    bt = Backtest(a.df, MyStrat, cash=250, margin=1 / 30)
    return bt.run()


if __name__ == '__main__':
    ema_slow = [30, 50]
    ema_fast = [30, 40, 70]
    back_candle = list(range(4, 30))
    no = [30000]
    with multiprocessing.Pool(processes=3) as pool:
        # results = pool.starmap(merge_names, product(names, repeat=2))
        args = [x for x in itertools.product(ema_slow, ema_fast, back_candle, no)]
        results = pool.starmap(test, args)

    print(results)
