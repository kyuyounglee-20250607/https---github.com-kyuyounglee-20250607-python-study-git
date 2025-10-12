score = 85
if score >= 90:
    print('90점 이상입니다.')

print('if와 상관 없는 문장')    


list_1 = [1,2,3]
if 2 in list_1:
    print("2가 list_1에 포함되어 있습니다.")

dict_1={'name':'홍길동','age':20}
if 'name' in dict_1:
    print("name이 dict_1에 포함되어 있습니다.")

# 중첩 조건문
# if 조건문1:
#   if 조건문2:
#     실행문
#   else:
#    실행문
# else:
#   실행문
# 예시
num = 15
if num % 2 == 0:   # 짝수
    if num % 3 == 0:
        print("2와 3의 공배수입니다.")
    else:
        print("2의 배수입니다.")

if num % 2 == 0 and num % 3 == 0:
    print("2와 3의 공배수입니다.")


dong = '101'
ho = '101'
price = "25000"

# "101동 101호의 관리비는 25000원입니다."
print(dong+"동 "+ho+"호의 관리비는 "+price+"원입니다.")
print(f"{dong}동 {ho}호의 관리비는 {price}원입니다.")