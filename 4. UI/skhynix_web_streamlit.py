import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import datetime
import boto3
from PIL import Image
import requests
from io import BytesIO

# AWS 자격 증명을 코드 내에서 설정
aws_access_key_id = 'key'
aws_secret_access_key = 'secret key'
region_name = 'ap-northeast-2'  # 서울 리전

# S3 버킷과 폴더 정보
bucket_name = 'lcsa-test'
folder_path = 'final_ui/'
image_folder_path = folder_path + 'images/'

# S3 클라이언트 생성
s3 = boto3.client('s3',
                  aws_access_key_id='access key',
                  aws_secret_access_key='secret access key')

# 이미지 로드 함수
def load_image_from_s3(bucket, path):
    response = s3.get_object(Bucket=bucket, Key=path)
    img = Image.open(BytesIO(response['Body'].read()))
    return img

# 페이지 설정
page_icon_path = image_folder_path + 'sk_wing.png'
page_icon = load_image_from_s3(bucket_name, page_icon_path)
st.set_page_config(page_title="SK hynix MLOPS", page_icon=page_icon)

# CSV 파일 로드 함수
def load_csv_from_s3(bucket, path):
    response = s3.get_object(Bucket=bucket, Key=path)
    df = pd.read_csv(BytesIO(response['Body'].read()))
    return df

# 데이터 로드
csv_files = ['final_df.csv', 'result.csv', 'result2.csv']
df = load_csv_from_s3(bucket_name, folder_path + csv_files[0])
df1 = load_csv_from_s3(bucket_name, folder_path + csv_files[1])
df2 = load_csv_from_s3(bucket_name, folder_path + csv_files[2])


# 사이드바 설정
with st.sidebar:
    # 사이드바 메뉴 구성
    selected = option_menu("SK hynix", ["Dashboard", "Pump Failure Prediction", "Settings"],
                           icons=['clipboard-data', 'gear', 'wrench'],
                           menu_icon="building", default_index=0,
                           styles={
                               "container": {"padding": "5!important", "background-color": "#fafafa"},
                               "icon": {"color": "orange", "font-size": "25px"}, 
                               "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                               "nav-link-selected": {"background-color": "#02ab21"},
                           }
    )

############################################################
# 컬럼 이름 변경
df.rename(columns={
    'sequence': '고장 이후 공정진행횟수',
    'EQ_ID': 'EQ ID',
    'TA_tm_before': '최근 고장 알람 시간',
    'Last_change': '마지막 교체 시간',
    'WAFER_ID': 'Wafer'
}, inplace=True)

# EQ ID 값 포맷 변경
df['EQ ID'] = df['EQ ID'].apply(lambda x: f'EQ ID {x}')

# 상태 및 색상 열 추가
df['Status'] = df['diff_hours'].apply(lambda x: "Good" if x < 50 else "Warning" if x < 100 else "Critical")
df['Color'] = df['Status'].map({
    'Good': '#00FF00',   # Green for good condition
    'Warning': '#FFFF00', # Yellow for warning
    'Critical': '#FF0000' # Red for critical
})

# 현재 시간 표시 (화면 오른쪽 상단)
st.markdown(f"<div style='float: right; border: 3px solid #FF7F50; padding: 8px; border-radius: 8px; font-weight: bold;'>현재시간: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)

###################################################################

# 시간 데이터 파싱
df1['start_dt_tm'] = pd.to_datetime(df1['start_dt_tm'])
df2['start_dt_tm'] = pd.to_datetime(df2['start_dt_tm'])

# 열 이름 확인
#st.write(df1.columns)
#st.write(df2.columns)

# 데이터 프레임 병합
df1['interval'] = 'Interval 1'
df2['interval'] = 'Interval 2'
df3 = pd.concat([df1, df2])

# 두 구간의 경계 시간 계산(회색선 그리려고)
boundary_time = df2['start_dt_tm'].min()


# 중앙 정렬을 위한 스타일 설정
st.markdown("""
    <style>
    .center-label > div > label {
        display: flex;
        justify-content: center;
    }
    .center-text {
        text-align: center;
    }
    .section-spacing {
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .subsection-spacing {
        margin-top: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


####################################################################

# 페이지 내용에 따른 조건부 렌더링
if selected == "Dashboard":
       
    st.title("Fail Prediction Dashboard")
    st.write("Here you can view the overall failure prediction.")
    st.markdown("<div style='height: 3px; background-color: #f0f0f0; margin: 10px 0;'></div>", unsafe_allow_html=True)
# SK 하이닉스 색상 : #FF4500

    # Pump Status 섹션
    st.markdown('<div class="header-center">', unsafe_allow_html=True)
    st.header("Pump Status")
    st.markdown('</div>', unsafe_allow_html=True)
    cols = st.columns([1, 1, 1, 1, 1])
    for i, row in df.iterrows():
        with cols[1 if i == 0 else 3]:  # EQ ID 1 in 2/5 위치, EQ ID 2 in 4/5 위치
            #st.subheader(f"{row['EQ ID']}")
            if row['diff_hours'] < 50:
                # Smile SVG from Bootstrap
                emoji_svg = '''
                <svg xmlns="http://www.w3.org/2000/svg" width="150" height="150" fill="#00FF00" class="bi bi-emoji-smile" viewBox="0 0 16 16">
                  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                  <path d="M4.285 9.567a.5.5 0 0 1 .683.183A3.5 3.5 0 0 0 8 11.5a3.5 3.5 0 0 0 3.032-1.75.5.5 0 1 1 .866.5A4.5 4.5 0 0 1 8 12.5a4.5 4.5 0 0 1-3.898-2.25.5.5 0 0 1 .183-.683M7 6.5C7 7.328 6.552 8 6 8s-1-.672-1-1.5S5.448 5 6 5s1 .672 1 1.5m4 0c0 .828-.448 1.5-1 1.5s-1-.672-1-1.5S9.448 5 10 5s1 .672 1 1.5"/>
                </svg>
                '''
                status_text = "Status: Good 😊"
                color = "#00FF00"
            else:
                # Angry SVG from Bootstrap
                emoji_svg = '''
                <svg xmlns="http://www.w3.org/2000/svg" width="150" height="150" fill="#FF0000" class="bi bi-emoji-angry" viewBox="0 0 16 16">
                  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                  <path d="M4.285 12.433a.5.5 0 0 0 .683-.183A3.5 3.5 0 0 1 8 10.5c1.295 0 2.426.703 3.032 1.75a.5.5 0 0 0 .866-.5A4.5 4.5 0 0 0 8 9.5a4.5 4.5 0 0 0-3.898 2.25.5.5 0 0 0 .183.683m6.991-8.38a.5.5 0 1 1 .448.894l-1.009.504c.176.27.285.64.285 1.049 0 .828-.448 1.5-1 1.5s-1-.672-1-1.5c0-.247.04-.48.11-.686a.502.502 0 0 1 .166-.761zm-6.552 0a.5.5 0 0 0-.448.894l1.009.504A1.94 1.94 0 0 0 5 6.5C5 7.328 5.448 8 6 8s1-.672 1-1.5c0-.247-.04-.48-.11-.686a.502.502 0 0 0-.166-.761z"/>
                </svg>
                '''
                status_text = "Status: Critical 😟"
                color = "#FF0000"

            st.markdown(f"<div style='text-align: center; margin-bottom: 10px;'><div style='font-size: 24px;'>{row['EQ ID']}</div>{emoji_svg}<div style='margin-top: 9px;'>{status_text}</div></div>", unsafe_allow_html=True)

    # Status 오른쪽 옆 상태 설명 : 표의 legend처럼
    st.markdown("""
    <div style='text-align: right;'>
        <span style='color: #00FF00;'>Good: 수명이 50시간 이상</span><br>
        <span style='color: #FF0000;'>Critical: 수명이 50시간 미만</span>
    </div>
    """, unsafe_allow_html=True)
    

    # 구분선(회색)
    st.text('')
    st.text('')
    st.markdown("<div style='height: 3px; background-color: #f0f0f0; margin: 20px 0;'></div>", unsafe_allow_html=True)
    st.text('')
    # Fail Prediction Details 섹션 표
    st.markdown('<div class="header-center">', unsafe_allow_html=True)
    st.header("Fail Prediction Status")
    st.markdown('</div>', unsafe_allow_html=True)

    column_order = ['EQ ID', '고장 이후 공정진행횟수', '최근 고장 알람 시간', '마지막 교체 시간', 'Wafer']
    df = df[column_order]
    df_display = df[column_order]
    st.table(df_display.style.set_properties(**{'text-align': 'center'}))


    # 구분선(회색)
    st.text('')
    st.text('')
    st.markdown("<div style='height: 2px; background-color: #f0f0f0; margin: 20px 0;'></div>", unsafe_allow_html=True)

    st.text('')
    st.text('')
    st.header("Cost Status")

    # 첫 번째 표
    st.markdown("<div class='section-spacing' style='font-size: 20px; font-weight: bold; text-align: center;'>[ 비용 및 주기 입력 ]</div>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div style='text-align: center; font-weight: bold;'>기준 비용</div>", unsafe_allow_html=True)
        with st.container():
            std_cost = st.number_input("대당수리비용", value=100)
            std_wf_loss = st.number_input("대당고장시 WFLoss 비용", value=500)
            std_avg_duration = st.number_input("평균고장주기", value=30)
        st.write(f"<div class='center-text'>총 비용: <span style='color: #00FF00;'>{round(std_cost / std_avg_duration + std_wf_loss / std_avg_duration, 2)} 원/(일*대)</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='text-align: center; font-weight: bold;'>과잉 정비</div>", unsafe_allow_html=True)
        with st.container():
            over_maint_cost = st.number_input("대당수리비용", value=100, key="over_maint_cost")
            over_success_wf_loss = st.number_input("대당고장시 WFLoss 비용", value=0, key="over_success_wf_loss")
            over_maint_duration = st.number_input("평균수리주기", value=20, key="over_maint_duration")
        st.write(f"<div class='center-text'>총 비용: <span style='color: #00FF00;'>{round(over_maint_cost / over_maint_duration, 2)} 원/(일*대)</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='text-align: center; font-weight: bold;'>예측 성공</div>", unsafe_allow_html=True)
        with st.container():
            pred_success_cost = st.number_input("대당수리비용", value=100, key="pred_success_cost")
            pred_success_wf_loss = st.number_input("대당고장시 WFLoss 비용", value=0, key="pred_success_wf_loss")
            pred_success_duration = st.number_input("평균수리주기", value=30, key="pred_success_duration")
        st.write(f"<div class='center-text'>총 비용: <span style='color: #00FF00;'>{round(pred_success_cost / pred_success_duration + pred_success_wf_loss / pred_success_duration, 2)} 원/(일*대)</span></div>", unsafe_allow_html=True)

    # 두 번째 표
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown("<div class='section-spacing' style='font-size: 20px; font-weight: bold; text-align: center;'>[ AI 모델 별 비용 분석 ]</div>", unsafe_allow_html=True)
    st.text('')

    cols = st.columns(5)
    cases = ["AI 모델 미적용", "딥러닝 모델", "딥러닝 모델 앙상블", "머신러닝 모델", "머신러닝+딥러닝 모델"]
    case_data = {case: {} for case in cases}
    total_intervals = 25

    for i, case in enumerate(cases):
        with cols[i]:
            st.markdown(f"<div class='subsection-spacing' style='text-align: center; font-weight: bold;'>{case}</div>", unsafe_allow_html=True)
            with st.container():
                case_data[case]["기준비용 건수"] = st.number_input(f"기준비용 건수", value=0, key=f"std_{case}")
                case_data[case]["기준비용 비율"] = case_data[case]["기준비용 건수"] / total_intervals
                case_data[case]["과잉정비 건수"] = st.number_input(f"과잉정비 건수", value=0, key=f"over_{case}")
                case_data[case]["과잉정비 비율"] = case_data[case]["과잉정비 건수"] / total_intervals
                case_data[case]["예측성공 건수"] = st.number_input(f"예측성공 건수", value=0, key=f"pred_{case}")
                case_data[case]["예측성공 비율"] = case_data[case]["예측성공 건수"] / total_intervals

            st.write(f"<div class='center-text'>기준비용 비율: {case_data[case]['기준비용 비율']:.2f}</div>", unsafe_allow_html=True)
            st.write(f"<div class='center-text'>과잉정비 비율: {case_data[case]['과잉정비 비율']:.2f}</div>", unsafe_allow_html=True)
            st.write(f"<div class='center-text'>예측성공 비율: {case_data[case]['예측성공 비율']:.2f}</div>", unsafe_allow_html=True)

            total_cost = round(
                std_cost / std_avg_duration * case_data[case]['기준비용 비율'] +
                std_wf_loss / std_avg_duration * case_data[case]['기준비용 비율'] +
                over_maint_cost / over_maint_duration * case_data[case]['과잉정비 비율'] +
                pred_success_cost / pred_success_duration * case_data[case]['예측성공 비율'] +
                pred_success_wf_loss / pred_success_duration * case_data[case]['예측성공 비율'], 2
            )

            st.write(f"<div class='center-text'>총 비용: <span style='color: #00FF00;'>{total_cost} 원/(일*대)</span></div>", unsafe_allow_html=True)

    st.text('')
    total_cost_all = sum(
        std_cost / std_avg_duration * case_data[case]['기준비용 비율'] +
        std_wf_loss / std_avg_duration * case_data[case]['기준비용 비율'] +
        over_maint_cost / over_maint_duration * case_data[case]['과잉정비 비율'] +
        pred_success_cost / pred_success_duration * case_data[case]['예측성공 비율'] +
        pred_success_wf_loss / pred_success_duration * case_data[case]['예측성공 비율'] for case in cases
    )
    total_cost_all = round(total_cost_all, 2)
    st.text('')
    st.markdown(f"<div class='total-cost' style='text-align: center; border: 2px solid #FFA500; padding: 10px; border-radius: 5px; font-weight: bold; color: #FFA500;'>총 비용: {total_cost_all} 원/(일*대)</div>", unsafe_allow_html=True)

############################################################################


elif selected == "Pump Failure Prediction":
    st.title("Pump Failure Prediction")
    st.write("Detailed analysis of pump failure predictions.")
    st.markdown("<div style='height: 3px; background-color: #f0f0f0; margin: 10px 0;'></div>", unsafe_allow_html=True)

    # 구분선 대신 UI 요소 변경
    st.text('')
    #st.markdown("<div style='height: 6px; background-color: #f0f0f0; margin: 10px 0;'></div>", unsafe_allow_html=True)
    st.text('')

    # Select Box 추가
    st.text('')
    st.markdown("<div style='font-size: 32px; font-weight: bold; text-align: center;'>Select Fail to Fail Interval</div>", unsafe_allow_html=True)
    selected_interval = st.selectbox("", [f"Interval {i}" for i in range(1, 26)])

    # 각 구간의 데이터를 필터링
    intervals = df3['interval'].unique()

    # 그래프 생성
    fig = go.Figure()

    colors = {'Interval 1': 'blue', 'Interval 2': 'green'}
    for interval in intervals:
        interval_data = df3[df3['interval'] == interval]
        fig.add_trace(go.Scatter(x=interval_data['start_dt_tm'], y=interval_data['pred'],
                                 mode='markers', name=f'{interval} RUL', marker=dict(color=colors[interval])))

    # 회색 선 추가 (구간 사이)
    fig.add_shape(type="line",
                  x0=boundary_time, y0=0, x1=boundary_time, y1=max(df3['pred'].max(), df3['true'].max()),
                  line=dict(color="gray", width=1, dash="dash"))

    # 그래프 레이아웃 설정
    fig.update_layout(
        title={
            'text': "RUL Prediction Graph",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Date',
        yaxis_title='Remaining Life Hours',
        legend_title='Graph',
        title_font=dict(size=20, family='Arial', color='black'),
        autosize=True,
        width=1450,
        height=700
    )

    # 그래프 가운데 정렬을 위한 HTML 스타일
    st.markdown("""
        <style>
        .center {
            display: flex;
            justify-content: center;
        }
        .plotly_chart {
            margin: auto;
        }
        </style>
        """, unsafe_allow_html=True)

    # 그래프 표시
    st.markdown('<div class="center">', unsafe_allow_html=True)
    st.plotly_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)

    # 마지막 업데이트 시간 설정
    last_update_time = df3['start_dt_tm'].max().strftime('%Y-%m-%d %H:%M:%S')

    # 마지막 업데이트 시간 표시
    st.markdown(f"<div style='text-align: right; font-size: 16px;font-weight: bold;'>updated {last_update_time}</div>", unsafe_allow_html=True)


    # 구분선(회색)
    st.text('')
    st.markdown("<div style='height: 3px; background-color: #f0f0f0; margin: 20px 0;'></div>", unsafe_allow_html=True)

##################################

    #  Metric 데이터 생성 및 mlflow에서 받아오기
    st.text('')
    metrics_data = {
        'Metric': ['Fail to Fail 27', 'Fail to Fail 11', 'Fail to Fail 1', 'Fail to Fail 31'],
        'Min-Max Weighted RMSE': [mlflow에서 metric 받아오기]],
        'Weighted RMSE': [mlflow에서 metric 받아오기],
        'MSE': [mlflow에서 metric 받아오기],
        'MAE': [mlflow에서 metric 받아오기],
        'RMSE': [mlflow에서 metric 받아오기]
    }
    
    metric_df = pd.DataFrame(metrics_data)

    # Metric 선택 박스
    st.markdown("<div style='font-size: 32px; font-weight: bold; text-align: center;'>Compare Metric</div>", unsafe_allow_html=True)
    st.text('')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='font-size: 20px; font-weight: bold; text-align: center;'>Metric 1</div>", unsafe_allow_html=True)
        metric1 = st.selectbox('', ['Min-Max Weighted RMSE', 'Weighted RMSE', 'MSE', 'MAE', 'RMSE'], key='metric1')
    with col2:
        st.markdown("<div style='font-size: 20px; font-weight: bold; text-align: center;'>Metric 2</div>", unsafe_allow_html=True)
        metric2 = st.selectbox('', ['Min-Max Weighted RMSE', 'Weighted RMSE', 'MSE', 'MAE', 'RMSE'], key='metric2')

    col1, col2 = st.columns(2)
    with col1:
        fig1 = go.Figure(go.Bar(
            y=metric_df['Metric'],
            x=metric_df[metric1],
            text=metric_df[metric1],
            textposition='auto',
            orientation='h',
            name=metric1
        ))

        fig1.update_layout(
            xaxis_title='Value',
            yaxis_title='Metric',
            autosize=True
        )

        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = go.Figure(go.Bar(
            y=metric_df['Metric'],
            x=metric_df[metric2],
            text=metric_df[metric2],
            textposition='auto',
            orientation='h',
            name=metric2
        ))

        fig2.update_layout(
            xaxis_title='Value',
            yaxis_title='Metric',
            autosize=True
        )

        st.plotly_chart(fig2, use_container_width=True)



##################################################################################

elif selected == "Settings":
    st.title("Log In/Sign Up")
    st.text('')
    st.write("로그인 및 회원가입을 진행해주세요.")
    st.text('')  # 로그인 버튼 위의 공간

    with st.form("login_form"):
        st.write("로그인")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            st.success("Login successful for user: " + username)

    st.text('')
    with st.form("signup_form"):
        st.write("회원가입")
        new_username = st.text_input("New username", key="new_username")
        new_password = st.text_input("New password", type="password", key="new_password")
        confirm_password = st.text_input("Confirm password", type="password", key="confirm_password")
        signup_submitted = st.form_submit_button("Sign Up")
        if signup_submitted:
            if new_password == confirm_password:
                st.success("회원가입이 성공적으로 완료되었습니다!")
            else:
                st.error("비밀번호가 일치하지 않습니다.")