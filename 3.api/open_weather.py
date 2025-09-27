import requests

import dotenv
import os
dotenv.load_dotenv()  # .env 환경변수 파일을 로드함
OPEN_WEATHER_MAP_KEY = os.getenv("OPEN_WEATHER_MAP_KEY")

url = 'http://api.openweathermap.org/geo/1.0/direct'
params = {
    'q': 'London',
    'limit': 5,
    'appid': OPEN_WEATHER_MAP_KEY
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print('Error:', response.status_code)



