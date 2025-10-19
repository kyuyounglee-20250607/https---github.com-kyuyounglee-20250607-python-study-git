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

# 환경변수 로드
load_dotenv()
SEOUL_API_KEY = os.getenv('SEOUL_LANDMARK_API')
KAKAO_API_KEY = os.getenv('REST_API')
KAKAO_JAVA_SCRIPT_KEY = os.getenv('KAKAO_JAVA_SCRIPT_KEY')

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
async def _get_rent_data_async(gu_code, gu_name, start_idx, end_idx):
    """비동기 데이터 조회 함수"""
    url = f"http://openapi.seoul.go.kr:8088/{SEOUL_API_KEY}/json/tbLnOpendataRentV/{start_idx}/{end_idx}/2025/{gu_code}/{gu_name}"    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:                
                if response.status == 200:
                    data = await response.json()
                    return data['tbLnOpendataRentV']['row']
                else:
                    st.error(f"API 오류 발생: {response.status}")
                    return []
    except Exception as e:
        st.error(f"데이터 조회 중 오류 발생: {e}")
        return []

@st.cache_data(ttl=3600)  # 1시간 동안 캐시 유지
def get_rent_data(gu_code, gu_name, start_idx, end_idx):
    """캐시 가능한 동기 래퍼 함수"""
    return asyncio.run(_get_rent_data_async(gu_code, gu_name, start_idx, end_idx))

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

def main():
    st.title("서울시 임대차 정보 조회")
    
    # 세션 상태 초기화
    if 'full_data_df' not in st.session_state:
        st.session_state.full_data_df = None
    if 'selected_gu_info' not in st.session_state:
        st.session_state.selected_gu_info = None
    
    # 법정동 코드 데이터 로드
    try:
        codes_df = pd.read_csv('code.csv')
        gu_options = codes_df[['code', 'name']].values.tolist()
    except Exception as e:
        st.error(f"법정동 코드 파일 로드 중 오류 발생: {e}")
        return

    # 자치구 선택
    selected_gu = st.selectbox(
        "자치구 선택",
        options=gu_options,
        format_func=lambda x: x[1]
    )

    # 새로운 데이터 조회가 필요한 경우에만 API 호출
    if st.button("조회") or (st.session_state.selected_gu_info != selected_gu):
        # 상태 표시 컨테이너 초기화
        status_container = st.empty()
        progress_container = st.empty()
        result_container = st.empty()
        
        # 데이터 조회 시작
        status_container.text("🔍 데이터를 조회중입니다...")
        progress_bar = progress_container.progress(0)
        
        try:
            # 초기 데이터 조회로 전체 개수 확인
            initial_data = get_rent_data(selected_gu[0], selected_gu[1], 1, 1)
            if not initial_data:
                st.error("데이터를 조회할 수 없습니다.")
                return
                
            # 전체 데이터 수집
            total_count = initial_data[0].get('총건수', 1000)
            page_size = 1000
            total_pages = (total_count + page_size - 1) // page_size
            
            all_data = []
            for page in range(total_pages):
                start_idx = page * page_size + 1
                end_idx = min((page + 1) * page_size, total_count)
                
                # 진행률 업데이트
                progress = (page + 1) / total_pages
                status_container.text(f"🔍 데이터를 조회중입니다... ({start_idx:,}~{end_idx:,}/{total_count:,})")
                progress_bar.progress(progress)
                
                # 데이터 조회
                page_data = get_rent_data(selected_gu[0], selected_gu[1], start_idx, end_idx)
                if page_data:
                    all_data.extend(page_data)
                time.sleep(0.5)
            
            if not all_data:
                st.error("데이터를 조회할 수 없습니다.")
                return
            
            # 데이터프레임 생성 및 전처리
            df = pd.DataFrame(all_data)
            
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
            
            # 주소 생성 및 위경도 조회
            df['주소'] = df.apply(lambda x: create_address(x, selected_gu[1]), axis=1)
            
            status_container.text("🌍 위치 정보를 조회중입니다...")
            coordinates = []
            for idx, address in enumerate(df['주소']):
                lng, lat = get_coordinates(address)
                coordinates.append((lat, lng))
                progress = (idx + 1) / len(df['주소'])
                progress_bar.progress(progress)
                status_container.text(f"🌍 위치 정보를 조회중입니다... ({idx + 1}/{len(df['주소'])})")
            
            df['위도'] = [coord[0] for coord in coordinates]
            df['경도'] = [coord[1] for coord in coordinates]
            
            # 데이터를 세션 상태에 저장
            st.session_state.full_data_df = df
            st.session_state.selected_gu_info = selected_gu
            
            # 완료 메시지 표시
            status_container.text("✅ 데이터 수집이 완료되었습니다!")
            progress_bar.progress(1.0)
            
        except Exception as e:
            st.error(f"데이터 처리 중 오류가 발생했습니다: {str(e)}")
            return
    
    # 저장된 데이터가 있으면 필터링 및 표시
    if st.session_state.full_data_df is not None:
        filter_and_display_data(
            st.session_state.full_data_df,
            status_container if 'status_container' in locals() else None,
            progress_bar if 'progress_bar' in locals() else None
        )
            
        total_count = initial_data[0].get('총건수', 1000)  # 기본값 1000
        page_size = 1000
        total_pages = (total_count + page_size - 1) // page_size
        
        # 진행 상태 업데이트
        result_container.info(f"총 {total_count:,}건의 데이터를 조회합니다.")
        
        # 전체 데이터 수집
        all_data = []
        for page in range(total_pages):
            start_idx = page * page_size + 1
            end_idx = min((page + 1) * page_size, total_count)
            
            # 진행률 업데이트
            progress = (page + 1) / total_pages
            status_container.text(f"🔍 데이터를 조회중입니다... ({start_idx:,}~{end_idx:,}/{total_count:,})")
            progress_bar.progress(progress)
            
            # 데이터 조회
            page_data = get_rent_data(selected_gu[0], selected_gu[1], start_idx, end_idx)
            if page_data:
                all_data.extend(page_data)
            time.sleep(0.5)  # API 요청 간격 조절
        
        # 진행 완료
        progress_bar.progress(1.0)
        status_container.text("✅ 데이터 조회가 완료되었습니다!")
        
        if not all_data:
            st.error("데이터를 조회할 수 없습니다.")
            return
            
        data = all_data



        # 데이터프레임 생성 및 전처리
        df = pd.DataFrame(data)
        
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