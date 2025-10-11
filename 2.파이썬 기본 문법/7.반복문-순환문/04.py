import random
print(random.sample(range(1,101),10))   # 1~100 중에서 랜덤한 10개 추출(중복되지 않는 값들로)
print(random.randint(1,100))  # 1~100 중에서 랜덤한 1

list_1 = []
for _ in range(10):
    num = random.randint(1,15)
    list_1.append(num)

print(f'list_1 = {list_1}')
