# 기본 매개변수
def welcome_customer(name, addr,age ):
    return f'{name}, {age}세 {addr}지역 고객님 환영합니다.'

# print(welcome_customer('홍길동' ) )
# print(welcome_customer('홍길동','경기' ) )
print(welcome_customer('홍길동','경기',20 ) )

print(welcome_customer(age = 20,addr = '경기', name = '홍길동' ) )
print(welcome_customer('홍길동',addr = '경기', age = 20 ) )
# print(welcome_customer(age = 20, '경기', name = '홍길동' ) )
