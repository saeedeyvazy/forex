import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from plotly.subplots import make_subplots
from utils.utility import path_exists
from datetime import datetime
import pandas_ta as ta

tickers_list = ['USDJPY=X', 'USDCHF=X', 'GC=F', 'EURUSD=X']
download_path = './downloads'
start_time_for_gathering_data = '2014-01-01'
end_time_for_gathering_data = datetime.today().strftime('%Y-%m-%d')
interval_for_gathering_time = '1d'


def fetch_data():
    ilist = []
    is_processed = False;
    for ticker in tickers_list:
        clean_ticker = ticker.replace('=X', '')
        clean_ticker = clean_ticker.replace('=F', '')
        file = path_exists(download_path, clean_ticker, '.csv')
        if file:
            ilist.append({clean_ticker: pd.read_csv(file)})
            is_processed = True

    if len(ilist) > 0:
        return ilist, is_processed

    df = yf.download(tickers=tickers_list, start=start_time_for_gathering_data, end=end_time_for_gathering_data,
                     interval=interval_for_gathering_time, group_by='ticker')


    df_usdjpy_candle_1d_2000_01_01_to_2024_08_04 = df[tickers_list[0]]
    df_usdchf_candle_1d_2000_01_01_to_2024_08_04 = df[tickers_list[1]]
    df_gold_candle_1d_2000_01_01_to_2024_08_04 = df[tickers_list[2]]
    df_eurusd_candle_1d_2000_01_01_to_2024_08_04 = df[tickers_list[3]]

    df_gold_candle_1d_2000_01_01_to_2024_08_04.to_csv(
        download_path + '/GC_candle_' + interval_for_gathering_time + start_time_for_gathering_data + '_TO_' + end_time_for_gathering_data + '.csv',
        mode='w+')

    df_usdchf_candle_1d_2000_01_01_to_2024_08_04.to_csv(
        download_path + '/USDCHF_candle_' + interval_for_gathering_time  + start_time_for_gathering_data + '_TO_' + end_time_for_gathering_data + '.csv',
        mode='w+')

    df_eurusd_candle_1d_2000_01_01_to_2024_08_04.to_csv(
        download_path + '/EURUSD_candle_' + interval_for_gathering_time  + start_time_for_gathering_data + '_TO_' + end_time_for_gathering_data + '.csv',
        mode='w+')

    df_usdjpy_candle_1d_2000_01_01_to_2024_08_04.to_csv(
        download_path + '/USDJPY_candle_' + interval_for_gathering_time  + start_time_for_gathering_data + '_TO_' + end_time_for_gathering_data + '.csv',
        mode='w+')

    return [{'EURUSD': df_eurusd_candle_1d_2000_01_01_to_2024_08_04},
            {'GC': df_gold_candle_1d_2000_01_01_to_2024_08_04},
            {'USDCHF': df_usdchf_candle_1d_2000_01_01_to_2024_08_04},
            {'USDJPY': df_usdjpy_candle_1d_2000_01_01_to_2024_08_04}], is_processed


def calc_primary_indicator(df):
    df.ta.bbands(append=True, length=30, std=2)
    df.ta.rsi(append=True, length=14)
    df["ATR"] = ta.atr(low=df.Low, close=df.Close, high=df.High, length=14)

    # Rename columns for clarity if necessary
    df.rename(columns={
        'BBL_30_2.0': 'BBL', 'BBM_30_2.0': 'BBM', 'BBU_30_2.0': 'BBH', 'RSI_14': 'RSI'
    }, inplace=True)

    # Calculate Bollinger Bands Width
    df['BB_WIDTH'] = (df['BBH'] - df['BBL']) / df['BBM']


def plot_chart_with_indicators(df, label, st):
    dfpl = df[st:st + 350]
    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(go.Candlestick(x=dfpl.index,
                                 open=dfpl['Open'],
                                 high=dfpl['High'],
                                 low=dfpl['Low'],
                                 close=dfpl['Close']),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['BBL'],
                             line=dict(color='blue', width=1),
                             name="BBL"),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['BBH'],
                             line=dict(color='green', width=1),
                             name="BBU"),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['RSI'],
                             line=dict(color='green', width=2),
                             name="RSI"),
                  row=2, col=1)

    fig.update_layout(width=1800, height=800, sliders=[], title_text=label)

    fig.show()


fetched_data_list, is_processed = fetch_data()
df_list = []
ticker_list = []
for item in fetched_data_list:
    df_list.append(pd.DataFrame(list(item.items())[0][1]))
    ticker_list.append(list(item.items())[0][0])

if not is_processed:
    for index in range(0, len(df_list)): calc_primary_indicator(df_list[index])
    df_list[index].reset_index(inplace=True)
    df_list[index].set_index('Date', inplace=True)
    for index in range(0, len(df_list)): df_list[index].to_csv(download_path + "/" + ticker_list[index] + '.csv')

for index in range(0, len(df_list)):
    df_list[index].reset_index(inplace=True)
    df_list[index].set_index('Date', inplace=True)
    plot_chart_with_indicators(df_list[index], ticker_list[index], st=500)
