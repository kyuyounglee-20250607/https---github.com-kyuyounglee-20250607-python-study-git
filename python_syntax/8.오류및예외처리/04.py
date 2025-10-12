# 음수는 있으면 안되다
# 음수값이 발생되면 경로메세지를 출력하고 해당 데이터를 무시
# 음수값이 발견되면 예외를 우리가 발생시켜서 해당 오류를 except에서 처리
purchases = [1000,2000,-3000,5000,3000]
# 총 구매금액
total = 0
for p in purchases:
    try:
        if p < 0:  #음수
            raise ValueError(f"음수 금액 발견 : {p}")
        total += p
    except ValueError as e:
        print(f'오류 : {e}  해당 데이터 건너뜀')

print(f'총 구매액 : {total}')
