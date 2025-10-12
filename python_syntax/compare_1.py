# 비교연산자
# ==, !=, >, <, >=, <=
# is, is not
# is    : 객체의 동일성(메모리 주소 비교)
# ==    : 객체의 동등성(값 비교)
a = [1, 2, 3]
# b = [1, 2, 3]
b = a
print(a == b)      # True  (값이 같다)       
print(a is b)     # False (메모리 주소가 다르다)

# in, not in
# - 시퀀스 자료형(문자열, 리스트, 튜플, 딕셔너리(key값 비교), set)
# - 특정 값이 시퀀스 자료형에 포함되어 있는지 확인
print(10 in a)

# 논리연산자
# and, or, not
# ~  이고 ~ 이다  (and)    맛있다 그리고 저렴하다
# ~ 이거나 ~ 이다 (or)   맛있다 또는 저럼하다
# ~ 이 아니다   (not)  
x = 0
x > 5 and x < 10  # 6 7 8 9

age = 0
age <= 8 or age >= 65
kor = 0 ; eng = 0; math = 0 ; avg = 0
avg >=60 and kor >=40 and eng >=40 and math >=40
