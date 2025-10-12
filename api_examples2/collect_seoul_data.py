
import os
import requests
import sqlite3
from dotenv import load_dotenv
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 상수 정의
DB_NAME = "seoul_data.db"
TABLE_NAME = "job_counseling"

def get_api_key():
    """
    .env 파일에서 서울시 API 키를 로드합니다.
    """
    load_dotenv()
    api_key = os.getenv("SEOUL_API")
    if not api_key:
        raise ValueError("SEOUL_API 키가 .env 파일에 설정되지 않았습니다.")
    return api_key

def get_total_data_count(api_key):
    """
    API를 호출하여 전체 데이터 건수를 가져옵니다.
    """
    url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/GlobalJobCounselLngTypeRst/1/1/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "GlobalJobCounselLngTypeRst" in data:
            return data["GlobalJobCounselLngTypeRst"]["list_total_count"]
        else:
            # API 키가 유효하지 않거나 다른 문제가 있을 경우
            if "RESULT" in data:
                error_msg = data["RESULT"]["MESSAGE"]
                logging.error(f"API 에러: {error_msg}")
            return 0
    except requests.exceptions.RequestException as e:
        logging.error(f"API 요청 중 오류 발생: {e}")
        return 0
    except KeyError:
        logging.error("API 응답에서 'list_total_count'를 찾을 수 없습니다.")
        return 0


def fetch_all_data(api_key, total_count):
    """
    전체 데이터를 1000개 단위로 나누어 모두 가져옵니다.
    """
    all_data = []
    chunk_size = 1000
    for start_index in range(1, total_count + 1, chunk_size):
        end_index = start_index + chunk_size - 1
        if end_index > total_count:
            end_index = total_count
        
        url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/GlobalJobCounselLngTypeRst/{start_index}/{end_index}/"
        logging.info(f"{start_index}부터 {end_index}까지 데이터를 가져옵니다...")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            rows = data.get("GlobalJobCounselLngTypeRst", {}).get("row", [])
            all_data.extend(rows)
        except requests.exceptions.RequestException as e:
            logging.error(f"데이터를 가져오는 중 오류 발생 (URL: {url}): {e}")
            continue # 오류 발생 시 다음 청크로 넘어감
        except KeyError:
            logging.error(f"API 응답 형식이 올바르지 않습니다 (URL: {url})")
            continue

    return all_data

def setup_database():
    """
    SQLite 데이터베이스와 테이블을 생성합니다.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 테이블 생성 (IF NOT EXISTS 사용으로 여러 번 실행해도 문제 없음)
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        YYYYMM TEXT,
        CATEGORY_NM TEXT,
        TYPE0 INTEGER,
        TYPE1 INTEGER,
        TYPE2 INTEGER,
        TYPE3 INTEGER,
        TYPE4 INTEGER,
        TYPE5 INTEGER,
        TYPE6 INTEGER,
        TYPE7 INTEGER,
        TYPE8 INTEGER,
        TYPE9 INTEGER,
        TYPE10 INTEGER,
        TYPE11 INTEGER,
        TYPE12 INTEGER,
        TYPE13 INTEGER,
        TYPE14 INTEGER,
        TYPE15 INTEGER,
        TYPE99 INTEGER,
        TYPE_SUM INTEGER
    )
    """)
    
    # 기존 데이터 삭제
    cursor.execute(f"DELETE FROM {TABLE_NAME}")
    logging.info(f"기존 '{TABLE_NAME}' 테이블의 데이터를 모두 삭제했습니다.")

    conn.commit()
    return conn, cursor

def insert_data(conn, cursor, data):
    """
    가져온 데이터를 데이터베이스에 삽입합니다.
    """
    if not data:
        logging.warning("삽입할 데이터가 없습니다.")
        return

    logging.info(f"총 {len(data)}개의 데이터를 데이터베이스에 삽입합니다...")
    
    for item in data:
        # API 응답의 필드 이름과 DB 컬럼 이름을 매핑
        # 숫자로 된 필드는 정수형으로 변환 (값이 없을 경우 0으로 처리)
        values = (
            item.get("YYYYMM"),
            item.get("CATEGORY_NM"),
            int(item.get("TYPE0", 0) or 0),
            int(item.get("TYPE1", 0) or 0),
            int(item.get("TYPE2", 0) or 0),
            int(item.get("TYPE3", 0) or 0),
            int(item.get("TYPE4", 0) or 0),
            int(item.get("TYPE5", 0) or 0),
            int(item.get("TYPE6", 0) or 0),
            int(item.get("TYPE7", 0) or 0),
            int(item.get("TYPE8", 0) or 0),
            int(item.get("TYPE9", 0) or 0),
            int(item.get("TYPE10", 0) or 0),
            int(item.get("TYPE11", 0) or 0),
            int(item.get("TYPE12", 0) or 0),
            int(item.get("TYPE13", 0) or 0),
            int(item.get("TYPE14", 0) or 0),
            int(item.get("TYPE15", 0) or 0),
            int(item.get("TYPE99", 0) or 0),
            int(item.get("TYPE_SUM", 0) or 0)
        )
        cursor.execute(f"""
        INSERT INTO {TABLE_NAME} (
            YYYYMM, CATEGORY_NM, TYPE0, TYPE1, TYPE2, TYPE3, TYPE4, TYPE5, 
            TYPE6, TYPE7, TYPE8, TYPE9, TYPE10, TYPE11, TYPE12, TYPE13, 
            TYPE14, TYPE15, TYPE99, TYPE_SUM
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, values)
    
    conn.commit()
    logging.info("데이터 삽입이 완료되었습니다.")


def main():
    """
    메인 실행 함수
    """
    try:
        api_key = get_api_key()
        logging.info("API 키를 성공적으로 로드했습니다.")
        
        total_count = get_total_data_count(api_key)
        if total_count == 0:
            logging.warning("가져올 데이터가 없거나 API 키가 유효하지 않습니다.")
            return
            
        logging.info(f"총 {total_count}개의 데이터를 확인했습니다.")
        
        all_data = fetch_all_data(api_key, total_count)
        if not all_data:
            logging.warning("API로부터 데이터를 가져오지 못했습니다.")
            return

        conn, cursor = setup_database()
        insert_data(conn, cursor, all_data)
        
        # 데이터베이스 연결 종료
        conn.close()
        logging.info("데이터베이스 연결을 종료했습니다. 모든 작업이 완료되었습니다.")

    except ValueError as e:
        logging.error(e)
    except Exception as e:
        logging.error(f"예상치 못한 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main()
