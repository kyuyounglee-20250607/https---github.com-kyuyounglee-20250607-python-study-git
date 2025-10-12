# 함수를 매개변수로 받는 함수
def calc(func,a,b):
    return func(a,b)

def plus(a,b):
    return a+b

def minus(a,b):
    return a-b

print(calc(plus,10,20))  # 30
print(calc(minus,10,20)) # -10
print(list(calc(range,1,10)))  # list(range(1,10))
import random 
print(calc(random.randint,1,10) ) # print(random.randint(1,10))

# 람다함수는 이름없이 기능만 제공하는 함수 재사용 불가
# 함수를 매개변수로 사용하는 함수에 제공하는 역활

# lambda x : x*2

# def temp(x):
#     return x*2


# def multi(a,b):
#     return a*b

print( calc(lambda a,b : a*b, 10 ,20) )