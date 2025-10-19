import os
import requests
import pandas as pd
from dotenv import load_dotenv
import time
from tqdm import tqdm

# .env 파일에서 환경변수 로드
load_dotenv()

def get_total_count():
    """전체 데이터 수를 조회하는 함수"""
    api_key = os.getenv('SEOUL_LANDMARK_API')
    url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/tbLnOpendataRentV/1/1/"
    
    try:
        response = requests.get(url)
        data = response.json()
        return data['tbLnOpendataRentV']['list_total_count']
    except Exception as e:
        print(f"데이터 수 조회 중 오류 발생: {e}")
        return 0

def get_rent_data(start_idx, end_idx):
    """임대차 정보를 조회하는 함수"""
    api_key = os.getenv('SEOUL_LANDMARK_KEY')
    url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/tbLnOpendataRentV/{start_idx}/{end_idx}/"
    
    try:
        response = requests.get(url)
        data = response.json()
        return data['tbLnOpendataRentV']['row']
    except Exception as e:
        print(f"데이터 조회 중 오류 발생: {e}")
        return []

def main():
    # 전체 데이터 수 조회
    total_count = get_total_count()
    print(f"전체 데이터 수: {total_count}")
    
    if total_count == 0:
        print("데이터를 가져올 수 없습니다.")
        return
    
    # 데이터를 저장할 리스트
    all_data = []
    
    # 전체 반복 횟수 계산
    total_iterations = (total_count + 9) // 10  # 올림 나눗셈
    
    # 10페이지씩 데이터 조회 (tqdm으로 진행률 표시)
    page_size = 10
    for start in tqdm(range(1, total_count + 1, page_size), 
                     total=total_iterations,
                     desc="데이터 수집 진행률",
                     unit="페이지"):
        end = min(start + page_size - 1, total_count)
        data = get_rent_data(start, end)
        all_data.extend(data)
        
        # API 호출 간격 조절
        time.sleep(0.5)
    
    # 데이터프레임 생성
    df = pd.DataFrame(all_data)
    
    # CSV 파일로 저장
    current_time = time.strftime("%Y%m%d_%H%M%S")
    filename = f"seoul_rent_data_{current_time}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"데이터가 {filename}에 저장되었습니다.")
    
    # 데이터 요약 정보 출력
    print("\n데이터 요약:")
    print(f"총 행 수: {len(df)}")
    print("\n컬럼 정보:")
    for col in df.columns:
        print(f"- {col}")

if __name__ == "__main__":
    main()