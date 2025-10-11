purchases = ['1000','2000','3000','500 0','3000']
# 총 구매금액
total = 0
for p in purchases:
    try:
        total += int(p)
    except ValueError:
        print(f'에러 : {p}')

print(f'총 구매액 : {total}')
