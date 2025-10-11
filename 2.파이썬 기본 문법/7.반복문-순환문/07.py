# 고객 리스트 출력
list_1 = ['김','이','박','최','홍']
list_2 = ['철수','미애','영수','영규','민수']
# random.choice(list_1)   list_1 값중에 임의로 한개 선택
import random
customers = []

for i in range(10):
    name = random.choice(list_1) + random.choice(list_2)
    customers.append(name)

# 1. 고개 리스트 출력
for i in customers:
    print(f'고객명 : {i}')

print('-'*100)    
# 고객별 구매 금액 10000 ~ 200000 사이값으로 랜덤하게 생성
purchases = []
for _ in range(10):
    purchases.append(random.randint(10,50)*1000)

# 총 구매금액
total_price = 0
for i in purchases:
    total_price += i
# total_price = sum(purchases)    
print(f'총 구매금액 : {total_price}')

# 25000원 이상 구매한 고객의 수
customer_counts = 0
for i in purchases:
    if i >= 25000:
        customer_counts += 1
print(f'25000이상 구매한 고객의 수 : {customer_counts}')
# 25000원 이상 구매한 고객은 누구?

for idx,price in enumerate(purchases):
    if price >= 25000:
        print(f'고객명 : {customers[idx]}  구매가격 : {price}')