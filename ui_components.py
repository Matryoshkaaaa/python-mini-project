import streamlit as st
import pandas as pd
import numpy as np
import optuna
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
# import koreanize_matplotlib
from datetime import date
from backtest_core import run_backtest
from data_loader import load_data

# ===== 한글 폰트 설정 (Windows 기준) =====
# 1) 사용할 폰트 파일 경로 (Windows 기본: 맑은 고딕)
font_path = r"C:\Windows\Fonts\malgun.ttf"

# 2) 폰트 매니저에 등록
fm.fontManager.addfont(font_path)
font_name = fm.FontProperties(fname=font_path).get_name()

# 3) 전역 설정
plt.rcParams["font.family"] = font_name
plt.rcParams["axes.unicode_minus"] = False
# =========================================


def setup_sidebar():
    st.sidebar.title("메뉴")
    page = st.sidebar.radio("페이지 선택", ["아키텍처", "메인 페이지", "평균 수익률 계산기"])
    initial_balance = st.sidebar.number_input("시작 자본금 (USD)", min_value=100, value=10000, step=100)
    fee = 0.001
    
    stock_options = {
        "암호화폐": ['BTC-USD', 'ETH-USD', 'XRP-USD', 'LTC-USD'],
        "미국 주식": ['AAPL', 'MSFT', 'GOOG', 'TSLA', 'AMZN', 'NVDA', 'ORCL', 'NFLX', 'INTC'],
        "한국 주식": [
            "005930.KS (삼성전자)", "000250.KQ (삼천당제약)", "036570.KS (엔씨소프트)",
            "051910.KS (LG화학)", "066700.KQ (테라젠이텍스)", "066970.KQ (엘앤에프)",
            "068270.KQ (셀트리온제약)", "078600.KQ (대주전자재료)", "096770.KS (SK이노베이션)",
            "128940.KQ (한미약품)", "185750.KQ (종근당)", "192080.KQ (더블유게임즈)",
            "207940.KS (삼성바이오로직스)", "251270.KQ (넷마블)", "293490.KQ (카카오게임즈)",
            "373220.KS (에너지솔루션)", "247540.KQ (에코프로비엠)", "225010.KQ (넥슨게임즈)",
            "373220.KS (LG에너지솔루션)"
        ],
        "글로벌 지수/상품": ['SPY', 'QQQ', 'GLD', 'VIX']
    }
    
    return initial_balance, fee, page, stock_options

def main_page(initial_balance, fee, stock_options):
    start_date = st.sidebar.date_input("시작일", pd.to_datetime("2025-01-01"))
    end_date = st.sidebar.date_input("종료일", pd.to_datetime("2025-08-26"))

    selected_category = st.sidebar.selectbox("종목 카테고리 선택", list(stock_options.keys()))
    selected_stock = st.sidebar.selectbox("종목 선택", stock_options[selected_category], index=0)
    stock_ticker = selected_stock.split(' ')[0]

    df = load_data(stock_ticker, start_date, end_date)

    if df.empty:
        st.error("데이터가 없습니다. 기간을 다시 설정하거나 다른 종목을 선택하세요.")
        st.stop()

    st.header("수동 파라미터 설정 및 백테스트")
    with st.expander("수동 설정", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            kr_window = st.slider("커널 회귀 윈도우 (일)", 10, 100, 50, 1)
        with col2:
            kr_bandwidth = st.slider("커널 회귀 대역폭", 0.1, 10.0, 5.0, 0.1)
        with col3:
            bb_k = st.slider("볼린저 밴드 k 값", 0.1, 3.0, 0.7, 0.1)

        col4, col5, col6, col7 = st.columns(4)
        with col4:
            rsi_period = st.slider("RSI 기간 (일)", 5, 30, 14, 1)
        with col5:
            extrema_order = st.slider("다이버전스 감지 오더", 1, 10, 5, 1)
        with col6:
            rsi_oversold = st.slider("RSI 과매도", 10, 40, 30, 1)
        with col7:
            rsi_overbought = st.slider("RSI 과매수", 60, 90, 70, 1)

        manual_params = {
            'kr_window': kr_window,
            'kr_bandwidth': kr_bandwidth,
            'bb_k': bb_k,
            'rsi_period': rsi_period,
            'extrema_order': extrema_order,
            'rsi_oversold': rsi_oversold,
            'rsi_overbought': rsi_overbought,
        }

        if st.button("수동 백테스트 실행"):
            with st.spinner("백테스트 실행 중..."):
                profit_pct, final_value, trade_df, result_df, divergences = run_backtest(df, manual_params, initial_balance, fee)

                st.subheader("백테스트 결과")
                st.write(f"최종 자산: **{final_value:,.2f} USD**")
                st.write(f"수익률: **{profit_pct:.2f}%**")

                st.subheader("거래 내역")
                st.dataframe(trade_df)

                st.subheader("차트 시각화")
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

                ax1.plot(result_df.index, result_df['Close'], color='blue', label=f'{stock_ticker} 종가')
                if 'y_pred' in result_df and 'band' in result_df:
                    ax1.plot(result_df.index, result_df['y_pred'], color='orange', linestyle='--', label='커널 회귀 예측')
                    ax1.fill_between(result_df.index, result_df['y_pred'] - result_df['band'],
                                     result_df['y_pred'] + result_df['band'], color='gray', alpha=0.2, label='변동성 밴드')
                buy_idx = np.where(result_df['signal'] == 1)[0]
                sell_idx = np.where(result_df['signal'] == -1)[0]
                ax1.scatter(result_df.index[buy_idx], result_df['Close'].iloc[buy_idx], marker='^', color='green',
                            label='매수 신호', alpha=0.8, s=100)
                ax1.scatter(result_df.index[sell_idx], result_df['Close'].iloc[sell_idx], marker='v', color='red',
                            label='매도 신호', alpha=0.8, s=100)

                bullish_plotted, bearish_plotted = False, False
                for start_date_div, end_date_div, div_type in divergences:
                    p1_price = result_df.loc[start_date_div]['Close']
                    p2_price = result_df.loc[end_date_div]['Close']
                    if div_type == "bullish":
                        if not bullish_plotted:
                            ax1.plot([start_date_div, end_date_div], [p1_price, p2_price], color='lime', linestyle='--', label='강세 다이버전스', linewidth=2)
                            bullish_plotted = True
                        else:
                            ax1.plot([start_date_div, end_date_div], [p1_price, p2_price], color='lime', linestyle='--', linewidth=2)
                    elif div_type == "bearish":
                        if not bearish_plotted:
                            ax1.plot([start_date_div, end_date_div], [p1_price, p2_price], color='magenta', linestyle='--', label='약세 다이버전스', linewidth=2)
                            bearish_plotted = True
                        else:
                            ax1.plot([start_date_div, end_date_div], [p1_price, p2_price], color='magenta', linestyle='--', linewidth=2)
                ax1.set_title(f"{stock_ticker} 가격 및 매매 신호")
                ax1.legend()
                ax1.grid(True)
                ax1.tick_params(labelbottom=True)
                
                ax2.plot(result_df.index, result_df["RSI"], label="RSI", color="blue")
                ax2.axhline(manual_params['rsi_overbought'], color="red", linestyle="--", alpha=0.5, label='과매수')
                ax2.axhline(manual_params['rsi_oversold'], color="green", linestyle="--", alpha=0.5, label='과매도')
                
                bullish_plotted, bearish_plotted = False, False
                for start_date_div, end_date_div, div_type in divergences:
                    p1_rsi = result_df.loc[start_date_div]['RSI']
                    p2_rsi = result_df.loc[end_date_div]['RSI']
                    if div_type == "bullish":
                        if not bullish_plotted:
                            ax2.plot([start_date_div, end_date_div], [p1_rsi, p2_rsi], color='lime', linestyle='--', label='강세 다이버전스', linewidth=2)
                            bullish_plotted = True
                        else:
                            ax2.plot([start_date_div, end_date_div], [p1_rsi, p2_rsi], color='lime', linestyle='--', linewidth=2)
                    elif div_type == "bearish":
                        if not bearish_plotted:
                            ax2.plot([start_date_div, end_date_div], [p1_rsi, p2_rsi], color='magenta', linestyle='--', label='약세 다이버전스', linewidth=2)
                            bearish_plotted = True
                        else:
                            ax2.plot([start_date_div, end_date_div], [p1_rsi, p2_rsi], color='magenta', linestyle='--', linewidth=2)
                
                ax2.set_title("RSI")
                ax2.legend()
                ax2.grid(True)
                
                plt.tight_layout()
                st.pyplot(fig)

    st.header("Optuna 기반 파라미터 최적화")
    st.write("베이지안 최적화를 통해 가장 높은 수익률을 내는 파라미터를 자동으로 찾아냅니다.")
    n_trials = st.number_input("최적화 시도 횟수", min_value=10, value=100, step=10)

    def objective(trial):
        kr_window_trial = trial.suggest_int('kr_window', 20, 100)
        kr_bandwidth_trial = trial.suggest_float('kr_bandwidth', 0.5, 10.0)
        bb_k_trial = trial.suggest_float('bb_k', 0.1, 2.0)
        rsi_period_trial = trial.suggest_int('rsi_period', 7, 21)
        extrema_order_trial = trial.suggest_int('extrema_order', 3, 10)
        rsi_oversold_trial = trial.suggest_int('rsi_oversold', 20, 40)
        rsi_overbought_trial = trial.suggest_int('rsi_overbought', 60, 80)

        params = {
            'kr_window': kr_window_trial, 'kr_bandwidth': kr_bandwidth_trial, 'bb_k': bb_k_trial,
            'rsi_period': rsi_period_trial, 'extrema_order': extrema_order_trial,
            'rsi_oversold': rsi_oversold_trial, 'rsi_overbought': rsi_overbought_trial,
        }
        profit_pct, _, _, _, _ = run_backtest(df, params, initial_balance, fee)
        return profit_pct

    if st.button(f"Optuna 최적화 시작 ({n_trials}회 시도)"):
        with st.spinner("최적화 진행 중... 잠시 기다려주세요."):
            status_placeholder = st.empty()
            status_placeholder.info(f"0 / {n_trials} 시도 완료")
            study = optuna.create_study(direction="maximize")
            for i in range(n_trials):
                study.optimize(objective, n_trials=1)
                status_placeholder.info(f"{i + 1} / {n_trials} 시도 완료")
        st.success("최적화 완료!")
        status_placeholder.empty()

        st.subheader("최적의 파라미터")
        st.json(study.best_params)
        st.write(f"최대 수익률: `{study.best_value:.2f}%`")
        st.write("---")

        st.subheader("최적 파라미터로 백테스트 결과")
        with st.spinner("최적 파라미터로 백테스트 재실행 중..."):
            best_profit_pct, best_final_value, best_trade_df, best_result_df, best_divergences = run_backtest(df, study.best_params, initial_balance, fee)
            
            st.write(f"최종 자산: **{best_final_value:,.2f} USD**")
            st.write(f"수익률: **{best_profit_pct:.2f}%**")
            st.subheader("최적화된 거래 내역")
            st.dataframe(best_trade_df)
            
            st.subheader("최적 파라미터 차트")
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
            
            ax1.plot(best_result_df.index, best_result_df['Close'], color='blue', label=f'{stock_ticker} 종가')
            if 'y_pred' in best_result_df and 'band' in best_result_df:
                ax1.plot(best_result_df.index, best_result_df['y_pred'], color='orange', linestyle='--', label='커널 회귀 예측')
                ax1.fill_between(best_result_df.index, best_result_df['y_pred'] - best_result_df['band'],
                                 best_result_df['y_pred'] + best_result_df['band'], color='gray', alpha=0.2, label='변동성 밴드')
            buy_idx = np.where(best_result_df['signal'] == 1)[0]
            sell_idx = np.where(best_result_df['signal'] == -1)[0]
            ax1.scatter(best_result_df.index[buy_idx], best_result_df['Close'].iloc[buy_idx], marker='^', color='green', label='매수 신호', alpha=0.8, s=100)
            ax1.scatter(best_result_df.index[sell_idx], best_result_df['Close'].iloc[sell_idx], marker='v', color='red', label='매도 신호', alpha=0.8, s=100)
            
            bullish_plotted, bearish_plotted = False, False
            for start_date_div, end_date_div, div_type in best_divergences:
                p1_price = best_result_df.loc[start_date_div]['Close']
                p2_price = best_result_df.loc[end_date_div]['Close']
                if div_type == "bullish":
                    if not bullish_plotted:
                        ax1.plot([start_date_div, end_date_div], [p1_price, p2_price], color='lime', linestyle='--', label='강세 다이버전스', linewidth=2)
                        bullish_plotted = True
                    else:
                        ax1.plot([start_date_div, end_date_div], [p1_price, p2_price], color='lime', linestyle='--', linewidth=2)
                elif div_type == "bearish":
                    if not bearish_plotted:
                        ax1.plot([start_date_div, end_date_div], [p1_price, p2_price], color='magenta', linestyle='--', label='약세 다이버전스', linewidth=2)
                        bearish_plotted = True
                    else:
                        ax1.plot([start_date_div, end_date_div], [p1_price, p2_price], color='magenta', linestyle='--', linewidth=2)
            ax1.set_title(f"{stock_ticker} 가격 및 최적화된 매매 신호")
            ax1.legend()
            ax1.grid(True)
            ax1.tick_params(labelbottom=True)
            
            ax2.plot(best_result_df.index, best_result_df["RSI"], label="RSI", color="blue")
            ax2.axhline(study.best_params['rsi_overbought'], color="red", linestyle="--", alpha=0.5, label='과매수')
            ax2.axhline(study.best_params['rsi_oversold'], color="green", linestyle="--", alpha=0.5, label='과매도')
            
            bullish_plotted, bearish_plotted = False, False
            for start_date_div, end_date_div, div_type in best_divergences:
                p1_rsi = best_result_df.loc[start_date_div]['RSI']
                p2_rsi = best_result_df.loc[end_date_div]['RSI']
                if div_type == "bullish":
                    if not bullish_plotted:
                        ax2.plot([start_date_div, end_date_div], [p1_rsi, p2_rsi], color='lime', linestyle='--', label='강세 다이버전스', linewidth=2)
                        bullish_plotted = True
                    else:
                        ax2.plot([start_date_div, end_date_div], [p1_rsi, p2_rsi], color='lime', linestyle='--', linewidth=2)
                elif div_type == "bearish":
                    if not bearish_plotted:
                        ax2.plot([start_date_div, end_date_div], [p1_rsi, p2_rsi], color='magenta', linestyle='--', label='약세 다이버전스', linewidth=2)
                        bearish_plotted = True
                    else:
                        ax2.plot([start_date_div, end_date_div], [p1_rsi, p2_rsi], color='magenta', linestyle='--', linewidth=2)
            ax2.set_title("RSI")
            ax2.legend()
            ax2.grid(True)
            plt.tight_layout()
            st.pyplot(fig)


def average_profit_calculator(initial_balance, fee, stock_options):
    st.header("한국 주식 전체 평균 수익률 계산")
    st.info("아래의 고정 파라미터로 모든 한국 주식 종목의 **상장일 ~ 2023-05-31** 기간의 평균 수익률을 계산합니다.")
    st.subheader("분석 대상 종목")

    stock_list = [
        "**삼성전자**", "**삼천당제약**", "**엔씨소프트**",
        "**LG화학**", "**테라젠이텍스**", "**엘앤에프**",
        "**셀트리온제약**", "**대주전자재료**", "**SK이노베이션**",
        "**한미약품**", "**종근당**", "**더블유게임즈**",
        "**삼성바이오로직스**", "**넷마블**", "**카카오게임즈**",
        "**에너지솔루션**", "**에코프로비엠**", "<del>**넥슨게임즈**</del>",
        "**LG에너지솔루션**"
    ]
    chunks = [stock_list[i:i + 3] for i in range(0, len(stock_list), 3)]
    for chunk in chunks:
        cols = st.columns(3)
        for i, stock in enumerate(chunk):
            cols[i].markdown(f"{stock}", unsafe_allow_html=True)
    st.warning("**특이사항:** 넥슨게임즈는 yfinance에 데이터가 없어 목록에서 제외했습니다.")
    st.markdown("---")
    st.subheader("분석 파라미터")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - **커널 회귀 윈도우 (일):** **50**
        - **커널 회귀 대역폭:** **5.0**
        - **볼린저 밴드 k값:** **0.7**
        - **RSI 기간 (일):** **14**
        """)
    with col2:
        st.markdown("""
        - **다이버전스 감지 오더:** **5**
        - **RSI 과매도:** **30**
        - **RSI 과매수:** **70**
        """)

    fixed_params = {
        'kr_window': 50, 'kr_bandwidth': 5.0, 'bb_k': 0.7,
        'rsi_period': 14, 'extrema_order': 5,
        'rsi_oversold': 30, 'rsi_overbought': 70,
    }
    start_date_korean = '1990-01-01'
    end_date_korean = '2023-05-31'

    if st.button("평균 수익률 계산 시작"):
        with st.spinner("모든 한국 주식의 백테스트를 실행하고 있습니다. 잠시만 기다려주세요..."):
            all_profit_percentages = []
            successful_stocks = []
            korean_stocks = stock_options["한국 주식"]
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, stock_item in enumerate(korean_stocks):
                try:
                    ticker = stock_item.split(' ')[0]
                    stock_name = stock_item.split(' ')[1].strip('()')
                    df_korean = load_data(ticker, start=start_date_korean, end=end_date_korean)
                    if df_korean.empty:
                        status_text.warning(f"경고: {stock_name} ({ticker}) 데이터가 없어 건너뜁니다.")
                        continue
                    profit_pct, _, _, _, _ = run_backtest(df_korean, fixed_params, initial_balance, fee)
                    all_profit_percentages.append(profit_pct)
                    successful_stocks.append(stock_item)
                    progress_percentage = (i + 1) / len(korean_stocks)
                    progress_bar.progress(progress_percentage)
                    status_text.info(f"{stock_name} ({ticker}) 백테스트 완료. 수익률: {profit_pct:.2f}%")
                except Exception as e:
                    status_text.error(f"오류 발생: {stock_name} ({ticker}) - {e}")
                    continue
            progress_bar.empty()
            status_text.empty()
        
        if all_profit_percentages:
            average_profit = np.mean(all_profit_percentages)
            st.subheader("최종 결과")
            st.success(f"**전체 한국 주식 평균 수익률: {average_profit:.2f}%**")
            st.write("---")
            st.dataframe(pd.DataFrame({
                "종목": [item.split(' ')[1].strip('()') for item in successful_stocks],
                "티커": [item.split(' ')[0] for item in successful_stocks],
                "수익률 (%)": all_profit_percentages
            }))
        else:
            st.warning("계산 가능한 주식 데이터가 없습니다. 다시 시도해주세요.")