import requests
import dotenv
import os
dotenv.load_dotenv()  # .env 환경변수 파일을 로드함

key = os.getenv('OPEN_DART_KEY')
url = 'https://opendart.fss.or.kr/api/list.json'
params = {
    'crtfc_key': key, 
}

response = requests.get(url, params=params)
if response.status_code == 200:
    print(response.json())
else:
    print('Error:', response.status_code, response.text)