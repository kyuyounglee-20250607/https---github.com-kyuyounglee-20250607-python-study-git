import requests
import dotenv
import os
dotenv.load_dotenv()  # .env 환경변수 파일을 로드함

key = os.getenv('OPEN_DART_KEY')
url = 'https://opendart.fss.or.kr/api/corpCode.xml'
params = {
    'crtfc_key': key,     

}

response = requests.get(url, params=params)
if response.status_code == 200:
    # binary 파일
    with open('codes.zip','wb') as f:
        f.write(response.content)
    print('파일 다운로드 성공')
else:
    print('Error:', response.status_code, response.text)