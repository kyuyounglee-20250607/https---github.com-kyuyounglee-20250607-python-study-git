
# 서울 열린데이터 광장 - 이용안내 - OPEN API 소개 - api 발급( * 사용URL :  http://localhost )
# .env 파일에 SEOUL_API=''등록

# 호출주소
# 호출주소와 같이 사용되는 입력 파라메터 정보
# 제공하는 api키

# 응답결과의 형태 - api제공하는곳에서 정보를 취득
# 응답결과는 대부분 json  / xml형태  (json추천)
	# 서울시 상권분석서비스(추정매출-서울시)
# http://openapi.seoul.go.kr:8088/(인증키)/xml/VwsmMegaSelngW/1/5/

# 공공데이터
# https://data.seoul.go.kr/dataList/OA-22177/S/1/datasetView.do
# 서울시 상권분석서비스(추정매출-서울시)

import requests
import dotenv
import os
dotenv.load_dotenv()  # .env 환경변수 파일을 로드함

key = os.getenv("SEOUL_API")

url = 'http://openapi.seoul.go.kr:8088/'+key+'/json/VwsmMegaSelngW/1/1000/'
response = requests.get(url)
print(f'접속주소 : {response.url}')
print(f'응답코드 : {response.status_code}')
result = response.json()
# 보기쉽게 들여쓰기로 출력
import json
result = result['VwsmMegaSelngW']['row']
print(len(result))
print(json.dumps(result[0],indent=4,ensure_ascii=False)) 

import pandas as pd
df = pd.DataFrame(result)

column_mapping = {
    "STDR_YYQU_CD": "기준_년분기_코드",
    "MEGA_CD": "서울시_코드",
    "MEGA_CD_NM": "서울시_코드_명",
    "SVC_INDUTY_CD": "서비스_업종_코드",
    "SVC_INDUTY_CD_NM": "서비스_업종_코드_명",
    "THSMON_SELNG_AMT": "당월_매출_금액",
    "THSMON_SELNG_CO": "당월_매출_건수",
    "MDWK_SELNG_AMT": "주중_매출_금액",
    "WKEND_SELNG_AMT": "주말_매출_금액",
    "MON_SELNG_AMT": "월요일_매출_금액",
    "TUES_SELNG_AMT": "화요일_매출_금액",
    "WED_SELNG_AMT": "수요일_매출_금액",
    "THUR_SELNG_AMT": "목요일_매출_금액",
    "FRI_SELNG_AMT": "금요일_매출_금액",
    "SAT_SELNG_AMT": "토요일_매출_금액",
    "SUN_SELNG_AMT": "일요일_매출_금액",
    "TMZON_00_06_SELNG_AMT": "시간대_00~06_매출_금액",
    "TMZON_06_11_SELNG_AMT": "시간대_06~11_매출_금액",
    "TMZON_11_14_SELNG_AMT": "시간대_11~14_매출_금액",
    "TMZON_14_17_SELNG_AMT": "시간대_14~17_매출_금액",
    "TMZON_17_21_SELNG_AMT": "시간대_17~21_매출_금액",
    "TMZON_21_24_SELNG_AMT": "시간대_21~24_매출_금액",
    "ML_SELNG_AMT": "남성_매출_금액",
    "FML_SELNG_AMT": "여성_매출_금액",
    "AGRDE_10_SELNG_AMT": "연령대_10_매출_금액",
    "AGRDE_20_SELNG_AMT": "연령대_20_매출_금액",
    "AGRDE_30_SELNG_AMT": "연령대_30_매출_금액",
    "AGRDE_40_SELNG_AMT": "연령대_40_매출_금액",
    "AGRDE_50_SELNG_AMT": "연령대_50_매출_금액",
    "AGRDE_60_ABOVE_SELNG_AMT": "연령대_60_이상_매출_금액",
    "MDWK_SELNG_CO": "주중_매출_건수",
    "WKEND_SELNG_CO": "주말_매출_건수",
    "MON_SELNG_CO": "월요일_매출_건수",
    "TUES_SELNG_CO": "화요일_매출_건수",
    "WED_SELNG_CO": "수요일_매출_건수",
    "THUR_SELNG_CO": "목요일_매출_건수",
    "FRI_SELNG_CO": "금요일_매출_건수",
    "SAT_SELNG_CO": "토요일_매출_건수",
    "SUN_SELNG_CO": "일요일_매출_건수",
    "TMZON_00_06_SELNG_CO": "시간대_00~06_매출_건수",
    "TMZON_06_11_SELNG_CO": "시간대_06~11_매출_건수",
    "TMZON_11_14_SELNG_CO": "시간대_11~14_매출_건수",
    "TMZON_14_17_SELNG_CO": "시간대_14~17_매출_건수",
    "TMZON_17_21_SELNG_CO": "시간대_17~21_매출_건수",
    "TMZON_21_24_SELNG_CO": "시간대_21~24_매출_건수",
    "ML_SELNG_CO": "남성_매출_건수",
    "FML_SELNG_CO": "여성_매출_건수",
    "AGRDE_10_SELNG_CO": "연령대_10_매출_건수",
    "AGRDE_20_SELNG_CO": "연령대_20_매출_건수",
    "AGRDE_30_SELNG_CO": "연령대_30_매출_건수",
    "AGRDE_40_SELNG_CO": "연령대_40_매출_건수",
    "AGRDE_50_SELNG_CO": "연령대_50_매출_건수",
    "AGRDE_60_ABOVE_SELNG_CO": "연령대_60_이상_매출_건수"
}

df.rename(columns= column_mapping, inplace=True)
df.to_csv('seoul_store.csv',index=False,encoding='cp949')