import yfinance as yf

# 삼성전자 주가 조회
ticker = "005930.KS"  # 티커
stock = yf.Ticker(ticker)

# 최근 1개월 주가 데이터
hist = stock.history(period="1mo")
print(hist)

# 현재 주가 정보
print(stock.info['currentPrice'])
