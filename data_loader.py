import yfinance as yf
import streamlit as st
import pandas as pd

@st.cache_data
def load_data(ticker, start, end):
    """지정된 기간의 주식 데이터를 다운로드하고 캐시합니다."""
    with st.spinner(f"'{ticker}' 데이터 다운로드 중..."):
        df_data = yf.download(ticker, start=start, end=end, auto_adjust=True)
    return df_data