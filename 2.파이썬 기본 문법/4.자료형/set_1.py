# SET의 기본 사용법
# - 중복을 허용하지 않는다
# - 순서를 보장하지 않는다
# - 집합연산 가능(교집합, 합집합, 차집합)
# - 서로 다른 자료형끼리 전환이 가능하다( 리스트 <--> 튜플)

# 1. SET 생성 및 중복 제거 예제
numbers = {1, 2, 2, 3, 3, 4, 5, 5}  # 중복된 숫자를 포함하여 SET 생성
print("중복이 제거된 SET:", numbers)  # 출력: {1, 2, 3, 4, 5}

# 2. 순서가 보장되지 않는 특성 보여주기
fruits = {'apple', 'banana', 'orange', 'grape'}
print("SET의 요소들 (순서 무작위):", fruits)  # 실행할 때마다 순서가 다를 수 있음

# 3. 집합 연산 예제
set_A = {1, 2, 3, 4, 5}
set_B = {4, 5, 6, 7, 8}

# 교집합 (intersection)
intersection = set_A & set_B
print("교집합:", intersection)  # 출력: {4, 5}

# 합집합 (union)
union = set_A | set_B
print("합집합:", union)  # 출력: {1, 2, 3, 4, 5, 6, 7, 8}

# 차집합 (difference)
difference = set_A - set_B
print("차집합 (A-B):", difference)  # 출력: {1, 2, 3}

# 4. 자료형 변환 예제
# 리스트를 SET으로 변환
my_list = [1, 2, 2, 3, 3, 4]
list_to_set = set(my_list)
print("리스트를 SET으로 변환:", list_to_set)  # 출력: {1, 2, 3, 4}

# SET을 리스트로 변환
set_to_list = list(list_to_set)
print("SET을 리스트로 변환:", set_to_list)  # 출력: [1, 2, 3, 4]