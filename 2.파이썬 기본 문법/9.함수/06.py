# 함수 전달하는 매개변수가 가변적일때
# temp(1)
# temp(1,2)
# temp(12,3,4,3,2,3,4,3)

# 가변 매개변수
def temp(*params):  # packing
    print(type(params))
    for i in params:
        print(i)  # 적절한 로직

temp( 1,2,4 )

v1,v2 = (100,10)   # unpacking
print(f'v1 : {v1}')


def Test(*args,name=''):
    pass

Test(1,2,3)
Test(1,2,3,name='홍길동')


# positional, defualt, 가변
# def Test(*args,data):  Test(1,2,3,4)  X
# def Test(data,*args):  Test(1,2,3,4)  O

# 25000￦  25000$
price = '25000￦'
if price[-1] == '￦':
    pass


def convert(price , conver = '￦'):
    if conver == '$':
        pass
    elif conver == '￦':
        pass   


convert(price, conver='$')