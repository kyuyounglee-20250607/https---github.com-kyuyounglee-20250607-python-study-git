import os
import sys
import urllib.request
import json
import sqlite3
import re
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

def get_api_data(query, display, start, sort):
    """
    네이버 검색 API를 호출하여 결과를 반환합니다.
    """
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not client_id or not client_secret:
        print("환경변수 NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET을 설정해주세요.")
        sys.exit(1)

    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/blog.json?query={encText}&display={display}&start={start}&sort={sort}"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            return json.loads(response_body.decode('utf-8'))
        else:
            print(f"Error Code: {rescode}")
            return None
    except Exception as e:
        print(f"API 호출 중 오류 발생: {e}")
        return None

def clean_html(text):
    """
    HTML 태그를 제거합니다.
    """
    return re.sub('<.*?>', '', text)

def init_db(db_path='naver_blog.db'):
    """
    데이터베이스와 테이블을 초기화합니다.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 네이버 블로그 검색 결과를 저장할 테이블 생성
    # link는 고유해야 하므로 UNIQUE 제약조건 추가
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS naver_blog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        link TEXT NOT NULL UNIQUE,
        description TEXT,
        bloggername TEXT,
        bloggerlink TEXT,
        postdate DATE
    )
    ''')
    conn.commit()
    return conn

def save_data_to_db(conn, items):
    """
    검색 결과를 데이터베이스에 저장합니다.
    """
    cursor = conn.cursor()
    
    for item in items:
        try:
            cursor.execute('''
            INSERT INTO naver_blog (title, link, description, bloggername, bloggerlink, postdate)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                clean_html(item['title']),
                item['link'],
                clean_html(item['description']),
                item['bloggername'],
                item['bloggerlink'],
                item['postdate']
            ))
        except sqlite3.IntegrityError:
            # UNIQUE 제약조건 위반 (이미 존재하는 link) 시 무시
            print(f"이미 존재하는 데이터입니다: {item['link']}")
        except Exception as e:
            print(f"DB 저장 중 오류 발생: {e}")
            
    conn.commit()

def main():
    """
    메인 실행 함수
    """
    query = "리뷰"  # 검색어
    display = 100   # 한 번에 가져올 검색 결과 개수 (최대 100)
    start = 1       # 검색 시작 위치
    sort = "sim"    # 정렬 옵션 (sim: 정확도순, date: 날짜순)

    db_conn = init_db()
 
    # 1. 첫 호출로 전체 개수(total) 파악
    print("전체 데이터 개수를 파악합니다...")
    first_result = get_api_data(query, 1, 1, sort)
    if not first_result:
        print("API 호출에 실패하여 프로그램을 종료합니다.")
        db_conn.close()
        return
 
    total_count = first_result.get('total', 0)
    # 2. API 제약사항(최대 1000개)에 맞춰 수집할 목표 개수 설정
    target_count = min(total_count, 1000)
    print(f"전체 검색 결과: {total_count}개, 수집 목표: {target_count}개")
 
    # 3. 목표 개수만큼 데이터 수집 반복
    while start <= target_count:
        print(f"데이터 수집 중... (시작 위치: {start}/{target_count})")
        search_result = get_api_data(query, display, start, sort)
        if search_result and search_result.get('items'):
            save_data_to_db(db_conn, search_result['items'])
            start += display # 다음 페이지로 이동
        else:
            print("더 이상 가져올 데이터가 없거나 API 호출에 실패하여 중단합니다.")
            break # 반복 중단
 
    db_conn.close()
    print("데이터 수집 및 저장이 완료되었습니다.")

if __name__ == '__main__':
    main()