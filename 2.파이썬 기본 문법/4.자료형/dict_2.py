# 학생관리 프로그램
# 학생 - 이름, 나이 ,과목(국어,영어,수학)

s1 = {
    "name": "홍길동",
    "age": 20,
    "subjects": {
        "국어": 90,
        "영어": 85,
        "수학": 95
    }
}
s2 = {
    "name": "이순신",
    "age": 25,
    "subjects": {
        "국어": 99,
        "영어": 98,
        "수학": 100
    }
}
students = [s1, s2]
# 홍길동의 영어점수를 80으로 변경
students[0]['subjects']['영어'] = 80
print(students[0]['subjects']['영어'])