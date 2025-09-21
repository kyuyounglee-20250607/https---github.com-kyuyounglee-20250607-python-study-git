import sqlite3

class DB_Read:
    def __init__(self,db_name = 'test.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.all_customers = None
    def close(self):
        self.conn.close()
    def read_all(self,table_name='customers'):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        self.all_customers = self.cursor.fetchall()
    def print_all(self):
        print("전체 고객 목록:")
        for cust in self.all_customers:
            print(f"ID: {cust[0]}, 이름: {cust[1]}, 이메일: {cust[2]}, 나이: {cust[3]}, 포인트: {cust[4]}")
db_read = DB_Read()
db_read.read_all()
db_read.print_all()
db_read.close()