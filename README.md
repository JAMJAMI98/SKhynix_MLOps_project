<div align="center">
  <img width="30%" alt="SKhynix_logo" src="https://github.com/JAMJAMI98/SKhynix_MLOps_project/assets/94438552/7dd73b3e-6598-4efb-9c26-e90202d1bf1a" title="SKhynix logo">
  <br/>
  <h3 align="center">SmartFactory 운영을 위한 Subcomponent Fail Prediction MLOps 개발</h3>
  <p align="center">
    <a href="https://github.com/JAMJAMI98">현재민</a> · 이승규 · 박소정 · 정대훈
  </p>
  <p align="center">
    2024.03 ~ 2024.05 | SK planet T-academy
    <br/>
    🥇 1st Place in T-academy and SK hynix Business linkage Program
    <br/><br/>
    <a href="https://www.youtube.com/watch?v=0lnuD3EgGe4&list=RDCMUCtV98yyffjUORQRGTuLHomw&start_radio=1" target="_blank">
      <img width="40%" alt="youtube" src="https://github.com/JAMJAMI98/SKhynix_MLOps_project/assets/94438552/1a601a0d-e025-4844-a75b-529497115654" title="MLOops Presentation">
    </a>
  </p>
</div>


<!-- INDEX OF CONTENTS -->
<details>
  <summary>Index of Contents</summary>
  <ul>
    <li>
      Overview</a>
      <ul>
        <li>Service Component</a></li>
        <li>Short Video</a></li>
      </ul>
    </li>
    <li>Built With</a></li>
    <li>Backgroud</a></li>
    <li>MLOps pipeline</a></li>
    <li>Data Preprocessing</a></li>
    <li>Modeling</a></li>
    <li>Conclusion</a></li>
  </ul>
</details>

<br>

## 📝 Overview
### 💡 Service Component
- 고장예측 대시보드 (Fail Prediction Dashboard): Pump Status, Fail Prediction Status, Cost Status
- 펌프 고장 예측 (Pump Failure Prediction): RUL Prediction Graph, Compare Metric
- 로그인 및 회원가입 (LogIn/SignUp)

### 💡 Short Video
<div align="center">
  <video src="https://github.com/JAMJAMI98/SKhynix_MLOps_project/assets/94438552/c23edf01-9783-4be6-bde2-2e5b2daf820a" data-canonical-src="https://github.com/JAMJAMI98/SKhynix_MLOps_project/assets/94438552/c23edf01-9783-4be6-bde2-2e5b2daf820a" controls="controls" muted="muted" style="max-height:640px;">
  </video>
</div>

<br/>

## ⭐️ Built With
- [Python](https://www.python.org/)
- [HTML/JS/CSS](https://getbootstrap.kr/)
- [Amazon Web Services: EC2, S3, Lambda, Cloud Watch, RDS, SSM](https://aws.amazon.com/ko/)
- [MLflow](https://mlflow.org/)
- [Streamlit](https://streamlit.io/)
- [Keras](https://keras.io/)
- [TensorFlow](https://www.tensorflow.org/?hl=ko)
- [PyTorch](https://pytorch.org/)
- [Prophet](https://facebook.github.io/prophet/)
- [Scikit-learn](https://scikit-learn.org/stable/)
- [Python Libary: pandas, Numpy, matplotlib, SciPy](https://docs.python.org/ko/3/library/index.html)
- [Jira](https://www.atlassian.com/ko/software/jira)

<br/>

## ⭐️ Background
### 1. 기획 배경
- 스마트팩토리의 효율적인 운영을 위해 설비 고장을 사전에 예측하는 **예지 정비(Predictive Maintenance)** 솔루션 필수적
- 공장 내 설비의 고장은 생산 라인의 비가동 시간(downtime)을 초래하여 기업에 막대한 손실을 초래
- 많은 기업들이 설비 데이터를 기반으로 통계 분석과 AI 기술을 활용하여 이상치를 탐지하고, 고장을 예측하는 예지 정비 시행
- 제조업에서 핵심 자산인 설비의 **유지보수와 관련된 예측 모델이 비용 절감과 생산성 향상** 필요

### 2. 목적
- SK하이닉스의 스마트팩토리 운영을 위해 주요 부품의 고장을 사전에 예측할 수 있는 MLOps 시스템 개발
- 제조 환경에서는 장애 이력 데이터의 수집과 관리가 어렵기 때문에 **단순한 이상 감지가 아닌 정확한 장애 시점 예측**
- 최신 머신러닝 및 딥러닝 기법을 활용하여 **Remaining Useful Life(RUL)를 예측하고, RUL이 임계값 이하로 떨어지면 사전에 알람을 발생**시켜 고장을 예방하고자 함
- SOTA(State of the Art) 모델을 비교 분석하여 최적의 성능을 가진 모델 채택 및 RMSE, MAE, MSE 외의 고장 예측의 실시간성과 정확성을 높이기 위해 **특별히 설계한 새로운 성능 지표**를 도입하여 모델의 정확성 평가

### 3. MLOps 도입 필요성
- **데이터 처리 자동화**: 펌프 등의 장비에서 매초마다 데이터가 쌓이고 업데이트 되는데, 이를 모두 사람이 직접 처리하고 모델링하여 적용하는 것은 한계가 있음
- **지속적 모델 개선**: 모든 과정을 자동화하고 최적화하는 MLOps를 구현함으로써 모델의 지속적 개선과 안정적 운영이 가능
- **복잡한 운영 환경 대응**: 스마트팩토리의 복잡한 운영 환경에서 MLOps가 효과적으로 작동하면 더 큰 효율성을 얻을 수 있음

👉🏻 기존의 수동적이고 사후 대응 방식에서 벗어나, 실시간 데이터 분석과 예측을 통한 선제적 대응 체계를 구축하여 공장 운영의 효율성과 안정성을 높이고자 함

<br/>

## ⭐️ MLOps pipeline
<div align="center">
  <img width="55%" alt="pipeline" src="https://github.com/JAMJAMI98/SKhynix_MLOps_project/assets/94438552/d669da64-ff9c-4a04-bc5d-41f979c970f4">
</div>

<br/>

<div align="center">
  <img width="55%" alt="database_ERD" src="https://github.com/JAMJAMI98/SKhynix_MLOps_project/assets/94438552/0a2446a1-d977-4bf4-ac3b-96756245eba2">
</div>


<br/>

## ⭐️ Data Preprocessing
### 1. Data set
<div align="center">
  <img width="55%" alt="dataset" src="https://github.com/JAMJAMI98/SKhynix_MLOps_project/assets/94438552/e77a765a-0464-47cb-a58c-a5fbfa6d8d69">
</div>



<br/>

## ⭐️ Modeling


<br/>

## ⭐️ Conclusion



