# pip install finance-datareader
import pandas as pd
import FinanceDataReader as fdr
from difflib import get_close_matches
import re

def load_stock_data():
    """한국 상장사 데이터 로드"""
    print("📡 상장사 데이터 로딩중...")
    
    # KOSPI + KOSDAQ 데이터 가져오기
    kospi = fdr.StockListing('KOSPI')
    kospi['Market'] = 'KOSPI'
    
    kosdaq = fdr.StockListing('KOSDAQ')
    kosdaq['Market'] = 'KOSDAQ'
    
    # 데이터 합치기 및 정리
    stocks = pd.concat([kospi, kosdaq], ignore_index=True)
    
    # 필요한 컬럼만 선택하고 이름 변경
    stocks = stocks[['Code', 'Name', 'Market']].rename(columns={
        'Code': 'ticker', 
        'Name': 'name', 
        'Market': 'market'
    })
    
    # 티커를 6자리 문자열로 변환
    stocks['ticker'] = stocks['ticker'].astype(str).str.zfill(6)
    
    # 야후 파이낸스 심볼 생성
    stocks['yahoo_symbol'] = stocks.apply(lambda row: 
        f"{row['ticker']}.KS" if row['market'] == 'KOSPI' else f"{row['ticker']}.KQ", 
        axis=1
    )
    
    print(f"✅ {len(stocks):,}개 종목 로드 완료")
    print(f"   - KOSPI: {len(stocks[stocks['market'] == 'KOSPI']):,}개 (.KS)")
    print(f"   - KOSDAQ: {len(stocks[stocks['market'] == 'KOSDAQ']):,}개 (.KQ)")
    
    return stocks

def search_stock(query, stocks):
    """종목 검색"""
    # 정확한 매칭 확인
    exact_match = stocks[stocks['name'] == query]
    if not exact_match.empty:
        return exact_match.iloc[0], "정확한 매칭"
    
    # 부분 매칭 (포함 관계)
    partial_matches = stocks[stocks['name'].str.contains(query, na=False)]
    if len(partial_matches) == 1:
        return partial_matches.iloc[0], "부분 매칭"
    elif len(partial_matches) > 1:
        return partial_matches.head(5), "여러 후보"
    
    # 유사한 종목명 검색
    all_names = stocks['name'].tolist()
    similar_names = get_close_matches(query, all_names, n=5, cutoff=0.4)
    
    if similar_names:
        similar_stocks = stocks[stocks['name'].isin(similar_names)]
        return similar_stocks, "유사한 종목"
    
    return None, "매칭 실패"

def display_result(result, match_type, query):
    """검색 결과 출력"""
    print(f"\n🔍 '{query}' 검색결과:")
    
    if match_type in ["정확한 매칭", "부분 매칭"]:
        print(f"✅ {match_type}:")
        print(f"   종목명: {result['name']}")
        print(f"   종목코드: {result['ticker']}")
        print(f"   야후심볼: {result['yahoo_symbol']}")
        print(f"   시장: {result['market']}")
        
    elif match_type in ["여러 후보", "유사한 종목"]:
        print(f"📝 {match_type}:")
        print(f"{'번호':<4} {'종목명':<20} {'종목코드':<8} {'야후심볼':<12} {'시장':<8}")
        print("-" * 60)
        
        for i, (_, row) in enumerate(result.iterrows(), 1):
            name = row['name'][:18] + '..' if len(row['name']) > 18 else row['name']
            print(f"{i:<4} {name:<20} {row['ticker']:<8} {row['yahoo_symbol']:<12} {row['market']:<8}")
            
    else:
        print("❌ 일치하는 종목을 찾을 수 없습니다.")

def get_stock_info(query, stocks):
    """단일 검색용 함수 - 딕셔너리 반환"""
    result, match_type = search_stock(query, stocks)
    
    if match_type in ["정확한 매칭", "부분 매칭"]:
        return {
            'name': result['name'],
            'ticker': result['ticker'],
            'yahoo_symbol': result['yahoo_symbol'],
            'market': result['market'],
            'status': match_type
        }
    elif match_type in ["여러 후보", "유사한 종목"]:
        return {
            'candidates': [
                {
                    'name': row['name'],
                    'ticker': row['ticker'], 
                    'yahoo_symbol': row['yahoo_symbol'],
                    'market': row['market']
                }
                for _, row in result.iterrows()
            ],
            'status': match_type
        }
    else:
        return {'status': '매칭 실패'}

def main():
    """메인 실행 함수"""
    try:
        # 데이터 로드
        stocks = load_stock_data()
        
        print("\n🎯 한국 주식 티커 검색 (야후 파이낸스 지원)")
        print("=" * 50)
        print("💡 야후 파이낸스 심볼 형태:")
        print("   - KOSPI: 종목코드.KS (예: 005930.KS)")
        print("   - KOSDAQ: 종목코드.KQ (예: 086520.KQ)")
        
        while True:
            query = input("\n🔍 종목명 입력 (종료: quit): ").strip()
            
            if query.lower() in ['quit', 'exit', '종료', 'q']:
                break
                
            if not query:
                continue
            
            # 검색 실행 및 결과 출력
            result, match_type = search_stock(query, stocks)
            display_result(result, match_type, query)
    
    except Exception as e:
        print(f"❌ 오류: {e}")

# 간단한 사용 예시 함수들
def get_yahoo_symbol(company_name):
    """종목명으로 야후 파이낸스 심볼 반환"""
    try:
        stocks = load_stock_data()
        info = get_stock_info(company_name, stocks)
        
        if info['status'] in ['정확한 매칭', '부분 매칭']:
            return info['yahoo_symbol']
        else:
            return None
    except:
        return None

def get_ticker_and_yahoo(company_name):
    """종목명으로 티커와 야후심볼 모두 반환"""
    try:
        stocks = load_stock_data()
        info = get_stock_info(company_name, stocks)
        
        if info['status'] in ['정확한 매칭', '부분 매칭']:
            return {
                'ticker': info['ticker'],
                'yahoo_symbol': info['yahoo_symbol'],
                'name': info['name'],
                'market': info['market']
            }
        else:
            return None
    except:
        return None

if __name__ == "__main__":
    main()

# 사용 예시:
# yahoo_symbol = get_yahoo_symbol("삼성전자")  # "005930.KS"
# info = get_ticker_and_yahoo("카카오")        # {'ticker': '035720', 'yahoo_symbol': '035720.KS', ...}