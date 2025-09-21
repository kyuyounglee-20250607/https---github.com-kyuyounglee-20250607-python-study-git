# 함수
# def 이름( 매개변수 ):
    # 코드 또는 
    # 변수 선언 및 
    # 사용
    # return 반환값

# 함수  사용
# 이름()


# 매개변수 : 함수를 호출하는 사용자가 데이터를 전달하면 함수가 매개변수로 받아서 함수안에서 사용

# 두개의 정수를 받아서 합을 리턴하는 함수
def add( x, y): # parameter  매개변수
    print( x+y)

result = add([1,2,3],[10,20,30])
print(result)

# 매개변수도 없어도 된다
def shot_info():
    print('제품정보는 다음과 같습니다.')
    # 생략

shot_info()


