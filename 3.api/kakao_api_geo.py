import requests

# 발급받은 REST API 키 입력
KAKAO_API_KEY = "발급받은_본인_API_KEY"

def get_address_from_coords(x, y):
    """
    위도(y), 경도(x)를 입력받아 카카오 지도 API로 주소를 가져옴
    """
    url = "https://dapi.kakao.com/v2/local/geo/coord2address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"x": x, "y": y}

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
    # 예: 서울 시청 좌표 (경도, 위도)
    longitude = 126.978652
    latitude = 37.566826

    address = get_address_from_coords(longitude, latitude)
    print("주소:", address)
