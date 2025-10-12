# 고객이 계속 구매 
# 구매한 고객명과 구매금액을 나타내는 두개의 리스트가 값이 쌓인다.
# 특정고객은 여러번 구매할수 있다
# 구매고객 리스트에 중복
# 고객별로 특정 가격 이상 구매한 고객들의 구매 총합
# 홍길동, 26000
# 강감찬, 30000
# 홍길동, 27000

# if 키 not in 딕셔너리:
#     딕셔너리[키] = 값
# else
#     딕셔너리[키] += 값

# 구매고객
customers = ['홍길동','이순신','홍길동','강감찬']
purchases = [10000,20000,15000,30000]
# 고객별 구매금액 의 합을 출력
# ex  고객명:홍길동 / 구매액 : 25000
# ex  고객명:이순신 / 구매액 : 20000
# ex  고객명:강감찬 / 구매액 : 30000
result = {}
for idx,name in enumerate(customers):
    if name not in result:
        result[name] = purchases[idx]
    else:
        result[name] += purchases[idx]

# 출력
for key,value in result.items():
    print(f'고객명:{key} / 구매금액:{value}')