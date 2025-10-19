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

# 환경변수 로드
load_dotenv()
SEOUL_API_KEY = os.getenv('SEOUL_LANDMARK_API')
KAKAO_API_KEY = os.getenv('REST_API')

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
async def get_rent_data(gu_code, gu_name, start_idx, end_idx):
    url = f"http://openapi.seoul.go.kr:8088/{SEOUL_API_KEY}/json/tbLnOpendataRentV/{start_idx}/{end_idx}/2025/{gu_code}/{gu_name}"    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:                
                print(f'debuge : {response}')
                if response.status == 200:
                    data = await response.json()
                    return data['tbLnOpendataRentV']['row']
                else:
                    st.error(f"API 오류 발생: {response.status}")
                    return []
    except Exception as e:
        st.error(f"데이터 조회 중 오류 발생: {e}")
        return []

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

# Kakao 지도 생성 함수
def create_kakao_map(data_df, center_lat, center_lng):
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
    <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey={KAKAO_API_KEY}"></script>
    <script>
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
    </script>
    """
    return map_html

def main():
    st.title("서울시 임대차 정보 조회")
    
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

    if st.button("조회"):
        with st.spinner("데이터를 조회중입니다..."):
            # 데이터 조회
            data = asyncio.run(get_rent_data(selected_gu[0], selected_gu[1], 1, 1000))
            if not data:
                st.error("데이터를 조회할 수 없습니다.")
                return

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

            # 위경도 조회
            coordinates = []
            with st.spinner("위치 정보를 조회중입니다..."):
                for address in df['주소']:
                    lng, lat = get_coordinates(address)
                    coordinates.append((lat, lng))
            
            df['위도'] = [coord[0] for coord in coordinates]
            df['경도'] = [coord[1] for coord in coordinates]

            # 필터링 옵션
            st.subheader("필터링 옵션")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                rent_type = st.multiselect("전월세구분", df['전월세구분'].unique())
            with col2:
                min_deposit = st.number_input("최소 보증금(만원)", value=0)
                max_deposit = st.number_input("최대 보증금(만원)", value=int(df['보증금(만원)'].fillna(0).max()))
            with col3:
                min_rent = st.number_input("최소 임대료(만원)", value=0)
                max_rent = st.number_input("최대 임대료(만원)", value=int(df['임대료(만원)'].fillna(0).max()))

            # 필터링 적용
            filtered_df = df.copy()
            if rent_type:
                filtered_df = filtered_df[filtered_df['전월세구분'].isin(rent_type)]
            filtered_df = filtered_df[
                (filtered_df['보증금(만원)'] >= min_deposit) &
                (filtered_df['보증금(만원)'] <= max_deposit) &
                (filtered_df['임대료(만원)'] >= min_rent) &
                (filtered_df['임대료(만원)'] <= max_rent)
            ]

            # 결과 표시
            st.subheader("조회 결과")
            st.write(f"총 {len(filtered_df)}건의 데이터가 조회되었습니다.")

            # 지도 표시
            if not filtered_df.empty:
                center_lat = filtered_df['위도'].mean()
                center_lng = filtered_df['경도'].mean()
                map_html = create_kakao_map(filtered_df, center_lat, center_lng)
                st.components.v1.html(map_html, height=600)

                # 데이터 테이블 표시
                st.subheader("상세 데이터")
                st.dataframe(filtered_df)
            else:
                st.warning("조건에 맞는 데이터가 없습니다.")

if __name__ == "__main__":
    main()