# 학생 관리 프로그램

# 학생 데이터를 저장할 빈 튜플 생성
students = ()

# 학생 수 입력받기
student_count = int(input("학생 수를 입력하세요: "))

# 각 학생의 이름과 성적을 입력받아 튜플로 저장
for i in range(student_count):
    name = input(f"{i+1}번 학생의 이름을 입력하세요: ")
    score = int(input(f"{name}의 성적을 입력하세요: "))
    # 새로운 학생 정보를 튜플로 만들어 기존 튜플에 추가
    student = (name, score)
    students = students + (student,)

# 성적을 기준으로 정렬하기 위해 임시 리스트 생성
sorted_students = ()
ranks = ()

# 각 학생의 석차 계산
for student in students:
    rank = 1
    for compare in students:
        if student[1] < compare[1]:  # 성적 비교
            rank += 1
    # 이름, 성적, 석차를 포함한 새로운 튜플 생성
    ranked_student = student + (rank,)
    ranks = ranks + (ranked_student,)

# 석차순으로 정렬
for rank in range(1, student_count + 1):
    for student in ranks:
        if student[2] == rank:
            sorted_students = sorted_students + (student,)

# 결과 출력
print("\n=== 학생 성적 순위 ===")
print("순위\t이름\t성적")
print("-------------------")
for student in sorted_students:
    print(f"{student[2]}등\t{student[0]}\t{student[1]}점")

# 석차순으로 정렬