import re

def normalize_phone(s):
    if not isinstance(s, str):
        return None
    
    # +82 처리 및 특수문자 제거
    s = s.strip()
    if s.startswith("+82"):
        s = "0" + s[3:]
    
    # 숫자만 추출
    digits = re.sub(r'[^0-9]', '', s)
    
    # 01로 시작하는 10자리 또는 11자리 확인
    if not (len(digits) in [10, 11] and digits.startswith("01")):
        return None
    
    # 자릿수에 따른 하이픈 포맷팅
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11:
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    
    return None
