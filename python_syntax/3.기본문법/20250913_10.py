# delete
# 1.빈 리스트 생성
# 2. append를 이용해서 데이터를 추가
# 3. pop을 이용해서 데이터를 삭제
# 4. 또다른 리스트를 준비해서 3번에서 삭제한 인덱스,데이터  저장
# 5. 저장된 리스트에 역순으로 데이터를 뽑아서 insrt를 이용해서 복원
import time
data = []
# num = input('숫자 입력 : ')
# num = int(num)
# data.append(num)
data.append( int(input('숫자 입력 : ')) )  # 10
data.append( int(input('숫자 입력 : ')) )  # 30
data.append( int(input('숫자 입력 : ')) )  # 20 
print('data = ',data)  # [10,30,20]
# 삭제
removed_list = []
removed_data = data.pop(1)  # data  [10,20]   
removed_list.append( [1,removed_data]  )  # [  [1,30 ]  ]
time.sleep(1)
print('data = ',data)

removed_data = data.pop(0)  # data  [20]   
removed_list.append( [0,removed_data]  )  # [  [1,30 ], [0,10]  ]
time.sleep(1)
print('data = ',data)

removed_data = data.pop(0)  # data  []   
removed_list.append( [0,removed_data]  )  # [  [1,30 ], [0,10], [0,20]  ]
time.sleep(1)
print('data = ',data)
#삭제순서 [10,30,20]  [10,20]  [20] []
#복원순서 [20]  [10,20]  [10,30,20]
data.insert( removed_list[2][0], removed_list[2][1]   )
print('복원 ',data)
time.sleep(1)

data.insert( removed_list[1][0], removed_list[1][1]   )
print('복원 ',data)
time.sleep(1)

data.insert( removed_list[0][0], removed_list[0][1]   )
print('복원 ',data)




