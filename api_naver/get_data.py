import os
import sys
import urllib.request
import dotenv
import os
dotenv.load_dotenv()  # .env 환경변수 파일을 로드함


# 발급받은 REST API 키 입력
client_id = os.getenv("CLIENT_ID")
client_secret= os.getenv("CLIENT_SECRET")

encText = urllib.parse.quote("MCP")
url = "https://openapi.naver.com/v1/search/blog?query=" + encText # JSON 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)