import open_dart_xml as dart
result = dart.get_data_dart()
# sqlite3 데이터베이스 생성 테이블 생성 데이터 삽입
import sqlite3

# 1. SQLite DB 연결 (파일: company.db)
conn = sqlite3.connect("company.db")
cur = conn.cursor()

# 2. 테이블 생성 (corp_code를 PK로 설정)
cur.execute("""
CREATE TABLE IF NOT EXISTS company (
    corp_code TEXT PRIMARY KEY,
    corp_name TEXT
)
""")

# 3. 파이썬 리스트 데이터 (예시)
data_list = [
    ("00434003", "다코"),
    ("00123456", "삼성전자"),
    ("00789012", "LG화학"),
    ("00987654", "현대자동차")
]

# 4. executemany()를 사용해 한 번에 추가
cur.executemany("INSERT OR IGNORE INTO company (corp_code, corp_name) VALUES (?, ?)", data_list)

# 5. 저장 후 닫기
conn.commit()
conn.close()

print("데이터 저장 완료 ✅")
