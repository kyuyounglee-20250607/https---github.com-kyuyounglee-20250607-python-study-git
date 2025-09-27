import xml.etree.ElementTree as ET

def get_data_dart():
    # XML 파일 읽기
    tree = ET.parse("D:\week_src\CORPCODE.xml")   # 파일명은 실제 xml 파일 이름으로 변경
    root = tree.getroot()

    # 원하는 값 추출
    result = []
    for item in root.findall("list"):
        corp_code = item.find("corp_code").text.strip()   # 공백 제거
        corp_name = item.find("corp_name").text.strip()
        
        result.append( (corp_code,corp_name) )

    return result

if __name__ == "__main__":
    result = get_data_dart()
    print(result)