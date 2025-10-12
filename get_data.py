import os
import sys
import urllib.request
import json
import sqlite3
import re
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

def get_api_data(search_type, query, display, start, sort):
    """
    네이버 검색 API를 호출하여 결과를 반환합니다.
    """
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not client_id or not client_secret:
        print("환경변수 NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET을 설정해주세요.")
        sys.exit(1)

    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/{search_type}.json?query={encText}&display={display}&start={start}&sort={sort}"

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
    return re.sub('<.*?>', '', text) if text else ''

def init_db(db_path='naver_search.db'):
    """
    데이터베이스 연결을 초기화합니다.
    """
    conn = sqlite3.connect(db_path)
    return conn

def create_table(conn, search_type):
    """
    검색 유형에 맞는 테이블을 생성합니다.
    """
    cursor = conn.cursor()
    table_name = f"naver_{search_type}"
    
    # 각 API 유형별 필드 정의
    fields = {
        "blog": "id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, link TEXT NOT NULL UNIQUE, description TEXT, bloggername TEXT, bloggerlink TEXT, postdate DATE",
        "news": "id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, originallink TEXT, link TEXT NOT NULL UNIQUE, description TEXT, pubDate DATE",
        "book": "id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, link TEXT NOT NULL UNIQUE, image TEXT, author TEXT, price INTEGER, discount INTEGER, publisher TEXT, pubdate DATE, isbn TEXT, description TEXT",
        "encyc": "id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, link TEXT NOT NULL UNIQUE, description TEXT, thumbnail TEXT",
        "cafearticle": "id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, link TEXT NOT NULL UNIQUE, description TEXT, cafename TEXT, cafeurl TEXT",
        "kin": "id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, link TEXT NOT NULL UNIQUE, description TEXT",
        "local": "id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, link TEXT, category TEXT, description TEXT, telephone TEXT, address TEXT, roadAddress TEXT, mapx INTEGER, mapy INTEGER",
        "webkr": "id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, link TEXT NOT NULL UNIQUE, description TEXT",
        "image": "id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, link TEXT NOT NULL UNIQUE, thumbnail TEXT, sizeheight INTEGER, sizewidth INTEGER",
        "shop": "id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, link TEXT NOT NULL UNIQUE, image TEXT, lprice INTEGER, hprice INTEGER, mallName TEXT, productId TEXT, productType TEXT, brand TEXT, maker TEXT, category1 TEXT, category2 TEXT, category3 TEXT, category4 TEXT",
        "doc": "id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, link TEXT NOT NULL UNIQUE, description TEXT"
    }
    
    if search_type in fields:
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({fields[search_type]})')
    else:
        # 기본 테이블 구조
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, link TEXT NOT NULL UNIQUE, description TEXT)')
        
    conn.commit()


def save_data_to_db(conn, search_type, items):
    """
    검색 결과를 데이터베이스에 저장합니다.
    """
    cursor = conn.cursor()
    table_name = f"naver_{search_type}"

    field_map = {
        "blog": ["title", "link", "description", "bloggername", "bloggerlink", "postdate"],
        "news": ["title", "originallink", "link", "description", "pubDate"],
        "book": ["title", "link", "image", "author", "price", "discount", "publisher", "pubdate", "isbn", "description"],
        "encyc": ["title", "link", "description", "thumbnail"],
        "cafearticle": ["title", "link", "description", "cafename", "cafeurl"],
        "kin": ["title", "link", "description"],
        "local": ["title", "link", "category", "description", "telephone", "address", "roadAddress", "mapx", "mapy"],
        "webkr": ["title", "link", "description"],
        "image": ["title", "link", "thumbnail", "sizeheight", "sizewidth"],
        "shop": ["title", "link", "image", "lprice", "hprice", "mallName", "productId", "productType", "brand", "maker", "category1", "category2", "category3", "category4"],
        "doc": ["title", "link", "description"]
    }

    fields = field_map.get(search_type, ["title", "link", "description"])
    
    for item in items:
        try:
            # HTML 태그 정리
            cleaned_item = {k: clean_html(v) for k, v in item.items()}
            
            values = [cleaned_item.get(field, None) for field in fields]
            
            placeholders = ', '.join(['?'] * len(fields))
            
            cursor.execute(f'''
            INSERT INTO {table_name} ({', '.join(fields)})
            VALUES ({placeholders})
            ''', values)

        except sqlite3.IntegrityError:
            print(f"이미 존재하는 데이터입니다: {item.get('link')}")
        except Exception as e:
            print(f"DB 저장 중 오류 발생: {e}, item: {item}")
            
    conn.commit()


def main():
    """
    메인 실행 함수
    """
    search_types = ['news', 'book', 'encyc', 'cafearticle', 'kin', 'local', 'webkr', 'image', 'shop', 'doc', 'blog']
    query = "MCP"  # 검색어
    display = 100   # 한 번에 가져올 검색 결과 개수 (최대 100)
    sort = "sim"    # 정렬 옵션 (sim: 정확도순, date: 날짜순)

    db_conn = init_db()
 
    for search_type in search_types:
        create_table(db_conn, search_type)
        start = 1
        
        print(f"'{search_type}' 유형의 데이터 수집을 시작합니다.")
        
        # 1. 첫 호출로 전체 개수(total) 파악
        first_result = get_api_data(search_type, query, 1, 1, sort)
        if not first_result:
            print(f"'{search_type}' API 호출에 실패하여 다음으로 넘어갑니다.")
            continue
 
        total_count = first_result.get('total', 0)
        # 2. API 제약사항(최대 1000개)에 맞춰 수집할 목표 개수 설정
        target_count = min(total_count, 1000)
        print(f"전체 검색 결과: {total_count}개, 수집 목표: {target_count}개")
 
        # 3. 목표 개수만큼 데이터 수집 반복
        while start <= target_count:
            print(f"데이터 수집 중... (시작 위치: {start}/{target_count})")
            search_result = get_api_data(search_type, query, display, start, sort)
            if search_result and search_result.get('items'):
                save_data_to_db(db_conn, search_type, search_result['items'])
                start += display # 다음 페이지로 이동
            else:
                print("더 이상 가져올 데이터가 없거나 API 호출에 실패하여 중단합니다.")
                break # 반복 중단
        
        print(f"'{search_type}' 유형의 데이터 수집 및 저장이 완료되었습니다.")
        print("-" * 50)

    db_conn.close()
    print("모든 데이터 수집 및 저장이 완료되었습니다.")

if __name__ == '__main__':
    main()
