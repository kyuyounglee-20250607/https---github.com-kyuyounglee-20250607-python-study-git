# pip install streamlit
# streamlit run [py파일명]
# 서울시 상권분석 & 지하철 실시간 대시보드
# Streamlit을 활용한 인터랙티브 대시보드

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="서울시 데이터 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 한글 폰트 설정
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 환경변수 로드
load_dotenv()

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Seoul_logo.svg/200px-Seoul_logo.svg.png", width=150)
    st.title("🏙️ 서울시 데이터")
    st.markdown("---")
    
    menu = st.radio(
        "메뉴 선택",
        ["📊 상권분석", "🚇 지하철 실시간", "📈 통합 분석"],
        index=0
    )
    
    st.markdown("---")
    st.info("💡 서울시 공공데이터를 활용한 실시간 대시보드입니다.")
    
    # 마지막 업데이트 시간
    st.caption(f"⏰ 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 메인 헤더
st.markdown('<div class="main-header">🌆 서울시 데이터 분석 대시보드</div>', unsafe_allow_html=True)

# 데이터 로드 함수 (캐싱)
@st.cache_data(ttl=3600)
def load_store_data():
    """상권분석 데이터 로드"""
    try:
        df = pd.read_csv('6.openapi_seoul/seoul_store.csv', encoding='cp949')
        return df
    except:
        try:
            df = pd.read_csv('seoul_store.csv', encoding='cp949')
            return df
        except Exception as e:
            st.error(f"데이터 로드 실패: {e}")
            return None

@st.cache_data(ttl=60)
def fetch_subway_data(station_name):
    """지하철 실시간 데이터 조회"""
    key = os.getenv("SEOUL_SUBWAY_API")
    if not key:
        return None
    
    url = f'http://swopenAPI.seoul.go.kr/api/subway/{key}/json/realtimeStationArrival/0/100/{station_name}'
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# ==========================================
# 1. 상권분석 대시보드
# ==========================================
if menu == "📊 상권분석":
    st.header("📊 서울시 상권분석 데이터")
    
    # 데이터 로드
    df = load_store_data()
    
    if df is not None:
        # 주요 지표 표시
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📍 총 업종 수",
                value=f"{df['서비스_업종_코드_명'].nunique():,}개"
            )
        
        with col2:
            total_sales = df['당월_매출_금액'].sum()
            st.metric(
                label="💰 총 매출액",
                value=f"{total_sales/1e12:.2f}조원"
            )
        
        with col3:
            total_count = df['당월_매출_건수'].sum()
            st.metric(
                label="🧾 총 거래 건수",
                value=f"{total_count/1e6:.1f}백만건"
            )
        
        with col4:
            avg_sales = df['당월_매출_금액'].mean()
            st.metric(
                label="📊 평균 매출",
                value=f"{avg_sales/1e9:.1f}억원"
            )
        
        st.markdown("---")
        
        # 탭 구성
        tab1, tab2, tab3 = st.tabs(["📈 업종별 분석", "📅 요일별 분석", "⏰ 시간대별 분석"])
        
        with tab1:
            st.subheader("업종별 매출 상위 10개")
            
            # 상위 10개 업종
            top10 = df.groupby('서비스_업종_코드_명')['당월_매출_금액'].sum().nlargest(10).reset_index()
            
            # Plotly 인터랙티브 차트
            fig = px.bar(
                top10,
                x='당월_매출_금액',
                y='서비스_업종_코드_명',
                orientation='h',
                title='업종별 당월 매출 상위 10개',
                labels={'당월_매출_금액': '매출액 (원)', '서비스_업종_코드_명': '업종'},
                color='당월_매출_금액',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # 파이 차트
            col1, col2 = st.columns(2)
            
            with col1:
                fig_pie = px.pie(
                    top10,
                    values='당월_매출_금액',
                    names='서비스_업종_코드_명',
                    title='업종별 매출 비율'
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # 데이터 테이블
                st.dataframe(
                    top10.style.format({'당월_매출_금액': '{:,.0f}원'}),
                    use_container_width=True,
                    height=400
                )
        
        with tab2:
            st.subheader("요일별 매출 패턴 분석")
            
            # 상위 5개 업종 선택
            top5_industries = df.groupby('서비스_업종_코드_명')['당월_매출_금액'].sum().nlargest(5).index.tolist()
            
            selected_industries = st.multiselect(
                "분석할 업종 선택 (최대 5개)",
                top5_industries,
                default=top5_industries[:3]
            )
            
            if selected_industries:
                df_selected = df[df['서비스_업종_코드_명'].isin(selected_industries)]
                
                # 요일별 컬럼
                weekday_cols = ['월요일_매출_금액', '화요일_매출_금액', '수요일_매출_금액', 
                               '목요일_매출_금액', '금요일_매출_금액', '토요일_매출_금액', '일요일_매출_금액']
                
                weekday_data = []
                for industry in selected_industries:
                    df_ind = df_selected[df_selected['서비스_업종_코드_명'] == industry]
                    for col in weekday_cols:
                        weekday_data.append({
                            '업종': industry,
                            '요일': col.replace('_매출_금액', ''),
                            '매출액': df_ind[col].sum()
                        })
                
                df_weekday = pd.DataFrame(weekday_data)
                
                # 라인 차트
                fig = px.line(
                    df_weekday,
                    x='요일',
                    y='매출액', 
                    color='업종',
                    markers=True,
                    title='업종별 요일별 매출 추이'
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("시간대별 매출 패턴 분석")
            
            # 시간대별 컬럼
            time_cols = ['시간대_00~06_매출_금액', '시간대_06~11_매출_금액', '시간대_11~14_매출_금액',
                        '시간대_14~17_매출_금액', '시간대_17~21_매출_금액', '시간대_21~24_매출_금액']
            
            # 전체 시간대별 매출
            time_data = []
            for col in time_cols:
                time_data.append({
                    '시간대': col.replace('시간대_', '').replace('_매출_금액', ''),
                    '매출액': df[col].sum()
                })
            
            df_time = pd.DataFrame(time_data)
            
            # 바 차트
            fig = px.bar(
                df_time,
                x='시간대',
                y='매출액',
                title='전체 업종 시간대별 매출',
                color='매출액',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.error("⚠️ 상권분석 데이터를 불러올 수 없습니다. seoul_store.csv 파일을 확인하세요.")

# ==========================================
# 2. 지하철 실시간 대시보드
# ==========================================
elif menu == "🚇 지하철 실시간":
    st.header("🚇 서울 지하철 실시간 도착정보")
    
    # 2호선 역 리스트
    line2_stations = [
        "시청", "을지로입구", "을지로3가", "을지로4가", "동대문역사문화공원", "신당", "상왕십리",
        "왕십리", "한양대", "뚝섬", "성수", "건대입구", "구의", "강변", "잠실나루", "잠실",
        "잠실새내", "종합운동장", "삼성", "선릉", "역삼", "강남", "교대", "서초", "방배", 
        "사당", "낙성대", "서울대입구", "봉천", "신림", "신대방", "구로디지털단지", "대림",
        "신도림", "문래", "영등포구청", "당산", "합정", "홍대입구", "신촌", "이대", "아현",
        "충정로"
    ]
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_station = st.selectbox(
            "🚉 역 선택",
            line2_stations,
            index=21  # 강남역 기본값
        )
        
        if st.button("🔄 새로고침", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        st.info(f"📍 선택된 역: **{selected_station}역** (2호선)")
    
    # 실시간 데이터 조회
    data = fetch_subway_data(selected_station)
    
    if data and 'realtimeArrivalList' in data:
        arrivals = data['realtimeArrivalList']
        
        if arrivals:
            st.success(f"✅ {len(arrivals)}개의 열차 정보를 찾았습니다.")
            
            # 실시간 정보 카드
            for i, train in enumerate(arrivals[:6], 1):  # 최대 6개 표시
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 2, 3, 2])
                    
                    with col1:
                        st.markdown(f"### 🚇 열차 {i}")
                        st.caption(train['trainLineNm'])
                    
                    with col2:
                        arrival_time = int(train['barvlDt'])
                        minutes = arrival_time // 60
                        seconds = arrival_time % 60
                        
                        if minutes == 0:
                            time_display = f"{seconds}초"
                            color = "🔴"
                        elif minutes < 3:
                            time_display = f"{minutes}분 {seconds}초"
                            color = "🟡"
                        else:
                            time_display = f"{minutes}분 {seconds}초"
                            color = "🟢"
                        
                        st.markdown(f"### {color} {time_display}")
                        st.caption("도착 예정")
                    
                    with col3:
                        st.write(f"**방향:** {train.get('trainLineNm', 'N/A')}")
                        st.write(f"**현재 위치:** {train.get('arvlMsg2', 'N/A')}")
                    
                    with col4:
                        status = train.get('btrainSttus', '일반')
                        if '급행' in status:
                            st.markdown("🚄 **급행**")
                        else:
                            st.markdown("🚇 **일반**")
                    
                    st.markdown("---")
        else:
            st.warning("⚠️ 현재 도착 예정인 열차가 없습니다.")
    else:
        st.error("⚠️ 실시간 정보를 가져올 수 없습니다. API 키를 확인하세요.")

# ==========================================
# 3. 통합 분석 대시보드
# ==========================================
elif menu == "📈 통합 분석":
    st.header("📈 통합 데이터 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 상권분석 요약")
        df = load_store_data()
        if df is not None:
            # 간단한 통계
            st.metric("총 업종", f"{df['서비스_업종_코드_명'].nunique()}개")
            st.metric("총 매출", f"{df['당월_매출_금액'].sum()/1e12:.2f}조원")
            
            # 미니 차트
            top5 = df.groupby('서비스_업종_코드_명')['당월_매출_금액'].sum().nlargest(5)
            fig = px.pie(values=top5.values, names=top5.index, title='상위 5개 업종')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🚇 지하철 현황")
        st.info("실시간 지하철 정보는 '지하철 실시간' 메뉴에서 확인하세요.")
        
        # 주요 역 리스트
        major_stations = ["강남", "신촌", "홍대입구", "잠실", "신도림"]
        st.write("**주요 역:**")
        for station in major_stations:
            st.write(f"• {station}역")
    
    st.markdown("---")
    st.subheader("📌 대시보드 사용 가이드")
    
    with st.expander("💡 기능 안내"):
        st.markdown("""
        ### 상권분석 메뉴
        - 업종별 매출 상위 10개 시각화
        - 요일별/시간대별 매출 패턴 분석
        - 인터랙티브 차트로 데이터 탐색
        
        ### 지하철 실시간 메뉴
        - 2호선 역별 실시간 도착정보
        - 열차 도착 시간 카운트다운
        - 급행/일반 열차 구분
        
        ### 통합 분석 메뉴
        - 전체 데이터 요약
        - 주요 지표 한눈에 보기
        """)
    
    with st.expander("🔧 기술 스택"):
        st.markdown("""
        - **Frontend**: Streamlit
        - **Data Processing**: Pandas, NumPy
        - **Visualization**: Plotly, Matplotlib, Seaborn
        - **API**: 서울시 공공데이터 API
        """)

# 푸터
st.markdown("---")
st.caption("© 2025 서울시 데이터 분석 대시보드 | Powered by Streamlit & 서울 열린데이터광장")
