📈 Trading Strategy Backtesting Dashboard

본 프로젝트는 시계열 금융 데이터를 기반으로 간단한 트레이딩 전략을 실험하고 결과를 검토할 수 있는 백테스트 대시보드입니다.
Streamlit을 이용해 웹 UI를 구성하였으며, 주요 기술적 지표를 조합해 매매 신호를 생성하는 구조로 되어 있습니다.

1. 기능 요약

데이터 로딩

yfinance를 사용해 미국·한국 주식, 암호화폐 등 주요 자산의 가격 데이터를 조회

Streamlit 캐시를 적용하여 반복 조회 성능 개선

지표 기반 시그널 생성

Kernel Regression 기반 단순 추세 추정

RSI Divergence 감지

Bollinger Band 활용

세 지표를 조합한 매매 신호 산출

백테스트

매수/매도 시점 자동 기록

시뮬레이션 기반 수익률 및 최종 자산 계산

주요 지표와 신호를 함께 시각화

파라미터 최적화

Optuna를 사용한 간단한 Bayesian Optimization

수익률 기준 최적 조합 탐색

종목별 수익률 분석

지정한 한국 주식 리스트에 대해 동일 전략을 일괄 적용

종목별 수익률 및 평균 수익률 출력

2. 기술 스택
영역	사용 기술
Language	Python
Framework	Streamlit
Optimization	Optuna
Data	yfinance
Visualization	Matplotlib
Modeling	statsmodels (Kernel Regression)
Data Processing	Pandas, NumPy
3. 실행 방법
pip install -r requirements.txt
streamlit run app.py


접속 URL은 실행 환경에 따라 자동 생성됩니다.

4. 프로젝트 구조
.
├── app.py                # Streamlit 메인 실행 파일
├── ui_components.py      # UI 모듈 (사이드바/메인 페이지/분석 페이지)
├── backtest_core.py      # 전략·백테스트 로직
├── data_loader.py        # yfinance 데이터 로더 (캐싱 적용)
├── requirements.txt      
└── README.md

5. 시각화 예시

아래는 실제 실행 화면 일부입니다.

<img src="https://github.com/user-attachments/assets/70b2c566-6cb3-4ccc-9e74-8f6e29cd6663" width="900"/> <img src="https://github.com/user-attachments/assets/4f6dd914-4d74-487c-a709-e6410d75e367" width="900"/> <img src="https://github.com/user-attachments/assets/fc05622f-ca5b-482d-b830-f2bb7fe530dc" width="900"/> <img src="https://github.com/user-attachments/assets/24bb61a9-bb78-4a94-86f1-e967aad3bb46" width="900"/> <img src="https://github.com/user-attachments/assets/dd89639d-bb14-4a5a-997a-c64b36cbbde7" width="900"/>
6. 기타

Matplotlib에서 한글 깨짐을 방지하기 위해 Windows 환경 기준 Malgun Gothic 폰트를 직접 등록하여 사용합니다.

koreanize-matplotlib와 같은 외부 패키지는 사용하지 않습니다.
