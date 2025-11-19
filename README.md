# 📈 커널 회귀 + RSI 다이버전스 기반 트레이딩 전략 백테스트 대시보드

> **Streamlit 기반 트레이딩 전략 백테스트 & 파라미터 최적화 웹 앱**  
> 커널 회귀(Kernel Regression), RSI 다이버전스, 볼린저 밴드 기반으로  
> 주식·암호화폐 데이터를 백테스트하고, Optuna로 전략 파라미터를 자동 최적화

---

## 🖼️ 데모 / 스크린샷

 
<img width="919" height="413" alt="image" src="https://github.com/user-attachments/assets/70b2c566-6cb3-4ccc-9e74-8f6e29cd6663" />
<img width="727" height="345" alt="image" src="https://github.com/user-attachments/assets/4f6dd914-4d74-487c-a709-e6410d75e367" />
<img width="641" height="391" alt="image" src="https://github.com/user-attachments/assets/fc05622f-ca5b-482d-b830-f2bb7fe530dc" />
<img width="633" height="194" alt="image" src="https://github.com/user-attachments/assets/24bb61a9-bb78-4a94-86f1-e967aad3bb46" />
<img width="672" height="391" alt="image" src="https://github.com/user-attachments/assets/dd89639d-bb14-4a5a-997a-c64b36cbbde7" />





---

## 🚀 주요 기능 (Features)

### 1. 종목 및 기간 선택
- yfinance를 사용해 아래 자산군 데이터를 자동으로 다운로드:
  - 암호화폐: `BTC-USD`, `ETH-USD`, `XRP-USD`, `LTC-USD` …
  - 미국 주식: `AAPL`, `MSFT`, `TSLA`, `NVDA`, `AMZN` …
  - 한국 주식: `005930.KS (삼성전자)` 등
  - 글로벌 지수/상품: `SPY`, `QQQ`, `GLD`, `VIX`
- 시작일 / 종료일을 UI에서 선택 후 데이터 로딩 (`st.cache_data` 로 캐싱)

### 2. 수동 파라미터 설정 기반 백테스트
- Streamlit 슬라이더로 전략 파라미터 조절:
  - `kr_window` : 커널 회귀 윈도우 길이
  - `kr_bandwidth` : 커널 회귀 대역폭
  - `bb_k` : 볼린저 밴드 계수
  - `rsi_period` : RSI 기간
  - `extrema_order` : 로컬 극값 탐지용 order
  - `rsi_oversold` / `rsi_overbought` : 과매도/과매수 기준
- 버튼 클릭 시:
  - 백테스트 실행
  - **최종 자산 / 수익률(%) 계산**
  - **매수·매도 거래 내역 테이블 출력**
  - 차트에 다음 정보 시각화:
    - 종가
    - 커널 회귀 예측선 (`y_pred`)
    - 변동성 밴드(`band`)
    - 매수/매도 시점(↑ / ↓ 마커)
    - 강세/약세 다이버전스 구간 (가격 + RSI)

### 3. Optuna 기반 파라미터 자동 최적화
- 목적 함수: **최종 수익률 최대화**
- Optuna로 아래 파라미터 탐색:
  - `kr_window`, `kr_bandwidth`, `bb_k`
  - `rsi_period`, `extrema_order`
  - `rsi_oversold`, `rsi_overbought`
- UI에서 `n_trials` 설정 후 최적화 실행
- 진행 상황을 실시간으로 표시:
  - `"i / n_trials 시도 완료"`
- 결과 출력:
  - 최적 파라미터(JSON)
  - 최대 수익률
  - 최적 파라미터로 다시 백테스트 및 차트 시각화

### 4. 한국 주식 전체 평균 수익률 계산기
- 사전에 정의된 한국 주식 리스트에 대해:
  - 동일 전략/동일 파라미터로 **상장일 ~ 2023-05-31** 구간 백테스트
  - 각 종목별 수익률을 집계 후 **평균 수익률 계산**
- 전체 결과 테이블 제공:
  - 종목명 / 티커 / 개별 수익률(%)

### 5. 대시보드 UI
- **사이드바**
  - 페이지 선택: `아키텍처`, `메인 페이지`, `평균 수익률 계산기`
  - 시작 자본금 입력
  - 종목 카테고리 / 종목 선택
- **한글 차트 렌더링**
  - `koreanize_matplotlib` 로 한글 폰트 깨짐 방지

---

## 🧱 아키텍처 & 코드 구조

```text
.
├── app.py                # Streamlit 앱 진입점, 페이지 라우팅
├── ui_components.py      # UI 구성 요소 (사이드바, 메인 페이지, 평균 수익률 페이지)
├── backtest_core.py      # 핵심 백테스트 로직 (전략, 시그널, 수익률 계산)
├── data_loader.py        # yfinance 데이터 로더 (@st.cache_data 적용)
├── requirements.txt      # 의존성 패키지 목록
└── README.md
