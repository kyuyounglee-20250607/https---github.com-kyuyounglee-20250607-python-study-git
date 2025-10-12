
# 파이썬 내장 DB   name email age loyalty_point
import sqlite3
# db 연결 : 파일 'test.db' 생성
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
# 테이블 생성
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER DEFAULT 18,
        loyalty_points INTEGER DEFAULT 0
    )
''')
# 데이터 생성
customers_data =[
    ('홍길동2','hong2@gmail.com',25),
    ('이순신2','lee2@gmail.com',30,)
]
# db 데이터  삽입
cursor.executemany('''
    INSERT INTO 
        customers (name,email,age) 
        VALUES (?,?,?)'''
        ,customers_data
)
conn.commit()  # db 반영
print('데이터 삽입 완료')
#연결 닫기
conn.close()


