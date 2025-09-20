customer_data = [
    ('김민수','15000'),
    ('이서연','-23000'),
    ('최지훈','wrong data'),
    ('박소연','45000'),
    ('정우진',None)
]
# 구매금액이 없을때  raise ValueError('구매금액이 없습니다')
# 음수 raise ValueError('구매금액이 음수입니다')
# 나머지는 시스테이 발행하는 예외를 처리

#유효한 데이터 
valid_data = []
# 에러 저장
error_log = []

for name,p in customer_data:
    try:
        if p is None:
            pass  # 예외 발생
        amount = int(p)
        if amount < 0 :
            pass # 예외 발생
    except ValueError as e:
        error_log.append(f'{name}: {e}')
    except TypeError:
        error_log.append(f'{name}: 데이터 형식이 잘못되었습니다.')
    else:
        valid_data.append((name,amount))
print(f'유효한 데이터 : {valid_data}')
print(f'오류 로그 : {error_log}')
    