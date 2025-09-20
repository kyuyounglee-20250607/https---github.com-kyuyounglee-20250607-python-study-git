# for
    # 순환하는 횟수가 지정
    # range(),  자료구조(list, tuple, set ,dict)
# while
    # 횟수는 없고 매 순환할때마다 조건을 판단해서 True

# 5번 반복
for i in range(5):
    print(i)
# 자료구조를 반복
for name in ['a','b','c']:
    print(name)    

# tuple 자료 순환
tuple_1 = (10,20,30)    
for i in tuple_1:
    print(f'i = {i}')

set_1 = {1,5,10}    
for i in set_1:
    print(f'i = {i}')

dict_1 = {
    'name':'홍길동',
    'age':20,
    'addr':'서울'
}
# dict자체는  key값들만 대상
for i in dict_1:
    print(f'i = {i}')
# .keys()  키 값들만 리스트형태로 반환
for i in dict_1.keys():
    print(f'i = {i}')    
# .values() 값들만 리스트 형태로 반환
for i in dict_1.values():
    print(f'i = {i}')    
# .items()  (key,value)  형태의 리스트집합
for i in dict.items():
    print(f'i = {i}')    
