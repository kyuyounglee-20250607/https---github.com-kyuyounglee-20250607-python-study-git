# 랜덤한 데이터 10개를 리스트에 저장하고

# 순환문을 이용해서 저장된 리스트의 각각의 값을 판단해서
# 짝수로 판단되면 새로운 리스트에 추가한다

# 짝수구분   if 값 % 2 == 0  조건을 만족하면 짝수

import random
target = random.sample(range(100),10)
print(f'target = {target}')
even_lists = []

for i in target:
    if i % 2 == 0:  #짝수
        even_lists.append(i)

print(f'짝수의 집합 : {even_lists}')