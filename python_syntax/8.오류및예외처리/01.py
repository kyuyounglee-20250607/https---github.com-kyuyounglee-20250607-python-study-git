import traceback
try:
    print('로직1')
    print('로직2')
    print('로직3')
    int('asdfasdf')
    print('오류발생')
    print('로직4')
    print('정상종료')
except:
    traceback.print_exc()

print('종료.....')
