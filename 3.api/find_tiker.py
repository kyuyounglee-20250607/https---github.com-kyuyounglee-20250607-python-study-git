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
    kosdaq = fdr.StockListing('KOSDAQ')
    
    # 데이터 합치기 및 정리
    stocks = pd.concat([kospi, kosdaq], ignore_index=True)
    stocks = stocks[['Symbol', 'Name']].rename(columns={'Symbol': 'ticker', 'Name': 'name'})
    stocks['ticker'] = stocks['ticker'].astype(str).str.zfill(6)
    
    print(f"✅ {len(stocks):,}개 종목 로드 완료")
    return stocks

def search_stock(query, stocks):
    """종목 검색"""
    # 정확한 매칭 확인
    exact_match = stocks[stocks['name'] == query]
    if not exact_match.empty:
        return exact_match.iloc[0]['ticker'], "정확한 매칭"
    
    # 부분 매칭 (포함 관계)
    partial_matches = stocks[stocks['name'].str.contains(query, na=False)]
    if len(partial_matches) == 1:
        return partial_matches.iloc[0]['ticker'], "부분 매칭"
    elif len(partial_matches) > 1:
        return partial_matches.head(5), "여러 후보"
    
    # 유사한 종목명 검색
    all_names = stocks['name'].tolist()
    similar_names = get_close_matches(query, all_names, n=5, cutoff=0.4)
    
    if similar_names:
        similar_stocks = stocks[stocks['name'].isin(similar_names)]
        return similar_stocks, "유사한 종목"
    
    return None, "매칭 실패"

def main():
    """메인 실행 함수"""
    try:
        # 데이터 로드
        stocks = load_stock_data()
        
        print("\n🎯 한국 주식 티커 검색")
        print("=" * 40)
        
        while True:
            query = input("\n종목명 입력 (종료: quit): ").strip()
            
            if query.lower() in ['quit', 'exit', '종료']:
                break
                
            if not query:
                continue
            
            # 검색 실행
            result, match_type = search_stock(query, stocks)
            
            print(f"\n🔍 '{query}' 검색결과:")
            
            if match_type == "정확한 매칭":
                print(f"✅ {query} → {result}")
                
            elif match_type == "부분 매칭":
                print(f"📌 {query} → {result}")
                
            elif match_type in ["여러 후보", "유사한 종목"]:
                print(f"📝 {match_type}:")
                for _, row in result.iterrows():
                    print(f"   {row['name']} → {row['ticker']}")
                    
            else:
                print("❌ 일치하는 종목을 찾을 수 없습니다.")
    
    except Exception as e:
        print(f"❌ 오류: {e}")

if __name__ == "__main__":
    # main()

    kospi = fdr.StockListing('KOSPI')
    kosdaq = fdr.StockListing('KOSDAQ')
    
    # 데이터 합치기 및 정리
    stocks = pd.concat([kospi, kosdaq], ignore_index=True)
    stocks.to_csv('stocks.csv', index=False)