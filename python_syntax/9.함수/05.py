# 현실적으로 가장 많이 사용되는 패턴
# 매개변수가 많을때
# 첫번째나 두번째 혹은 많은 3번째 까지는 positional
# 나머지는 전부 default parameter

# 학생들의 정보는 리스트로 받고  옵션을 줘서 다양하게 값을 리턴
print()
def students_info(scores, is_max=None, is_min=None, is_avg=None):
    if is_max:
        return max(scores)
    elif is_min:
        return min(scores)
    elif is_avg:
        return sum(scores)/len(scores)
    else:
        return scores

import random
student_scores = []
for i in range(10):
    student_scores.append(random.randint(0,100))

print(f'scores = {students_info(student_scores)}')
print(f'scores = {students_info(student_scores, is_max=True)}')


