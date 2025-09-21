
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