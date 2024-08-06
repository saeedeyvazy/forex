import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from plotly.subplots import make_subplots
from utils.utility import path_exists, apply_total_signal, pointpos
from datetime import datetime
import pandas_ta as ta

tickers_list = ['USDJPY=X', 'USDCHF=X', 'GC=F', 'EURUSD=X', 'BMW.DE']

download_path = './downloads'
start_time_for_gathering_data = '2011-01-01'
end_time_for_gathering_data = '2024-05-11' #datetime.today().strftime('%Y-%m-%d')
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
    df_bmw_de_candle_1d_2000_01_01_to_2024_08_04 = df[tickers_list[4]]

    df_gold_candle_1d_2000_01_01_to_2024_08_04.to_csv(
        download_path + '/GC_candle_' + interval_for_gathering_time + start_time_for_gathering_data + '_TO_' + end_time_for_gathering_data + '.csv',
        mode='w+')

    df_usdchf_candle_1d_2000_01_01_to_2024_08_04.to_csv(
        download_path + '/USDCHF_candle_' + interval_for_gathering_time + start_time_for_gathering_data + '_TO_' + end_time_for_gathering_data + '.csv',
        mode='w+')

    df_eurusd_candle_1d_2000_01_01_to_2024_08_04.to_csv(
        download_path + '/EURUSD_candle_' + interval_for_gathering_time + start_time_for_gathering_data + '_TO_' + end_time_for_gathering_data + '.csv',
        mode='w+')

    df_usdjpy_candle_1d_2000_01_01_to_2024_08_04.to_csv(
        download_path + '/USDJPY_candle_' + interval_for_gathering_time + start_time_for_gathering_data + '_TO_' + end_time_for_gathering_data + '.csv',
        mode='w+')

    df_bmw_de_candle_1d_2000_01_01_to_2024_08_04.to_csv(
        download_path + '/BMW.DE_candle_' + interval_for_gathering_time + start_time_for_gathering_data + '_TO_' + end_time_for_gathering_data + '.csv',
        mode='w+')

    return [{'EURUSD': df_eurusd_candle_1d_2000_01_01_to_2024_08_04},
            {'GC': df_gold_candle_1d_2000_01_01_to_2024_08_04},
            {'USDCHF': df_usdchf_candle_1d_2000_01_01_to_2024_08_04},
            {'BMW.DE': df_bmw_de_candle_1d_2000_01_01_to_2024_08_04},
            {'USDJPY': df_usdjpy_candle_1d_2000_01_01_to_2024_08_04}], is_processed


def calc_primary_indicator(df):
    df = df[df.High != df.Low]

    df.ta.bbands(append=True, length=30, std=2)
    df.ta.rsi(append=True, length=14)
    df["atr"] = ta.atr(low=df.Low, close=df.Close, high=df.High, length=14)

    df.rename(columns={
        'BBL_30_2.0': 'bbl', 'BBM_30_2.0': 'bbm', 'BBU_30_2.0': 'bbh', 'RSI_14': 'rsi'
    }, inplace=True)

    # Calculate Bollinger Bands Width
    df['bb_width'] = (df['bbh'] - df['bbl']) / df['bbm']

    df.rename(
        columns={'bbl': 'BBL', 'bb_width': 'BB_WIDTH', 'bbm': 'BBM', 'bbh': 'BBH', 'rsi': 'RSI'},
        inplace=True)

    return df


def plot_chart_with_indicators(df, label, st):
    dfpl = df
    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(go.Candlestick(x=dfpl.Date,
                                 open=dfpl['Open'],
                                 high=dfpl['High'],
                                 low=dfpl['Low'],
                                 close=dfpl['Close']),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=dfpl.Date, y=dfpl['BBL'],
                             line=dict(color='blue', width=1),
                             name="BBL"),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=dfpl.Date, y=dfpl['BBH'],
                             line=dict(color='green', width=1),
                             name="BBU"),
                  row=1, col=1)

    # Add markers for trade entry points on the same subplot
    fig.add_trace(go.Scatter(x=dfpl.Date, y=dfpl['pointpos'], mode="markers",
                             marker=dict(size=8, color="MediumPurple"),
                             name="entry"),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=dfpl.Date, y=dfpl['RSI'],
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
    for index in range(0, len(df_list)):
        df_list[index] = calc_primary_indicator(df_list[index])
        df_list[index] = df_list[index].round(4)
        df_list[index].reset_index(inplace=True)
        df_list[index].set_index('Date', inplace=True)
        df_list[index].to_csv(download_path + "/" + ticker_list[index] + '.csv')

total_signal_length = 0
for index in range(0, len(df_list)):
    df = df_list[index]
    df.ta.bbands(append=True, length=30, std=2)
    df.ta.rsi(append=True, length=14)
    df["atr"] = ta.atr(low=df.Low, close=df.Close, high=df.High, length=14)
    df.rename(columns={
        'BBL_30_2.0': 'bbl', 'BBM_30_2.0': 'bbm', 'BBU_30_2.0': 'bbh', 'RSI_14': 'rsi'
    }, inplace=True)

    # Calculate Bollinger Bands Width
    df['bb_width'] = (df['bbh'] - df['bbl']) / df['bbm']
    apply_total_signal(df=df, rsi_threshold_low=30, rsi_threshold_high=70, bb_width_threshold=0.001)
    df['pointpos'] = df.apply(lambda row: pointpos(row), axis=1)
    total_signal_length += len(df[df['TotalSignal'] != 0])

    print('Ticker : ' + ticker_list[index] + ' \n' )
    print(df[df['TotalSignal'] != 0])

    plot_chart_with_indicators(df, ticker_list[index], st=500)

print("Total Signal Count Is: {i}", total_signal_length)
