import streamlit as st
import pandas as pd
import requests
import json
from dotenv import load_dotenv
import os
import aiohttp
import asyncio
import time
from datetime import datetime
import folium
from streamlit_folium import folium_static
from folium import plugins
import folium
from streamlit_folium import folium_static

# API 키 로드 함수
def load_api_keys():
    """환경에 따라 적절한 방식으로 API 키 로드"""
    # 로컬 환경 (.env 파일)
    if os.path.exists(".env"):
        load_dotenv()
        return {
            "SEOUL_LANDMARK_API": os.getenv("SEOUL_LANDMARK_API"),
            "REST_API": os.getenv("REST_API"),
            "KAKAO_JAVA_SCRIPT_KEY": os.getenv("KAKAO_JAVA_SCRIPT_KEY")
        }
    # Streamlit Cloud 환경
    else:
        return {
            "SEOUL_LANDMARK_API": st.secrets["SEOUL_LANDMARK_API"],
            "REST_API": st.secrets["REST_API"],
            "KAKAO_JAVA_SCRIPT_KEY": st.secrets["KAKAO_JAVA_SCRIPT_KEY"]
        }

# API 키 로드
API_KEYS = load_api_keys()
SEOUL_API_KEY = API_KEYS["SEOUL_LANDMARK_API"]
KAKAO_API_KEY = API_KEYS["REST_API"]
KAKAO_JAVA_SCRIPT_KEY = API_KEYS["KAKAO_JAVA_SCRIPT_KEY"]

# 페이지 설정
st.set_page_config(
    page_title="서울시 임대차 정보",
    page_icon="🏢",
    layout="wide"
)

# 주소로 위경도 조회 함수
def get_coordinates(address):
    url = 'https://dapi.kakao.com/v2/local/search/address.json'
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {'query': address}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            result = response.json()['documents'][0]
            return float(result['x']), float(result['y'])
    except Exception as e:
        st.error(f"위경도 조회 중 오류 발생: {e}")
        return None, None
    
    return None, None

# 임대차 데이터 조회 함수
async def _get_rent_data_async(gu_code, dong_code=None, page=1):
    """비동기 데이터 조회 함수"""
    page_size = 1000
    start_idx = (page - 1) * page_size + 1
    end_idx = page * page_size
    
    # 기본 URL 구성
    base_url = f"http://openapi.seoul.go.kr:8088/{SEOUL_API_KEY}/json/tbLnOpendataRentV/{start_idx}/{end_idx}"
    
    # 자치구 코드와 법정동 코드 추가
    params = []
    if gu_code:
        params.append(f"CGG_CD={gu_code}")
    if dong_code:
        params.append(f"STDG_CD={dong_code}")
    
    # URL에 파라미터 추가
    url = f"{base_url}{'?' + '&'.join(params) if params else ''}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:                
                if response.status == 200:
                    data = await response.json()
                    if 'tbLnOpendataRentV' in data:
                        result = data['tbLnOpendataRentV']
                        if 'row' in result:
                            return result['row']
                    st.error("데이터 형식이 올바르지 않습니다.")
                    return None
                else:
                    st.error(f"API 오류 발생: {response.status}")
                    return None
    except Exception as e:
        st.error(f"데이터 조회 중 오류 발생: {str(e)}")
        st.error(f"API URL: {url}")
        return None

@st.cache_data(ttl=3600)  # 1시간 동안 캐시 유지
def get_rent_data(gu_code, dong_code=None, page=1):
    """캐시 가능한 동기 래퍼 함수"""
    return asyncio.run(_get_rent_data_async(
        gu_code=gu_code,
        dong_code=dong_code,
        page=page
    ))

@st.cache_data(ttl=3600)
def get_cached_data(gu_code, dong_code=None):
    """데이터 캐시 최적화 함수"""
    try:
        # 첫 페이지 데이터 조회
        data = get_rent_data(
            gu_code=gu_code,
            dong_code=dong_code,
            page=1
        )
        
        if not data:
            return None, "데이터가 없습니다."
        
        # 데이터 수집
        all_data = data.copy()
        current_page = 2
        
        # 데이터가 1000건인 경우 다음 페이지 확인
        while len(data) == 1000:
            data = get_rent_data(
                gu_code=gu_code,
                dong_code=dong_code,
                page=current_page
            )
            if data:
                all_data.extend(data)
            current_page += 1
            time.sleep(0.5)  # API 요청 간격 조절
        
        # 모든 데이터를 데이터프레임으로 변환
        if all_data:
            return pd.DataFrame(all_data), None
        return None, "데이터를 찾을 수 없습니다."
        
        # 데이터가 있으면 모든 페이지 조회
        all_data = initial_data
        page = 2
        
        # 데이터가 더 있는 동안 계속 조회
        while len(initial_data) == 1000:  # 페이지 크기가 1000이면 다음 페이지 존재
            initial_data = get_rent_data(
                gu_code=gu_code,
                dong_code=dong_code,
                page=page
            )
            if initial_data:
                all_data.extend(initial_data)
            page += 1
            time.sleep(0.5)  # API 요청 간격 조절
        
        return pd.DataFrame(all_data), None
        
    except Exception as e:
        return None, f"데이터 수집 중 오류 발생: {str(e)}"

def preprocess_data(df):
    """데이터 전처리 함수"""
    if df is None or df.empty:
        return None
    
    try:
        # 숫자형 컬럼 변환
        numeric_columns = ['GRFE', 'RTFE', 'MNO', 'SNO', 'FLR', 'RENT_AREA']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 컬럼명 한글 변환
        column_mapping = {
            'STDG_NM': '법정동명',
            'LOTNO_SE_NM': '지번구분명',
            'MNO': '본번',
            'SNO': '부번',
            'FLR': '층',
            'CTRT_DAY': '계약일',
            'RENT_SE': '전월세구분',
            'RENT_AREA': '임대면적(㎡)',
            'GRFE': '보증금(만원)',
            'RTFE': '임대료(만원)',
            'BLDG_NM': '건물명',
            'ARCH_YR': '건축년도',
            'BLDG_USG': '건물용도',
            'CTRT_PRD': '계약기간',
            'NEW_UPDT_YN': '신규갱신여부',
            'CTRT_UPDT_USE_YN': '계약갱신권사용여부',
            'BFR_GRFE': '종전보증금',
            'BFR_RTFE': '종전임대료'
        }
        df = df.rename(columns=column_mapping)
        
        return df
    except Exception as e:
        st.error(f"데이터 전처리 중 오류 발생: {str(e)}")
        return None

# 주소 생성 함수
def create_address(row, gu_name):
    address = f"서울특별시 {gu_name} {row['법정동명']}"
    if row['지번구분명'] == '산':
        address += f" {row['지번구분명']}"
    try:
        address += f" {int(row['본번'])}"
    except:
        pass
    try:
        if row['부번'] != 0:
            address += f"-{int(row['부번'])}"
    except:
        pass
    return address

# Folium 지도 생성 함수
def create_folium_map(data_df, center_lat, center_lng):
    # 기본 지도 생성
    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=14,
        tiles='OpenStreetMap'
    )
    
    # 마커 클러스터 생성
    marker_cluster = plugins.MarkerCluster().add_to(m)
    
    # 데이터포인트 추가
    for _, row in data_df.iterrows():
        if pd.notna(row['위도']) and pd.notna(row['경도']):
            # 팝업 내용 생성
            popup_content = f"""
                <div style='width:200px'>
                <b>{row['건물명'] if pd.notna(row['건물명']) else row['주소']}</b><br>
                전월세구분: {row['전월세구분']}<br>
                보증금: {int(row['보증금(만원)']):,}만원<br>
                임대료: {int(row['임대료(만원)']):,}만원<br>
                면적: {row['임대면적(㎡)']}㎡<br>
                계약일: {row['계약일']}
                </div>
            """
            
            # 마커 색상 설정 (전세/월세 구분)
            color = 'red' if row['전월세구분'] == '전세' else 'blue'
            
            # 마커 추가
            folium.Marker(
                location=[row['위도'], row['경도']],
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color=color, icon='info-sign'),
                tooltip=f"{row['건물명'] if pd.notna(row['건물명']) else row['주소']}"
            ).add_to(marker_cluster)
    
    return m
    # HTML 템플릿에 데이터 삽입
    markers = []
    for _, row in data_df.iterrows():
        if pd.notna(row['위도']) and pd.notna(row['경도']):
            marker = {
                'position': {'lat': row['위도'], 'lng': row['경도']},
                'content': f"{row['건물명'] if row['건물명'] else row['주소']}<br>전월세구분: {row['전월세구분']}<br>보증금: {row['보증금(만원)']}만원<br>임대료: {row['임대료(만원)']}만원"
            }
            markers.append(marker)
    
    map_html = f"""
    <div id="map" style="width:100%;height:600px;"></div>
    <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey={KAKAO_JAVA_SCRIPT_KEY}&autoload=false"></script>
    <script>
        kakao.maps.load(function() {{
            var container = document.getElementById('map');
            var options = {{
                center: new kakao.maps.LatLng({center_lat}, {center_lng}),
                level: 5
            }};
            var map = new kakao.maps.Map(container, options);
        
        var markers = {json.dumps(markers)};
        markers.forEach(function(markerInfo) {{
            var marker = new kakao.maps.Marker({{
                position: new kakao.maps.LatLng(markerInfo.position.lat, markerInfo.position.lng),
                map: map
            }});
            
            var infowindow = new kakao.maps.InfoWindow({{
                content: markerInfo.content
            }});
            
            kakao.maps.event.addListener(marker, 'click', function() {{
                infowindow.open(map, marker);
            }});
        }});
        }});
    </script>
    """
    return map_html

def filter_and_display_data(df, status_container=None, progress_bar=None):
    """필터링 및 데이터 표시 함수"""
    if df is None or df.empty:
        st.warning("표시할 데이터가 없습니다.")
        return

    # 필터링 옵션
    st.subheader("필터링 옵션")
    
    # 보증금 범위 슬라이더
    min_deposit_value = int(df['보증금(만원)'].fillna(0).min())
    max_deposit_value = int(df['보증금(만원)'].fillna(0).max())
    deposit_range = st.slider(
        "보증금 범위 (만원)",
        min_value=min_deposit_value,
        max_value=max_deposit_value,
        value=(min_deposit_value, max_deposit_value),
        format="%d"
    )
    min_deposit, max_deposit = deposit_range
    
    # 임대료 범위 슬라이더
    min_rent_value = int(df['임대료(만원)'].fillna(0).min())
    max_rent_value = int(df['임대료(만원)'].fillna(0).max())
    rent_range = st.slider(
        "임대료 범위 (만원)",
        min_value=min_rent_value,
        max_value=max_rent_value,
        value=(min_rent_value, max_rent_value),
        format="%d"
    )
    min_rent, max_rent = rent_range
    
    # 계약기간 범위 슬라이더 (있는 경우)
    period_range = None
    if '계약기간' in df.columns:
        period_values = pd.to_numeric(df['계약기간'], errors='coerce').dropna()
        if not period_values.empty:
            min_period_value = int(period_values.min())
            max_period_value = int(period_values.max())
            period_range = st.slider(
                "계약기간 (개월)",
                min_value=min_period_value,
                max_value=max_period_value,
                value=(min_period_value, max_period_value),
                format="%d"
            )

    # 필터링 적용
    filtered_df = df[
        (df['보증금(만원)'] >= min_deposit) &
        (df['보증금(만원)'] <= max_deposit) &
        (df['임대료(만원)'] >= min_rent) &
        (df['임대료(만원)'] <= max_rent)
    ]

    if period_range is not None:
        min_period, max_period = period_range
        filtered_df = filtered_df[
            pd.to_numeric(filtered_df['계약기간'], errors='coerce').between(min_period, max_period)
        ]

    # 결과 표시
    st.subheader("조회 결과")
    st.write(f"총 {len(filtered_df):,}건의 데이터가 조회되었습니다.")

    # 지도 표시
    if not filtered_df.empty:
        center_lat = filtered_df['위도'].mean()
        center_lng = filtered_df['경도'].mean()
        
        if status_container:
            status_container.text("🗺️ 지도를 생성중입니다...")
        if progress_bar:
            progress_bar.progress(0.5)
            
        # Folium 지도 생성 및 표시
        map_obj = create_folium_map(filtered_df, center_lat, center_lng)
        folium_static(map_obj)
        
        if progress_bar:
            progress_bar.progress(1.0)
        if status_container:
            status_container.text("✨ 모든 처리가 완료되었습니다!")

        # 데이터 테이블 표시
        st.subheader("상세 데이터")
        st.dataframe(filtered_df)
        
        # CSV 다운로드 버튼
        csv_data = filtered_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="CSV 파일 다운로드",
            data=csv_data,
            file_name=f"서울시_임대_정보_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("조건에 맞는 데이터가 없습니다.")

def initialize_session_state():
    """세션 상태 초기화 함수"""
    if 'full_data_df' not in st.session_state:
        st.session_state.full_data_df = None
    if 'selected_gu_info' not in st.session_state:
        st.session_state.selected_gu_info = None
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    if 'last_update' not in st.session_state:
        st.session_state.last_update = None

def load_location_codes():
    """법정동 코드 데이터 로드"""
    try:
        codes_df = pd.read_csv('code.csv')
        return codes_df
    except Exception as e:
        st.error(f"법정동 코드 파일 로드 중 오류 발생: {e}")
        return None

def main():
    st.title("서울시 임대차 정보 조회")
    
    # 세션 상태 초기화
    initialize_session_state()
    
    # 사이드바 설정
    with st.sidebar:
        st.header("데이터 조회 설정")
        
        # 법정동 코드 데이터 로드
        codes_df = load_location_codes()
        if codes_df is None:
            return
            
        # 자치구 선택
        gu_options = codes_df[['자치구코드', '자치구명']].drop_duplicates()
        selected_gu = st.selectbox(
            "자치구 선택",
            options=gu_options.values.tolist(),
            format_func=lambda x: x[1],
            key='selected_gu'
        )
        
        # 선택된 자치구의 법정동 목록 필터링
        dong_options = codes_df[
            codes_df['자치구코드'] == selected_gu[0]
        ][['법정동코드', '법정동명']].drop_duplicates()
        
        # 법정동 선택 (전체 선택 옵션 포함)
        dong_options = pd.concat([
            pd.DataFrame([['', '전체']], columns=['법정동코드', '법정동명']),
            dong_options
        ])
        
        selected_dong = st.selectbox(
            "법정동 선택",
            options=dong_options.values.tolist(),
            format_func=lambda x: x[1],
            key='selected_dong'
        )
        
        chunk_size = st.number_input(
            "데이터 로드 단위",
            min_value=100,
            max_value=1000,
            value=1000,
            step=100,
            help="한 번에 가져올 데이터의 개수입니다."
        )

    col1, col2 = st.columns([4, 1])
    with col2:
        load_data = st.button("데이터 조회", type="primary", use_container_width=True)
    
    # 새로운 데이터 조회가 필요한 경우에만 API 호출
    if load_data:
        # 상태 표시 컨테이너 초기화
        status_container = st.empty()
        progress_container = st.empty()
        
        with st.spinner("🔍 데이터를 조회중입니다..."):
            # 진행 상태 표시
            status_container.info("데이터를 수집하고 있습니다...")
            progress_container.progress(0.2)
            
            # 자치구/법정동 코드로 데이터 조회
            df, error_msg = get_cached_data(
                gu_code=selected_gu[0], 
                dong_code=selected_dong[0] if selected_dong[0] else None
            )
            progress_container.progress(0.4)
            
            if error_msg:
                status_container.error(error_msg)
                return
                
            if df is None or df.empty:
                status_container.error("데이터를 가져오는데 실패했습니다.")
                return
                
            status_container.info(f"총 {len(df):,}건의 데이터를 수집했습니다.")
            progress_container.progress(0.6)
            
            # 데이터 전처리
            status_container.info("데이터를 전처리하고 있습니다...")
            df = preprocess_data(df)
            if df is None:
                status_container.error("데이터 전처리 중 오류가 발생했습니다.")
                return
            
            progress_container.progress(0.8)
            
            # 주소 생성 및 위치 정보 조회
            status_container.info("🌍 위치 정보를 조회중입니다...")
            progress_bar = progress_container.progress(0)
            
            coordinates = []
            total_addresses = len(df['주소'])
            
            for idx, address in enumerate(df['주소']):
                lng, lat = get_coordinates(address)
                coordinates.append((lat, lng))
                progress = (idx + 1) / total_addresses
                progress_bar.progress(progress)
                status_container.text(f"🌍 위치 정보를 조회중입니다... ({idx + 1}/{total_addresses})")
            
            df['위도'] = [coord[0] for coord in coordinates]
            df['경도'] = [coord[1] for coord in coordinates]
            
            # 데이터를 세션 상태에 저장
            st.session_state.full_data_df = df
            st.session_state.selected_gu_info = selected_gu
            st.session_state.data_loaded = True
            
            # 완료 메시지 표시
            status_container.text("✅ 데이터 수집이 완료되었습니다!")
            progress_bar.progress(1.0)
            
            # 기본 통계 정보 표시
            with st.expander("📊 기본 통계 정보", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("총 데이터 수", f"{len(df):,}건")
                with col2:
                    st.metric("평균 보증금", f"{df['보증금(만원)'].mean():,.0f}만원")
                with col3:
                    st.metric("평균 임대료", f"{df['임대료(만원)'].mean():,.0f}만원")
    
    # 로딩 상태 표시
    if 'data_loaded' not in st.session_state:
        st.info("👆 위에서 자치구를 선택하고 데이터 조회 버튼을 클릭하세요.")
    
    # 저장된 데이터가 있으면 필터링 및 표시
    if st.session_state.data_loaded and st.session_state.full_data_df is not None:
        # 마지막 업데이트 시간 표시
        st.success(f"✅ {st.session_state.selected_gu_info[1]} 데이터 로드 완료 (마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        
        # 데이터 분석 탭 생성
        tab1, tab2, tab3 = st.tabs(["📊 데이터 분석", "🗺️ 지도 보기", "📋 상세 데이터"])
        
        with tab1:
            df = st.session_state.full_data_df
            
            # 기간별 분석
            st.subheader("기간별 분석")
            if '계약일' in df.columns:
                df['계약월'] = pd.to_datetime(df['계약일']).dt.strftime('%Y-%m')
                monthly_stats = df.groupby('계약월').agg({
                    '보증금(만원)': 'mean',
                    '임대료(만원)': 'mean',
                    '임대면적(㎡)': 'mean'
                }).round(2)
                st.line_chart(monthly_stats)
            
            # 지역별 분석
            st.subheader("지역별 분석")
            if '법정동명' in df.columns:
                dong_stats = df.groupby('법정동명').agg({
                    '보증금(만원)': 'mean',
                    '임대료(만원)': 'mean'
                }).round(2)
                st.bar_chart(dong_stats)
        
        with tab2:
            filter_and_display_data(
                st.session_state.full_data_df,
                status_container if 'status_container' in locals() else None,
                progress_bar if 'progress_bar' in locals() else None
            )
            
        with tab3:
            st.dataframe(
                st.session_state.full_data_df,
                use_container_width=True,
                height=400
            )
            
        # 데이터 조회 시작
        with st.spinner("데이터를 가져오는 중..."):
            # 자치구/법정동 코드로 데이터 조회
            df, error_msg = get_cached_data(
                gu_code=selected_gu[0], 
                dong_code=selected_dong[0] if selected_dong[0] else None
            )
            
            if error_msg:
                st.error(error_msg)
                return
                
            # 데이터 전처리
            df = preprocess_data(df)
            if df is None:
                st.error("데이터 전처리 중 오류가 발생했습니다.")
                return
            
            # 주소 생성
            df['주소'] = df.apply(lambda x: create_address(x, selected_gu[1]), axis=1)
        
        # 숫자형 컬럼 변환
        numeric_columns = ['GRFE', 'RTFE', 'MNO', 'SNO', 'FLR', 'RENT_AREA']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 컬럼명 한글 변환
        column_mapping = {
            'STDG_NM': '법정동명',
            'LOTNO_SE_NM': '지번구분명',
            'MNO': '본번',
            'SNO': '부번',
            'FLR': '층',
            'CTRT_DAY': '계약일',
            'RENT_SE': '전월세구분',
            'RENT_AREA': '임대면적(㎡)',
            'GRFE': '보증금(만원)',
            'RTFE': '임대료(만원)',
            'BLDG_NM': '건물명',
            'ARCH_YR': '건축년도',
            'BLDG_USG': '건물용도',
            'CTRT_PRD': '계약기간',
            'NEW_UPDT_YN': '신규갱신여부',
            'CTRT_UPDT_USE_YN': '계약갱신권사용여부',
            'BFR_GRFE': '종전보증금',
            'BFR_RTFE': '종전임대료'
        }
        df = df.rename(columns=column_mapping)

        # 주소 생성
        df['주소'] = df.apply(lambda x: create_address(x, selected_gu[1]), axis=1)

        # 위경도 조회 시작
        status_container.text("🌍 위치 정보를 조회중입니다...")
        total_addresses = len(df['주소'])
        
        coordinates = []
        for idx, address in enumerate(df['주소']):
            lng, lat = get_coordinates(address)
            coordinates.append((lat, lng))
            # 진행률 업데이트
            progress = (idx + 1) / total_addresses
            progress_bar.progress(progress)
            status_container.text(f"🌍 위치 정보를 조회중입니다... ({idx + 1}/{total_addresses})")
        
        # 진행바 완료 표시
        progress_bar.progress(1.0)
        status_container.text("✅ 위치 정보 조회가 완료되었습니다!")
        
        df['위도'] = [coord[0] for coord in coordinates]
        df['경도'] = [coord[1] for coord in coordinates]

        # 필터링 옵션
        st.subheader("필터링 옵션")
        
        # 보증금 범위 슬라이더
        min_deposit_value = int(df['보증금(만원)'].fillna(0).min())
        max_deposit_value = int(df['보증금(만원)'].fillna(0).max())
        deposit_range = st.slider(
            "보증금 범위 (만원)",
            min_value=min_deposit_value,
            max_value=max_deposit_value,
            value=(min_deposit_value, max_deposit_value),
            format="%d"
        )
        min_deposit, max_deposit = deposit_range
        
        # 임대료 범위 슬라이더
        min_rent_value = int(df['임대료(만원)'].fillna(0).min())
        max_rent_value = int(df['임대료(만원)'].fillna(0).max())
        rent_range = st.slider(
            "임대료 범위 (만원)",
            min_value=min_rent_value,
            max_value=max_rent_value,
            value=(min_rent_value, max_rent_value),
            format="%d"
        )
        min_rent, max_rent = rent_range
        
        # 계약기간 범위 슬라이더 (있는 경우)
        if '계약기간' in df.columns:
            period_values = df['계약기간'].dropna().unique()
            if len(period_values) > 0:
                period_values = sorted([int(x) for x in period_values if str(x).isdigit()])
                if period_values:
                    period_range = st.slider(
                        "계약기간 (개월)",
                        min_value=min(period_values),
                        max_value=max(period_values),
                        value=(min(period_values), max(period_values)),
                        format="%d"
                    )
                    min_period, max_period = period_range        # 필터링 적용
        filtered_df = df.copy()
        
        # 보증금과 임대료 필터 적용
        filtered_df = filtered_df[
            (filtered_df['보증금(만원)'] >= min_deposit) &
            (filtered_df['보증금(만원)'] <= max_deposit) &
            (filtered_df['임대료(만원)'] >= min_rent) &
            (filtered_df['임대료(만원)'] <= max_rent)
        ]
        
        # 계약기간 필터 적용 (있는 경우)
        if '계약기간' in filtered_df.columns and 'min_period' in locals():
            filtered_df = filtered_df[
                filtered_df['계약기간'].apply(lambda x: 
                    float(x) >= min_period and float(x) <= max_period 
                    if str(x).isdigit() else False
                )
            ]

        # 결과 표시
        st.subheader("조회 결과")
        st.write(f"총 {len(filtered_df)}건의 데이터가 조회되었습니다.")

        # 지도 표시
        if not filtered_df.empty:
            center_lat = filtered_df['위도'].mean()
            center_lng = filtered_df['경도'].mean()
            
            # Folium 지도 생성 시작
            status_container.text("🗺️ 지도를 생성중입니다...")
            progress_bar.progress(0)
            
            # Folium 지도 생성 및 표시
            map_obj = create_folium_map(filtered_df, center_lat, center_lng)
            folium_static(map_obj)
            
            # 진행 완료
            progress_bar.progress(1.0)
            status_container.text("✨ 모든 처리가 완료되었습니다!")

            # 데이터 테이블 표시
            st.subheader("상세 데이터")
            st.dataframe(filtered_df)
            
            # CSV 다운로드 버튼
            csv_data = filtered_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="CSV 파일 다운로드",
                data=csv_data,
                file_name=f"서울시_임대_정보_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("조건에 맞는 데이터가 없습니다.")

if __name__ == "__main__":
    main()