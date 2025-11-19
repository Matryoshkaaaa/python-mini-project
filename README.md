# 📈 AI 기반 트레이딩 전략 최적화 & 백테스트 대시보드

**커널 회귀(Kernel Regression)**, **RSI 다이버전스**, **볼린저 밴드(Bollinger Band)**  
세 가지 기술적 지표를 조합하여 트레이딩 전략을 자동 최적화·시각화하는 Streamlit 기반 웹 애플리케이션입니다.

Optuna 기반 **베이지안 최적화**를 적용하여  
가장 높은 수익률을 만드는 파라미터 조합을 자동으로 탐색합니다.

---

## 🚀 주요 기능

### 🔍 1. 실시간 데이터 다운로드
- yfinance 기반 주가 데이터 자동 다운로드  
- 미국/한국 주식 + 암호화폐 + 글로벌 지수 지원  
- Streamlit 캐싱 적용 → 빠른 로딩 속도

---

### 📊 2. 기술적 지표 기반 전략
#### ✔ 커널 회귀(Kernel Regression)
- 비선형 추세를 매끄럽게 추정
- 예측값 ± 변동성 밴드로 매매 타이밍 판단

#### ✔ RSI 다이버전스 탐지
- 가격은 하락하지만 RSI는 상승(강세 다이버전스)  
- 가격은 상승하지만 RSI는 하락(약세 다이버전스)  
- 자동 매수/매도 신호 반영

#### ✔ 볼린저 밴드
- 변동성 기반의 추세 벗어남 감지  
- 평균회귀 전략과 잘 결합

---

### 🧪 3. 백테스트 엔진
- 매수/매도 거래 내역 자동 기록  
- 수익률·최종 자산 자동 계산  
- RSI + 커널 회귀 + 볼린저 신호 결합 전략 수행

---

### 🤖 4. Optuna 자동 최적화
- Bayesian Optimization  
- 최대 수익률을 만드는 파라미터 조합 자동 검색  
- 진행률 표시 + 결과 요약 제공

---

### 🇰🇷 5. 한국 주식 전체 평균 수익률 분석
- 18개 한국 대형 종목 백테스트 자동 수행  
- 종목별 개별 수익률 + 평균 수익률 출력  
- 진행 상황 실시간 표시

---

## 🖥️ 실행 화면

<img src="https://github.com/user-attachments/assets/70b2c566-6cb3-4ccc-9e74-8f6e29cd6663" width="900"/>
<img src="https://github.com/user-attachments/assets/4f6dd914-4d74-487c-a709-e6410d75e367" width="900"/>
<img src="https://github.com/user-attachments/assets/fc05622f-ca5b-482d-b830-f2bb7fe530dc" width="900"/>
<img src="https://github.com/user-attachments/assets/24bb61a9-bb78-4a94-86f1-e967aad3bb46" width="900"/>
<img src="https://github.com/user-attachments/assets/dd89639d-bb14-4a5a-997a-c64b36cbbde7" width="900"/>

---

---


## 📝 기술 스택

| 기술 | 사용 목적 |
|------|------------|
| **Python 3.11** | 안정적 AI/백테스트 라이브러리 호환 |
| **Streamlit** | 실시간 대시보드 UI |
| **Optuna** | 베이지안 최적화 |
| **statsmodels** | Kernel Regression |
| **yfinance** | 시계열 데이터 수집 |
| **matplotlib** | 시각화 |
| **NumPy / Pandas** | 데이터 처리 |

---

## 🈶 한글 폰트 처리
koreanize-matplotlib 대신 **로컬 폰트 직접 등록 방식** 사용.

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = r"C:\Windows\Fonts\malgun.ttf"
fm.fontManager.addfont(font_path)
plt.rcParams["font.family"] = fm.FontProperties(fname=font_path).get_name()
plt.rcParams["axes.unicode_minus"] = False

## 🧱 아키텍처 & 코드 구조

```text
.
├── app.py                # Streamlit 앱 진입점, 페이지 라우팅
├── ui_components.py      # UI 구성 요소 (사이드바, 메인 페이지, 평균 수익률 페이지)
├── backtest_core.py      # 핵심 백테스트 로직 (전략, 시그널, 수익률 계산)
├── data_loader.py        # yfinance 데이터 로더 (@st.cache_data 적용)
├── requirements.txt      # 의존성 패키지 목록
└── README.md
