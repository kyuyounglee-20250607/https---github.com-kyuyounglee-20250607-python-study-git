# 파이썬 프로그래밍 가이드

## 기본 입출력

### 콘솔 출력 (print)

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

### 사용자 입력 (input)

```python
# 사용자 입력 받기
name = input('이름을 입력하세요: ')
score = int(input('점수를 입력하세요: '))  # 문자열을 정수로 변환
```

## 변수와 자료형

### 변수 기본

```python
# 변수 선언
name = '홍길동'  # 문자열
age = 25      # 정수
height = 175.5  # 실수
is_student = True  # 불리언

# 다중 할당
var01 = var02 = 20  # 같은 값을 여러 변수에 할당
```

### 기본 자료형

- **정수형(int)**: `10`, `-5`, `1000`
- **실수형(float)**: `3.14`, `-0.001`, `2.0`
- **문자열(str)**: `"Hello"`, `'Python'`
- **불리언(bool)**: `True`, `False`

## 복합 자료구조

### 순차형 - 리스트

```python
# 생성과 기본 연산
list_1 = [1, 2, 3]
list_2 = [4, 5, 6]
print(list_1 + list_2)  # 연결
list_1.extend(list_2)   # 확장

# 수정과 삭제
list_1.append(4)        # 끝에 추가
list_1.insert(1, 5)     # 특정 위치에 추가
list_1.pop()            # 마지막 요소 삭제
list_1.pop(0)           # 특정 위치 요소 삭제
```

### 불변 시퀀스 - 튜플

```python
# 생성과 연산
tuple_1 = (1, 2, 3, 4, 5)
tuple_2 = (10, 20)

# 접근과 슬라이싱
first = tuple_1[0]       # 첫 번째 요소
last = tuple_1[-1]       # 마지막 요소
subset = tuple_1[1:4]    # 슬라이싱
```

### 집합형 - 셋

```python
# 중복 제거와 생성
unique_numbers = {1, 2, 2, 3, 3, 4, 5}  # {1, 2, 3, 4, 5}

# 집합 연산
set_A = {1, 2, 3, 4, 5}
set_B = {4, 5, 6, 7, 8}

intersection = set_A & set_B  # 교집합
union = set_A | set_B        # 합집합
difference = set_A - set_B   # 차집합
```

### 키-값 쌍 - 딕셔너리

```python
# 기본 구조
student = {
    "이름": "홍길동",
    "나이": 20,
    "성적": {
        "국어": 90,
        "영어": 85,
        "수학": 95
    }
}

# 접근과 수정
print(student["이름"])           # 값 접근
student["나이"] = 21            # 값 수정
hobby = student.get("취미", "없음")  # 안전한 접근
```

## 제어 구조

### 조건문과 비교

```python
# 기본 조건문
score = 85
if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
else:
    grade = 'F'

# 비교 연산자
x = 10
y = 20
print(x == y)    # 같다
print(x != y)    # 다르다
print(x > y)     # 크다
print(x <= y)    # 작거나 같다

# 논리 연산자
is_valid = True
is_active = False
print(is_valid and is_active)  # 둘 다 참이어야 함
print(is_valid or is_active)   # 하나라도 참이면 됨
```

## 고급 활용

### 데이터 처리

```python
# 리스트 컴프리헨션
squares = [x**2 for x in range(10)]

# 딕셔너리 순회
for key, value in student.items():
    print(f"{key}: {value}")

# 필터링
even_numbers = [x for x in range(10) if x % 2 == 0]
```

### 실무 활용 예시

```python
# 직원 관리 시스템
employees = {
    "E001": {
        "기본정보": {
            "이름": "홍길동",
            "부서": "개발부",
            "직급": "선임"
        },
        "급여정보": {
            "기본급": 4500000,
            "수당": {
                "야근": 200000,
                "식대": 300000
            }
        }
    }
}

# 총급여 계산
def calculate_total_salary(emp_id):
    emp = employees[emp_id]
    base = emp["급여정보"]["기본급"]
    allowances = sum(emp["급여정보"]["수당"].values())
    return base + allowances
```

## 프로그래밍 실전 팁

### 코딩 스타일

1. **명확성**
   - 의미 있는 변수명 사용
   - 적절한 들여쓰기
   - 명확한 주석 작성

2. **효율성**
   - 적절한 자료구조 선택
   - 불필요한 반복 제거
   - 메모리 사용 최적화

3. **유지보수성**
   - 모듈화된 코드 작성
   - 일관된 코딩 스타일 유지
   - 문서화
