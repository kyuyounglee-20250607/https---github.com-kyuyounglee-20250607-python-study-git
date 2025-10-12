
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

DB_NAME = "seoul_data.db"
TABLE_NAME = "job_counseling"

# Streamlit의 캐시 기능을 사용하여 데이터 로딩 속도 향상
@st.cache_data
def load_data():
    """SQLite DB에서 데이터를 불러와 Pandas DataFrame으로 변환합니다."""
    try:
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        query = f"SELECT * FROM {TABLE_NAME}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        # YYYYMM을 문자열로 변환하여 시각화 시 범주형으로 처리되도록 함
        df['YYYYMM'] = df['YYYYMM'].astype(str)
        return df
    except Exception as e:
        st.error(f"데이터베이스를 불러오는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()


def show_data_viewer(df):
    """데이터 조회 및 검색, 페이징 기능을 구현한 탭"""
    st.subheader("데이터 조회 및 검색")

    # 검색 기능
    search_term = st.text_input("기관명(CATEGORY_NM)으로 검색", "")
    if search_term:
        df_filtered = df[df['CATEGORY_NM'].str.contains(search_term, case=False, na=False)]
    else:
        df_filtered = df

    total_rows = len(df_filtered)
    st.write(f"총 {total_rows}개의 결과")

    # 페이징 기능
    rows_per_page = 10
    total_pages = (total_rows // rows_per_page) + (1 if total_rows % rows_per_page > 0 else 0)
    
    if total_pages > 0:
        page_num = st.number_input('페이지 번호', min_value=1, max_value=total_pages, value=1, step=1)
        start_idx = (page_num - 1) * rows_per_page
        end_idx = page_num * rows_per_page
        st.dataframe(df_filtered.iloc[start_idx:end_idx])
    else:
        st.warning("표시할 데이터가 없습니다.")


def show_analyzer(df):
    """다양한 시각화와 통계를 보여주는 탭"""
    st.subheader("시각화 및 분석")

    # 언어 컬럼과 이름 매핑
    lang_map = {
        'TYPE0': '한국어', 'TYPE1': '영어', 'TYPE2': '일본어', 'TYPE3': '중국어',
        'TYPE4': '베트남어', 'TYPE5': '타갈로그어', 'TYPE6': '몽골어', 'TYPE7': '프랑스어',
        'TYPE8': '러시아어', 'TYPE9': '우즈벡어', 'TYPE10': '태국어', 'TYPE11': '네팔어',
        'TYPE12': '인도네시아어', 'TYPE13': '파키스탄어', 'TYPE14': '아랍어',
        'TYPE15': '스페인어', 'TYPE99': '기타언어'
    }
    lang_cols = list(lang_map.keys())

    # 1. 월별 전체 상담 건수 추이 (라인 차트)
    st.markdown("#### 월별 전체 상담 건수 추이")
    monthly_sum = df.groupby('YYYYMM')['TYPE_SUM'].sum().reset_index().sort_values('YYYYMM')
    fig1 = px.line(monthly_sum, x='YYYYMM', y='TYPE_SUM', title='월별 전체 상담 건수', markers=True)
    fig1.update_layout(xaxis_title="년월", yaxis_title="총 상담 건수")
    st.plotly_chart(fig1, use_container_width=True)

    # 2. 상담 유형별 비율 (파이 차트)
    st.markdown("#### 상담 유형별 비율")
    category_sum = df.groupby('CATEGORY_NM')['TYPE_SUM'].sum().reset_index()
    fig2 = px.pie(category_sum, names='CATEGORY_NM', values='TYPE_SUM', title='상담 유형별 상담 건수 비율',
                  hole=0.3, labels={'CATEGORY_NM':'상담 유형', 'TYPE_SUM':'총 상담 건수'})
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

    # 3. 언어별 상담 건수 (바 차트)
    st.markdown("#### 언어별 상담 건수")
    lang_sum = df[lang_cols].sum().sort_values(ascending=False)
    lang_sum.index = lang_sum.index.map(lang_map)
    fig3 = px.bar(lang_sum, x=lang_sum.index, y=lang_sum.values, title='언어별 총 상담 건수')
    fig3.update_layout(xaxis_title="언어", yaxis_title="총 상담 건수", xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig3, use_container_width=True)
    
    # 4. 연도별/기관별 상담 건수 (그룹 바 차트)
    st.markdown("#### 연도별/기관별 상담 건수")
    df['YEAR'] = df['YYYYMM'].str[:4]
    yearly_category_sum = df.groupby(['YEAR', 'CATEGORY_NM'])['TYPE_SUM'].sum().reset_index()
    fig4 = px.bar(yearly_category_sum, x='YEAR', y='TYPE_SUM', color='CATEGORY_NM', 
                  barmode='group', title='연도별/기관별 상담 건수')
    fig4.update_layout(xaxis_title="연도", yaxis_title="총 상담 건수")
    st.plotly_chart(fig4, use_container_width=True)


def main():
    """메인 앱 실행 함수"""
    st.set_page_config(page_title="서울시 외국인 취업 상담 분석", layout="wide")
    st.title("서울시 외국인 취업 상담 데이터 대시보드")

    df = load_data()

    if not df.empty:
        tab1, tab2 = st.tabs(["데이터 조회", "시각화 분석"])

        with tab1:
            show_data_viewer(df)
        
        with tab2:
            show_analyzer(df)
    else:
        st.warning("데이터를 불러올 수 없습니다. `collect_seoul_data.py`를 먼저 실행했는지, `seoul_data.db` 파일이 올바른지 확인하세요.")

if __name__ == "__main__":
    main()
