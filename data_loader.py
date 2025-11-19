import yfinance as yf
import streamlit as st
import pandas as pd

@st.cache_data
def load_data(ticker, start, end):
    with st.spinner(f"'{ticker}' 데이터 다운로드 중..."):
        df_data = yf.download(ticker, start=start, end=end, auto_adjust=True)
    return df_data