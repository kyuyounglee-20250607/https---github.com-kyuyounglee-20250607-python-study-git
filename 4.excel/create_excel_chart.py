import pandas as pd

# 1. 제공된 데이터로 데이터프레임 생성
data = {
    '지역': ['Oporto', 'lisbon', '기타'],
    '신선식품_합계': [464721, 854833, 3960577],
    '유제품_합계': [239144, 422454, 1888759],
    '식료품_합계': [433274, 570037, 2495251],
    '냉동식품_합계': [190132, 231026, 930492],
    '세제및종이류_합계': [173311, 204136, 890410],
    '고급식품_합계': [54506, 104327, 512110],
}
df = pd.DataFrame(data)

# 2. 엑셀 파일로 저장
excel_file = 'd:\\week_src\\4.excel\\product_report_by_region.xlsx'
writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
df.to_excel(writer, sheet_name='데이터', index=False)

# 3. 워크북 및 워크시트 객체 가져오기
workbook = writer.book
worksheet = writer.sheets['데이터']

# 4. 차트 생성
chart = workbook.add_chart({'type': 'column'})

# 5. 차트 데이터 계열 추가 (각 품목을 계열로)
num_regions = len(df)
# Iterate over each product column to add it as a series
for i, col_name in enumerate(df.columns[1:], 1):
    chart.add_series({
        'name':       ['데이터', 0, i],  # 품목 이름 (e.g., '신선식품_합계')
        'categories': ['데이터', 1, 0, num_regions, 0], # 지역 이름 (X-axis)
        'values':     ['데이터', 1, i, num_regions, i], # 해당 품목의 지역별 값
        'data_labels': {'value': True, 'num_format': '#_-'},
    })

# 6. 차트 축 및 제목 설정
chart.set_title({'name': '지역별 상품 판매 현황'})
chart.set_x_axis({'name': '지역'})
chart.set_y_axis({'name': '수량'})

# 7. 차트 스타일 및 크기 설정
chart.set_style(10)
worksheet.insert_chart('A10', chart, {'x_scale': 2, 'y_scale': 2})

# 8. 엑셀 파일 저장
writer.close()

print(f"엑셀 파일이 생성되었습니다: {excel_file}")