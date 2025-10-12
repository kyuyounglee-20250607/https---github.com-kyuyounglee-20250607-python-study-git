# 파이썬 프로그래밍 가이드

## 1. 기본 입출력

### print 함수

```python
# 기본 출력
print("hello world")

# end 옵션 사용
print('a', end=' ')  # 줄바꿈 대신 공백으로 끝냄
print('b')  # 결과: a b

# f-string을 사용한 형식화된 출력
dong = '101'
ho = '101'
print(f"{dong}동 {ho}호")  # 결과: 101동 101호
```

### input 함수

```python
# 사용자 입력 받기
name = input('이름을 입력하세요: ')
score = int(input('점수를 입력하세요: '))  # 문자열을 정수로 변환
```

## 2. 변수와 데이터 타입

### 변수 선언과 할당

```python
# 변수 선언
name = '홍길동'  # 문자열
age = 25      # 정수
height = 175.5  # 실수
is_student = True  # 불리언

# 다중 할당
var01 = var02 = 20  # 같은 값을 여러 변수에 할당
```

### 기본 데이터 타입

- **정수형(int)**: `10`, `-5`, `1000`
- **실수형(float)**: `3.14`, `-0.001`, `2.0`
- **문자열(str)**: `"Hello"`, `'Python'`
- **불리언(bool)**: `True`, `False`

## 3. 자료구조

### 리스트(List)

```python
# 생성
list_1 = [1, 2, 3]

# 연결
list_1 + list_2
list_1.extend(list_2)

# 반복
list_2 * 3

# 추가/삭제
list_1.append(4)    # 끝에 추가
list_1.insert(1, 5) # 특정 위치에 추가
list_1.pop()        # 마지막 요소 삭제
list_1.pop(0)       # 특정 위치 요소 삭제
del list_1[0]       # 특정 위치 요소 삭제

# 복사
shallow_copy = list_1        # 얕은 복사
deep_copy = list_1.copy()   # 깊은 복사
```

### 튜플(Tuple)

```python
# 생성
tuple_1 = (1, 2, 3, 4, 5)

# 연산
print(tuple_1 + (6, 7))  # 튜플 연결
print(tuple_1 * 3)  # 튜플 반복

# 인덱싱과 슬라이싱
print(tuple_1[0])  # 첫 번째 요소
print(tuple_1[-1])  # 마지막 요소
print(tuple_1[1:4])  # 슬라이싱
```

### 셋(Set)

```python
# 생성 및 중복 제거
numbers = {1, 2, 2, 3, 3, 4, 5}  # 결과: {1, 2, 3, 4, 5}

# 집합 연산
set_A = {1, 2, 3, 4, 5}
set_B = {4, 5, 6, 7, 8}

print(set_A & set_B)  # 교집합
print(set_A | set_B)  # 합집합
print(set_A - set_B)  # 차집합
```

### 딕셔너리(Dictionary)

```python
# 기본 사용
student = {
    "이름": "홍길동",
    "나이": 20,
    "과목": {
        "국어": 90,
        "영어": 85,
        "수학": 95
    }
}

# 값 접근 및 수정
print(student["이름"])
student["나이"] = 21

# get 메소드 사용
hobby = student.get("취미", "없음")  # 키가 없을 때 기본값 반환
```

## 4. 제어문

### 조건문

```python
# if-elif-else 구문
score = 85
if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
else:
    grade = 'F'

# 중첩 조건문
num = 15
if num % 2 == 0:
    if num % 3 == 0:
        print("2와 3의 공배수입니다.")
    else:
        print("2의 배수입니다.")
```

### 비교 연산자

```python
# 기본 비교
==  # 같다
!=  # 다르다
>   # 크다
<   # 작다
>=  # 크거나 같다
<=  # 작거나 같다

# 객체 비교
is     # 객체 동일성(메모리 주소 비교)
==     # 값 동등성

# 포함 여부
in     # 포함되어 있는지
not in # 포함되어 있지 않은지

# 논리 연산자
and  # 그리고
or   # 또는
not  # 아님
```

## 5. 고급 사용 예시

### 중첩 데이터 구조

```python
# 복잡한 데이터 구조 예시
company = {
    "departments": {
        "개발부": {
            "직원수": 15,
            "예산": 500000000
        }
    },
    "employees": {
        "E001": {
            "이름": "홍길동",
            "부서": "개발부",
            "급여정보": {
                "기본급": 4500000,
                "수당": {
                    "야근수당": 200000
                }
            }
        }
    }
}
```

### 데이터 처리

```python
# 리스트 컴프리헨션
squares = [x**2 for x in range(10)]

# 딕셔너리 순회
for key, value in student.items():
    print(f"{key}: {value}")

# 중첩 구조 접근
total_salary = company["employees"]["E001"]["급여정보"]["기본급"]
```

## 6. 프로그래밍 팁

### 코드 작성 원칙

1. **가독성**
   - 의미 있는 변수명 사용
   - 적절한 들여쓰기
   - 주석 활용

2. **데이터 구조 선택**
   - 리스트: 순서가 있는 데이터
   - 튜플: 변경되지 않는 데이터
   - 셋: 중복이 없는 데이터
   - 딕셔너리: 키-값 쌍의 데이터

3. **에러 처리**
   - try-except 구문 활용
   - 적절한 예외처리

## 1. 기본 입출력

### print 함수

```python
# 기본 출력
print("hello world")

# end 옵션 사용
print('a', end=' ')  # 줄바꿈 대신 공백으로 끝냄
print('b')  # 결과: a b

# f-string을 사용한 형식화된 출력
dong = '101'
ho = '101'
print(f"{dong}동 {ho}호")  # 결과: 101동 101호
```

### input 함수

```python
# 사용자 입력 받기
name = input('이름을 입력하세요: ')
score = int(input('점수를 입력하세요: '))  # 문자열을 정수로 변환
```

## 2. 변수와 데이터 타입

### 변수 선언과 할당

```python
# 변수 선언
name = '홍길동'  # 문자열
age = 25      # 정수
height = 175.5  # 실수
is_student = True  # 불리언

# 다중 할당
var01 = var02 = 20  # 같은 값을 여러 변수에 할당
```

### 기본 데이터 타입

- **정수형(int)**: `10`, `-5`, `1000`
- **실수형(float)**: `3.14`, `-0.001`, `2.0`
- **문자열(str)**: `"Hello"`, `'Python'`
- **불리언(bool)**: `True`, `False`

## 3. 자료구조

### 리스트(List)

```python
# 생성
scores = [10, 20, 30, 40, 50]

# 추가
scores.append(100)  # 끝에 추가
scores.insert(1, 200)  # 특정 위치에 추가

# 삭제
del scores[0]  # 인덱스로 삭제
scores.pop()  # 마지막 요소 삭제
scores.pop(0)  # 특정 위치 요소 삭제

# 복사
shallow_copy = scores  # 얕은 복사
deep_copy = scores.copy()  # 깊은 복사
```

### 튜플(Tuple)
```python
# 생성
tuple_1 = (1, 2, 3, 4, 5)

# 연산
print(tuple_1 + (6, 7))  # 튜플 연결
print(tuple_1 * 3)  # 튜플 반복

# 인덱싱과 슬라이싱
print(tuple_1[0])  # 첫 번째 요소
print(tuple_1[-1])  # 마지막 요소
print(tuple_1[1:4])  # 슬라이싱
```

### 셋(Set)
```python
# 생성 및 중복 제거
numbers = {1, 2, 2, 3, 3, 4, 5}  # 결과: {1, 2, 3, 4, 5}

# 집합 연산
set_A = {1, 2, 3, 4, 5}
set_B = {4, 5, 6, 7, 8}

print(set_A & set_B)  # 교집합
print(set_A | set_B)  # 합집합
print(set_A - set_B)  # 차집합
```

### 딕셔너리(Dictionary)
```python
# 기본 사용
student = {
    "이름": "홍길동",
    "나이": 20,
    "과목": {
        "국어": 90,
        "영어": 85,
        "수학": 95
    }
}

# 값 접근 및 수정
print(student["이름"])
student["나이"] = 21

# get 메소드 사용
hobby = student.get("취미", "없음")  # 키가 없을 때 기본값 반환
```

## 4. 제어문

### 조건문
```python
# if-elif-else 구문
score = 85
if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
else:
    grade = 'F'

# 중첩 조건문
num = 15
if num % 2 == 0:
    if num % 3 == 0:
        print("2와 3의 공배수입니다.")
    else:
        print("2의 배수입니다.")
```

### 비교 연산자
```python
# 기본 비교
==  # 같다
!=  # 다르다
>   # 크다
<   # 작다
>=  # 크거나 같다
<=  # 작거나 같다

# 객체 비교
is     # 객체 동일성(메모리 주소 비교)
==     # 값 동등성

# 포함 여부
in     # 포함되어 있는지
not in # 포함되어 있지 않은지

# 논리 연산자
and  # 그리고
or   # 또는
not  # 아님
```

## 5. 고급 사용 예시

### 중첩 데이터 구조
```python
# 복잡한 데이터 구조 예시
company = {
    "departments": {
        "개발부": {
            "직원수": 15,
            "예산": 500000000
        }
    },
    "employees": {
        "E001": {
            "이름": "홍길동",
            "부서": "개발부",
            "급여정보": {
                "기본급": 4500000,
                "수당": {
                    "야근수당": 200000
                }
            }
        }
    }
}
```

### 데이터 처리
```python
# 리스트 컴프리헨션
squares = [x**2 for x in range(10)]

# 딕셔너리 순회
for key, value in student.items():
    print(f"{key}: {value}")

# 중첩 구조 접근
total_salary = company["employees"]["E001"]["급여정보"]["기본급"]
```

## 6. 프로그래밍 팁

1. **가독성**
   - 의미 있는 변수명 사용
   - 적절한 들여쓰기
   - 주석 활용

2. **데이터 구조 선택**
   - 리스트: 순서가 있는 데이터
   - 튜플: 변경되지 않는 데이터
   - 셋: 중복이 없는 데이터
   - 딕셔너리: 키-값 쌍의 데이터

3. **에러 처리**
   - try-except 구문 활용
   - 적절한 예외처리