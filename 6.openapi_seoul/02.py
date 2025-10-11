
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
df.to_csv('seoul_store.csv',index=False,encoding='utf-8')