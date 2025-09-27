import requests

import dotenv
import os
dotenv.load_dotenv()  # .env 환경변수 파일을 로드함


# 발급받은 REST API 키 입력
KAKAO_API_KEY = os.getenv("REST_API")

def get_coords_from_address(address):
    """
    위도(y), 경도(x)를 입력받아 카카오 지도 API로 주소를 가져옴
    """
    # url = "https://dapi.kakao.com/v2/local/geo/coord2address.json"
    url = 'https://dapi.kakao.com/v2/local/search/address.json'
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {'query':address}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        result = response.json()
        if result.get("documents"):
            return result["documents"][0]["address"]
        else:
            return None
    else:
        print("Error:", response.status_code, response.text)
        return None


if __name__ == "__main__":
    address = '서울특별시 강남구 강남대로78길 8'

    address = get_coords_from_address(address)
    # print("결과:", address)
    # 보기편하기 들여쓰기를 3만큼  ensure_ascii=False 한글깨짐을 방지
    import json
    print(json.dumps(address,indent=3,ensure_ascii=False))
    print()
    print(f'{address["x"]},{address["y"]} ')
