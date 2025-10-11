"""
서울시 상권분석 데이터 수집 스크립트 (개선 버전)

개선사항:
- 에러 처리 강화
- 로깅 시스템 추가
- 함수화 및 재사용성 향상
- 타입 힌트 추가
- 설정 상수 분리
"""

import requests
import dotenv
import os
import json
import pandas as pd
from datetime import datetime
import logging
from typing import Optional, Dict, List

# =============================================================================
# 설정
# =============================================================================

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('seoul_api.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 컬럼명 매핑
COLUMN_MAPPING = {
    "STDR_YYQU_CD": "기준_년분기_코드",
    "MEGA_CD": "서울시_코드",
    "MEGA_CD_NM": "서울시_코드_명",
    "SVC_INDUTY_CD": "서비스_업종_코드",
    "SVC_INDUTY_CD_NM": "서비스_업종_코드_명",
    "THSMON_SELNG_AMT": "당월_매출_금액",
    "THSMON_SELNG_CO": "당월_매출_건수",
    "MDWK_SELNG_AMT": "주중_매출_금액",
    "WKEND_SELNG_AMT": "주말_매출_금액",
    "MON_SELNG_AMT": "월요일_매출_금액",
    "TUES_SELNG_AMT": "화요일_매출_금액",
    "WED_SELNG_AMT": "수요일_매출_금액",
    "THUR_SELNG_AMT": "목요일_매출_금액",
    "FRI_SELNG_AMT": "금요일_매출_금액",
    "SAT_SELNG_AMT": "토요일_매출_금액",
    "SUN_SELNG_AMT": "일요일_매출_금액",
    "TMZON_00_06_SELNG_AMT": "시간대_00~06_매출_금액",
    "TMZON_06_11_SELNG_AMT": "시간대_06~11_매출_금액",
    "TMZON_11_14_SELNG_AMT": "시간대_11~14_매출_금액",
    "TMZON_14_17_SELNG_AMT": "시간대_14~17_매출_금액",
    "TMZON_17_21_SELNG_AMT": "시간대_17~21_매출_금액",
    "TMZON_21_24_SELNG_AMT": "시간대_21~24_매출_금액",
    "ML_SELNG_AMT": "남성_매출_금액",
    "FML_SELNG_AMT": "여성_매출_금액",
    "AGRDE_10_SELNG_AMT": "연령대_10_매출_금액",
    "AGRDE_20_SELNG_AMT": "연령대_20_매출_금액",
    "AGRDE_30_SELNG_AMT": "연령대_30_매출_금액",
    "AGRDE_40_SELNG_AMT": "연령대_40_매출_금액",
    "AGRDE_50_SELNG_AMT": "연령대_50_매출_금액",
    "AGRDE_60_ABOVE_SELNG_AMT": "연령대_60_이상_매출_금액",
    "MDWK_SELNG_CO": "주중_매출_건수",
    "WKEND_SELNG_CO": "주말_매출_건수",
    "MON_SELNG_CO": "월요일_매출_건수",
    "TUES_SELNG_CO": "화요일_매출_건수",
    "WED_SELNG_CO": "수요일_매출_건수",
    "THUR_SELNG_CO": "목요일_매출_건수",
    "FRI_SELNG_CO": "금요일_매출_건수",
    "SAT_SELNG_CO": "토요일_매출_건수",
    "SUN_SELNG_CO": "일요일_매출_건수",
    "TMZON_00_06_SELNG_CO": "시간대_00~06_매출_건수",
    "TMZON_06_11_SELNG_CO": "시간대_06~11_매출_건수",
    "TMZON_11_14_SELNG_CO": "시간대_11~14_매출_건수",
    "TMZON_14_17_SELNG_CO": "시간대_14~17_매출_건수",
    "TMZON_17_21_SELNG_CO": "시간대_17~21_매출_건수",
    "TMZON_21_24_SELNG_CO": "시간대_21~24_매출_건수",
    "ML_SELNG_CO": "남성_매출_건수",
    "FML_SELNG_CO": "여성_매출_건수",
    "AGRDE_10_SELNG_CO": "연령대_10_매출_건수",
    "AGRDE_20_SELNG_CO": "연령대_20_매출_건수",
    "AGRDE_30_SELNG_CO": "연령대_30_매출_건수",
    "AGRDE_40_SELNG_CO": "연령대_40_매출_건수",
    "AGRDE_50_SELNG_CO": "연령대_50_매출_건수",
    "AGRDE_60_ABOVE_SELNG_CO": "연령대_60_이상_매출_건수"
}

COLUMNS_TO_DROP = ['서울시_코드', '서울시_코드_명']

# =============================================================================
# 함수 정의
# =============================================================================

def load_api_key() -> str:
    """환경변수에서 API 키 로드"""
    dotenv.load_dotenv()
    key = os.getenv("SEOUL_API")
    
    if not key:
        logger.error("API 키를 찾을 수 없습니다. .env 파일을 확인하세요.")
        raise ValueError("SEOUL_API 키가 설정되지 않았습니다.")
    
    logger.info("API 키 로드 완료")
    return key


def fetch_seoul_data(
    api_key: str, 
    start_idx: int = 1, 
    end_idx: int = 1000, 
    max_retries: int = 3
) -> Optional[Dict]:
    """
    서울시 상권분석 데이터 API 호출
    
    Args:
        api_key: API 인증키
        start_idx: 시작 인덱스
        end_idx: 종료 인덱스
        max_retries: 최대 재시도 횟수
    
    Returns:
        API 응답 데이터 (실패 시 None)
    """
    url = f'http://openapi.seoul.go.kr:8088/{api_key}/json/VwsmMegaSelngW/{start_idx}/{end_idx}/'
    
    for attempt in range(max_retries):
        try:
            logger.info(f"API 호출 시도 {attempt + 1}/{max_retries}")
            response = requests.get(url, timeout=30)
            
            logger.info(f'접속주소: {response.url}')
            logger.info(f'응답코드: {response.status_code}')
            
            if response.status_code == 200:
                result = response.json()
                
                # API 오류 체크
                if 'RESULT' in result and result['RESULT']['CODE'] != 'INFO-000':
                    logger.error(f"API 오류: {result['RESULT']['MESSAGE']}")
                    return None
                
                logger.info("API 호출 성공")
                return result
            else:
                logger.warning(f"HTTP 오류: {response.status_code}")
                
        except requests.Timeout:
            logger.warning(f"타임아웃 발생 (시도 {attempt + 1}/{max_retries})")
        except requests.RequestException as e:
            logger.error(f"요청 오류: {e}")
        except json.JSONDecodeError:
            logger.error("JSON 파싱 오류")
    
    logger.error("API 호출 실패")
    return None


def process_dataframe(data: List[Dict]) -> pd.DataFrame:
    """
    원본 데이터를 DataFrame으로 변환 및 전처리
    
    Args:
        data: API에서 받은 원본 데이터 리스트
    
    Returns:
        전처리된 DataFrame
    """
    if not data:
        logger.warning("처리할 데이터가 없습니다.")
        return pd.DataFrame()
    
    # DataFrame 생성
    df = pd.DataFrame(data)
    logger.info(f"DataFrame 생성: {len(df)} 행")
    
    # 컬럼명 변경
    df.rename(columns=COLUMN_MAPPING, inplace=True)
    
    # 인덱스 설정
    if '기준_년분기_코드' in df.columns:
        df.set_index('기준_년분기_코드', inplace=True)
    
    # 불필요한 컬럼 제거
    df.drop(columns=COLUMNS_TO_DROP, inplace=True, errors='ignore')
    
    # 데이터 타입 변환
    numeric_columns = [col for col in df.columns if '매출' in col or '건수' in col]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    logger.info("데이터 처리 완료")
    return df


def save_dataframe(df: pd.DataFrame, base_filename: str = 'seoul_store') -> None:
    """
    DataFrame을 CSV와 Excel 파일로 저장
    
    Args:
        df: 저장할 DataFrame
        base_filename: 기본 파일명
    """
    if df.empty:
        logger.warning("저장할 데이터가 없습니다.")
        return
    
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # CSV 저장 (타임스탬프 포함)
        csv_filename = f'{base_filename}_{timestamp}.csv'
        df.to_csv(csv_filename, encoding='cp949')
        logger.info(f"CSV 파일 저장 완료: {csv_filename}")
        
        # CSV 저장 (원본 파일명, 호환성 유지)
        df.to_csv(f'{base_filename}.csv', encoding='cp949')
        logger.info(f"CSV 파일 저장 완료: {base_filename}.csv")
        
        # Excel 저장
        excel_filename = 'output.xlsx'
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Sheet1')
        logger.info(f"Excel 파일 저장 완료: {excel_filename}")
        
    except Exception as e:
        logger.error(f"파일 저장 오류: {e}")


# =============================================================================
# 메인 실행
# =============================================================================

def main():
    """메인 실행 함수"""
    try:
        # API 키 로드
        api_key = load_api_key()
        
        # 데이터 가져오기
        result = fetch_seoul_data(api_key)
        
        if not result or 'VwsmMegaSelngW' not in result:
            logger.error("데이터를 가져올 수 없습니다.")
            return
        
        data = result['VwsmMegaSelngW']['row']
        logger.info(f'데이터 개수: {len(data)}')
        
        # 첫 번째 레코드 출력
        print("\n=== 첫 번째 데이터 샘플 ===")
        print(json.dumps(data[0], indent=4, ensure_ascii=False))
        
        # 데이터 처리
        df = process_dataframe(data)
        
        # 데이터 정보 출력
        print("\n=== 데이터 정보 ===")
        print(df.info())
        print("\n=== 처음 5개 행 ===")
        print(df.head())
        
        # 데이터 저장
        save_dataframe(df)
        
        logger.info("프로그램 실행 완료")
        
    except Exception as e:
        logger.error(f"프로그램 실행 중 오류 발생: {e}")
        raise


if __name__ == "__main__":
    main()
