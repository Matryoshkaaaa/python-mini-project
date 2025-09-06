import pandas as pd
import numpy as np
from statsmodels.nonparametric.kernel_regression import KernelReg
from scipy.signal import argrelextrema
import streamlit as st

def run_backtest(df_input, params, initial_balance, fee=0.001):
    """
    주어진 파라미터로 백테스트를 실행하고 결과를 반환합니다.
    Args:
        df_input (pd.DataFrame): yfinance로 다운로드된 데이터프레임.
        params (dict): 최적화할 파라미터 딕셔너리.
        initial_balance (float): 시작 자본금.
        fee (float): 거래 수수료율.
    Returns:
        tuple: (수익률, 최종 자산, 거래 내역 데이터프레임, 시그널 데이터프레임, 다이버전스 목록)
    """
    df_temp = df_input.copy()

    # 3-1. RSI 계산 함수
    def compute_rsi(series, period):
        delta = series.diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = pd.Series(gain, index=series.index).rolling(period).mean()
        avg_loss = pd.Series(loss, index=series.index).rolling(period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    df_temp["RSI"] = compute_rsi(df_temp["Close"].squeeze(), params['rsi_period'])

    # 3-2. 커널 회귀 예측 및 볼린저 밴드
    x = np.arange(len(df_temp))
    y = df_temp['Close'].to_numpy().ravel()
    y_pred = np.full(len(y), np.nan)
    window = int(params['kr_window'])

    if window >= len(y):
        return -100, 0, pd.DataFrame(), pd.DataFrame(), []

    for i in range(window, len(y)):
        x_train = x[i - window:i]
        y_train = y[i - window:i]
        try:
            kr = KernelReg(endog=y_train, exog=x_train, var_type='c', bw=[params['kr_bandwidth']])
            y_pred[i] = kr.fit([x[i]])[0][0]
        except Exception:
            y_pred[i] = np.nan

    df_temp['y_pred'] = y_pred
    vol = pd.Series(y).rolling(20).std()
    df_temp['band'] = (params['bb_k'] * vol).values

    # 3-3. RSI 다이버전스 감지
    order = int(params['extrema_order'])
    local_max_price = argrelextrema(df_temp["Close"].values, np.greater_equal, order=order)[0]
    local_min_price = argrelextrema(df_temp["Close"].values, np.less_equal, order=order)[0]
    divergences = []

    for i in range(1, len(local_min_price)):
        p1_idx, p2_idx = int(local_min_price[i - 1]), int(local_min_price[i])
        if df_temp["Close"].iloc[p2_idx].item() < df_temp["Close"].iloc[p1_idx].item() and \
           df_temp["RSI"].iloc[p2_idx].item() > df_temp["RSI"].iloc[p1_idx].item():
            if df_temp["RSI"].iloc[p2_idx].item() <= params['rsi_oversold']:
                divergences.append((df_temp.index[p1_idx], df_temp.index[p2_idx], "bullish"))

    for i in range(1, len(local_max_price)):
        p1_idx, p2_idx = int(local_max_price[i - 1]), int(local_max_price[i])
        if df_temp["Close"].iloc[p2_idx].item() > df_temp["Close"].iloc[p1_idx].item() and \
           df_temp["RSI"].iloc[p2_idx].item() < df_temp["RSI"].iloc[p1_idx].item():
            if df_temp["RSI"].iloc[p2_idx].item() >= params['rsi_overbought']:
                divergences.append((df_temp.index[p1_idx], df_temp.index[p2_idx], "bearish"))

    # 3-4. 매매 신호 생성 및 종합
    signal = np.zeros(len(y))
    for i in range(len(y)):
        if np.isnan(y_pred[i]) or np.isnan(df_temp['band'].iloc[i]):
            continue
        if y[i] > y_pred[i] + df_temp['band'].iloc[i]:
            signal[i] = -1
        elif y[i] < y_pred[i] - df_temp['band'].iloc[i]:
            signal[i] = 1
        else:
            signal[i] = 0

    for _, date_p2, div_type in divergences:
        if date_p2 in df_temp.index:
            idx = df_temp.index.get_loc(date_p2)
            if div_type == "bullish":
                signal[idx] = 1
            elif div_type == "bearish":
                signal[idx] = -1

    filtered_signal = np.zeros(len(signal))
    last_signal = 0
    for i in range(len(signal)):
        if signal[i] != 0 and signal[i] != last_signal:
            filtered_signal[i] = signal[i]
            last_signal = signal[i]
    df_temp['signal'] = filtered_signal

    # 3-5. 백테스트 실행
    capital = initial_balance
    balance = capital
    position = 0
    buy_price = 0
    trades = []
    dates = df_temp.index.to_list()
    prices = df_temp['Close'].to_numpy()
    signals = df_temp['signal'].to_numpy()

    for i in range(len(df_temp) - 1):
        price = prices[i + 1].item()
        date = dates[i + 1]

        if signals[i] == 1 and position == 0:
            position = balance * (1 - fee) / price
            buy_price = price
            balance = 0
            trades.append({'date': date, 'type': 'Buy', 'price': round(price, 3), 'quantity': round(position, 6),
                           'balance': round(balance, 3), 'profit': 0.0})
        elif signals[i] == -1 and position > 0:
            trade_profit = round(position * (price - buy_price) * (1 - fee), 3)
            balance = position * price * (1 - fee)
            trades.append({'date': date, 'type': 'Sell', 'price': round(price, 3), 'quantity': round(position, 6),
                           'balance': round(balance, 3), 'profit': trade_profit})
            position = 0
            buy_price = 0

    if position > 0:
        price = float(prices[-1].item())
        date = dates[-1]
        trade_profit = round(position * (price - buy_price) * (1 - fee), 3)
        balance = position * price * (1 - fee)
        trades.append({'date': date, 'type': 'Sell', 'price': round(price, 3), 'quantity': round(position, 6),
                       'balance': round(balance, 3), 'profit': trade_profit})

    final_value = balance if balance > 0 else position * prices[-1].item()
    if final_value == 0:
        profit_pct = -100
    else:
        profit_pct = (final_value - capital) / capital * 100

    trade_df = pd.DataFrame(trades)
    return profit_pct, final_value, trade_df, df_temp, divergences