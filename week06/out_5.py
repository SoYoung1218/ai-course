import re

def normalize_phone(s):
    if not isinstance(s, str):
        return None
    
    # +82 처리 및 특수문자 제거
    temp = s.strip()
    if temp.startswith("+82"):
        temp = "0" + temp[3:]
    
    # 숫자만 추출
    digits = "".join(re.findall(r'\d', temp))
    
    # 01로 시작하는지 확인 및 길이 체크 (10자리 또는 11자리)
    if not digits.startswith("01") or len(digits) not in [10, 11]:
        return None
    
    # 자릿수에 따른 하이픈 삽입
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    else:  # len == 11
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
