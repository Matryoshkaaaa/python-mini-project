# 📈 Kernel Regression Trading Strategy Backtesting Dashboard

<div align="center">

** 커널 회귀 기반 트레이딩 전략 실험 및 백테스팅 대시보드**

[![Python](https://img.shields.io/badge/Python-3.1+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Optuna](https://img.shields.io/badge/Optuna-0091EA?style=for-the-badge&logo=optuna&logoColor=white)](https://optuna.org/)

</div>

### 메인 대시보드
<img src="https://github.com/user-attachments/assets/70b2c566-6cb3-4ccc-9e74-8f6e29cd6663" width="800"/>

## 🎯 프로젝트 개요

주요 기술적 지표를 조합하여 매매 신호를 생성하고, 과거 데이터를 기반으로 전략의 성과를 검증할 수 있는 백테스팅 시스템입니다.  
Streamlit을 활용한 직관적인 웹 인터페이스로 누구나 쉽게 트레이딩 전략을 실험할 수 있습니다.

## ✨ 주요 기능

### 📊 데이터 로딩
- **yfinance** 통합으로 미국·한국 주식, 암호화폐 등 다양한 자산 데이터 조회
- Streamlit 캐싱을 통한 빠른 데이터 재조회
- 실시간 시장 데이터 접근

## ⚙️ 기술적 지표 기반 시그널 (Technical Indicators)

### **- Kernel Regression — 통계적 모델 기반 추세 추정**

비선형 가격 움직임을 **커널 회귀(Locally Weighted Regression)** 모델을 통해  
부드럽고 안정적으로 추정

- 단순 이동평균(SMA/EMA)과 달리 **데이터 구조에 따라 자동 가중치 적용**
- 단기·중기 추세를 **모델 기반으로 학습적으로 포착**
- 예측값 ± 변동성 밴드로 **과열/침체 구간을 정교하게 판단**
- 본 프로젝트 전략의 기반이 되는 **핵심 시그널 엔진**

---

### **- RSI Divergence — 과매수·과매도 국면에서의 반전 포착**

가격과 RSI의 움직임이 불일치할 때 발생하는  
**강세/약세 다이버전스**를 자동으로 탐지

- 가격 ↓ / RSI ↑ → **강세 다이버전스** (매수 신호)
- 가격 ↑ / RSI ↓ → **약세 다이버전스** (매도 신호)
- 반전 구간을 자동 라벨링하여 **매매 타이밍에 직접 반영**
- 시장 모멘텀 변화 감지에 효과적

---

### **- Bollinger Band — 변동성 기반 평균회귀 전략**

가격의 표준편차 기반 밴드를 통해  
현재 가격이 평균 대비 얼마나 과열/침체 상태인지 판단

- 상단 밴드 초과 → **과매수 가능성**
- 하단 밴드 이탈 → **과매도 가능성**
- 평균회귀(mean-reversion) 전략과 결합해 시그널 정확도 향상

---

### **- 복합 시그널 엔진 — 세 지표 조합 기반의 정교한 매매 판단**

커널 회귀 + RSI Divergence + Bollinger Band  
세 지표를 조합하여 단일 지표보다 훨씬 정교한 시그널을 생성

- **추세 + 모멘텀 + 변동성** 3가지 요소를 통합 분석
- 각각의 지표가 가지는 단점을 상호 보완
- 노이즈 제거 및 **매매 정확도 향상**
- 다양한 시장 환경 변화에도 유연하게 대응

---

<img src="https://github.com/user-attachments/assets/fc05622f-ca5b-482d-b830-f2bb7fe530dc" width="800"/>

<img src="https://github.com/user-attachments/assets/24bb61a9-bb78-4a94-86f1-e967aad3bb46" width="800"/>

### 🔄 자동화된 백테스트
- 매수/매도 시점 자동 기록 및 추적
- 실제 거래를 시뮬레이션한 수익률 계산
- 주요 지표와 신호의 통합 시각화
<img src="https://github.com/user-attachments/assets/4f6dd914-4d74-487c-a709-e6410d75e367" width="800"/>

### 🎯 파라미터 최적화
- **Optuna** Bayesian Optimization 엔진 탑재
- 수익률 기준 최적 파라미터 조합 자동 탐색
- 하이퍼파라미터 튜닝 간소화
<img src="https://github.com/user-attachments/assets/dd89639d-bb14-4a5a-997a-c64b36cbbde7" width="800"/>


### 📋 종목별 수익률 분석
- 다수 한국 주식에 대한 일괄 전략 적용
- 종목별 성과 비교 및 평균 수익률 산출
- 포트폴리오 레벨 인사이트 제공

## 🛠️ 기술 스택

| 영역 | 기술 |
|------|------|
| **Language** | Python 3.1+ |
| **Framework** | Streamlit |
| **Optimization** | Optuna |
| **Data Source** | yfinance |
| **Visualization** | Matplotlib |
| **Modeling** | statsmodels (Kernel Regression) |
| **Data Processing** | Pandas, NumPy |


## 📁 프로젝트 구조

```
.
├── 📄 app.py                # Streamlit 메인 실행 파일
├── 🎨 ui_components.py      # UI 모듈 (사이드바/메인 페이지/분석)
├── 🔧 backtest_core.py      # 전략·백테스트 핵심 로직
├── 📊 data_loader.py        # yfinance 데이터 로더 (캐싱)
└── 📖 README.md            # 프로젝트 문서
```

## 🖼️ 스크린샷

<details>
<summary>📸 대시보드 미리보기 (클릭하여 펼치기)</summary>











</details>

## 💡 사용 팁

- **데이터 로딩**: 초기 실행 시 데이터 다운로드에 시간이 소요될 수 있습니다
- **파라미터 조정**: 사이드바에서 각 지표의 파라미터를 실시간으로 조정 가능
- **최적화**: Optuna 최적화는 많은 시행 횟수를 설정할수록 더 나은 결과를 얻습니다
- **종목 추가**: `data_loader.py`에서 원하는 종목 리스트를 수정할 수 있습니다

## 🔧 기술적 특징

- **한글 폰트 지원**: Windows 환경에서 Malgun Gothic 폰트 자동 설정
- **모듈화 설계**: 각 기능별 파일 분리로 유지보수성 확보


