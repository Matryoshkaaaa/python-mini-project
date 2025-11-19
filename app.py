import streamlit as st
import pandas as pd
import warnings
from ui_components import setup_sidebar, main_page, average_profit_calculator

warnings.filterwarnings("ignore")

st.set_page_config(layout="wide")

st.title("트레이딩 전략 최적화 및 백테스트")
st.write("커널 회귀, RSI 다이버전스, 볼린저 밴드 기반 전략")
st.write("---")

initial_balance, fee, page, stock_options = setup_sidebar()

if page == "메인 페이지":
    main_page(initial_balance, fee, stock_options)

elif page == "평균 수익률 계산기":
    average_profit_calculator(initial_balance, fee, stock_options)

elif page == "아키텍처":
    st.header("아키텍처")
    st.markdown("""
    이 프로젝트는 **모듈화된 아키텍처**를 사용하여 각 기능별로 코드를 분리했습니다.
    
    * **`app.py`**: Streamlit 앱의 진입점으로, UI 컴포넌트들을 불러와 페이지를 구성합니다.
    * **`ui_components.py`**: 페이지의 레이아웃, 버튼, 슬라이더 등 **사용자 인터페이스** 로직을 관리합니다.
    * **`data_loader.py`**: **데이터 다운로드**를 담당하며, `st.cache_data`를 이용해 캐싱 효율을 높입니다.
    * **`backtest_core.py`**: 모든 **백테스트 로직** (RSI, 커널 회귀, 매매 시그널, 수익률 계산)을 처리합니다.
    
    이 구조는 코드의 **가독성과 유지보수성**을 향상시키며, 기능별로 독립적인 개발이 가능하게 합니다.
    """)