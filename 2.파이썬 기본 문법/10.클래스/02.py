class Teacher:
    def __init__(self,name):
        self.name = name

# 객체 생성
print('객체 생성전')
t = Teacher('홍길동')   # 객체를 생성할때는 반드시 내부의 생성자가 호출 __init__(self)
t2 = Teacher('이순신')
print('객체 생성후')
print(t.name)
print(type(t))

t.age = 10
print(t.age)
print(t2.age)
