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
    
    # 01로 시작하는지 확인
    if not digits.startswith("01"):
        return None
    
    length = len(digits)
    
    # 10자리 또는 11자리 형식 처리
    if length == 10:
        # 3-3-4 형식
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif length == 11:
        # 3-4-4 형식
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    else:
        return None
