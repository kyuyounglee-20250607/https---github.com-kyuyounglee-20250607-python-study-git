import requests

import dotenv
import os
dotenv.load_dotenv()  # .env 환경변수 파일을 로드함
OPEN_WEATHER_MAP_KEY = os.getenv("OPEN_WEATHER_MAP_KEY")

url = 'http://api.openweathermap.org/data/2.5/weather'
params = {
    'q': 'London',    
    'appid': OPEN_WEATHER_MAP_KEY,
    'units':'metric'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    import json
    data = response.json()
    print(json.dumps(data, indent=4,ensure_ascii=False))    
else:
    print('Error:', response.status_code)



