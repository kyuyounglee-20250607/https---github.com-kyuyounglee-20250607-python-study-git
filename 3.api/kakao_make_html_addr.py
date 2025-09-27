# make_map.py
def make_kakao_map(key, lat, lng, html_file="map.html"):
    """
    위도(lat), 경도(lng)를 받아
    카카오 지도 전체 화면 + 마커 표시 HTML 생성
    """
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Kakao Map - Fullscreen Marker</title>
        <!-- SDK 로드 (JS 키 필요, autoload=false, 콜백 방식) -->
        <script type="text/javascript"
                src="https://dapi.kakao.com/v2/maps/sdk.js?appkey={key}&libraries=services&autoload=false"></script>
        <style>
            html, body {{
                width: 100%;
                height: 100%;
                margin: 0;
                padding: 0;
            }}
            #map {{
                width: 100%;
                height: 100%;
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>

        <script>
            // SDK 로드 완료 후 지도 생성
            kakao.maps.load(function() {{
                var mapContainer = document.getElementById('map');
                var mapOption = {{
                    center: new kakao.maps.LatLng({lat}, {lng}),
                    level: 3
                }};

                var map = new kakao.maps.Map(mapContainer, mapOption);

                var marker = new kakao.maps.Marker({{
                    position: new kakao.maps.LatLng({lat}, {lng})
                }});
                marker.setMap(map);
            }});
        </script>
    </body>
    </html>
    """

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_code)

    print(f"{html_file} 파일이 생성되었습니다. 브라우저에서 열어보세요!")

if __name__ == "__main__":
    # 예시 좌표: 서울시청
    latitude = 37.566826
    longitude = 126.978652

    make_kakao_map(latitude, longitude)
