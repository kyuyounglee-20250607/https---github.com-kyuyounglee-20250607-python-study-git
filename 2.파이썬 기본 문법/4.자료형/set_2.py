# 리스트 연산자
list_1 = [1,2,3]
list_2 = [4,5,6]
print('list_1 + list_2 = ', list_1 + list_2)  # 리스트 연결

list_1.extend(list_2)
print('list_1 = ',list_1 )  # 리스트 연결
print('list_2 * 3 = ', list_2 * 3)              # 리스트 반복

# 문자열
str_1 = "Hello"
str_2 = "World"
print('str_1 + str_2 = ', str_1 + str_2)  # 문자열 연결
print('str_1 * 3 = ', str_1 * 3)              # 문자열 반복

# set
# 중복허용 안함
set_1 = {1,2,3,4,5,7,8,1,2,3,4,5,6,7}
print('set_1 = ', set_1)
# print(set_1[0])  # set은 인덱싱 불가
# set에서 특정 위치에 단일 값에 접근하려면
print('set_1에서 단일 값에 접근 = ', list(set_1)[0])
# set은 집합 연산이 가능하다
set_1 = {1,2,3,4,5}
set_2 = {4,5,6,7,8}
# 교집합
print('set_1 & set_2 = ', set_1 & set_2)
print('set_1.intersection(set_2) = ', set_1.intersection(set_2))
# 합집합
print('set_1 | set_2 = ', set_1 | set_2)
print('set_1.union(set_2) = ', set_1.union(set_2))
# 차집합
print('set_1 - set_2 = ', set_1 - set_2)
print('set_1.difference(set_2) = ', set_1.difference(set_2))

