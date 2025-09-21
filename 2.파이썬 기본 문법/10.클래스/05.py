
# 파이썬 내장 DB 
class Customer:
    def __init__(self,name,email,age = 18):
        self.name = name
        self.email = email
        self.age = age
        self.loyalty_point = 0  # 포인트
    def earn_points(self,amount):
        self.loyalty_point += amount
        return f'{self.name}님의 현재 포인트는 {self.loyalty_point}입니다.'
    def get_prifile(self):
        return f'프로필:{self.name}({self.age}세), 이메일:{self.email}, \
        포인트:{self.loyalty_point}'

# 인스턴스 생성
c1 = Customer('홍길동','hong@gmail.com',25)
# 메소드 사용
print(c1.earn_points(200))
print(c1.get_prifile())
