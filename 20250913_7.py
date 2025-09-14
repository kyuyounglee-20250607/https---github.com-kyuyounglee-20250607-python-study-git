# 리스트에 데이터 추가
# 맨 마지막에 추가
# 중간에 추가

# 리스트 변수
scores = [10,20,30]
# 추가 - 마지막
scores.append( 100 ) 
print(scores)
# 추가 - 인덱스 위치에 
scores.insert(1,200)
print(scores)
# delete
del scores[0]
print(scores)
scores.pop(0)
print(scores)