import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# 전체 읽기 (Read All)
cursor.execute("SELECT * FROM customers")
all_customers = cursor.fetchall()
print("전체 고객 목록:")
for cust in all_customers:
    print(f"ID: {cust[0]}, 이름: {cust[1]}, 이메일: {cust[2]}, 나이: {cust[3]}, 포인트: {cust[4]}")

# 특정 읽기 (WHERE로 필터)
cursor.execute("SELECT name, email FROM customers WHERE age > 20")
adults = cursor.fetchall()
print("\n20세 이상 고객:")
for cust in adults:
    print(f"{cust[0]}: {cust[1]}")

# 단일 읽기 (by ID)
cursor.execute("SELECT * FROM customers WHERE id = 1")
single = cursor.fetchone()
if single:
    print(f"\nID 1 고객: {single[1]} ({single[3]}세)")

conn.close()