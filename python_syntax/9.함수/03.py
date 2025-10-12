# 이름을 입력하면 주어진 양식으로 인사말을 출력하는 함수
# def hello(name):
#     return f'{name}님 안녕하세요'

# print( hello('홍길동')    )


def vaildate_email(data):    
    if '@' in data\
        and ('.com' in data\
        or '.co.kr' in data\
        or '.jr' in data):
        return True
    else:
        return False

customer_email = 'ab.c@abc.com'
is_valid = vaildate_email(customer_email)
print(f'이메일 {customer_email}  검증 : {is_valid}')
    