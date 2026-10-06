def format_phone_number(number):
    # 숫자 이외의 문자 제거
    number = ''.join(filter(str.isdigit, number))
    length = len(number)
    
    # 1. 010으로 시작하는 경우
    if number.startswith('010'):
        if length == 11:
            return f"{number[:3]}-{number[3:7]}-{number[7:]}"
        else:
            return "잘못된 010 번호 형식입니다."

    # 2. 011, 016, 017, 018, 019로 시작하는 경우
    elif number.startswith(('011', '016', '017', '018', '019')):
        if length == 10:
            return f"{number[:3]}-{number[3:6]}-{number[6:]}"
        elif length == 11:
            return f"{number[:3]}-{number[3:7]}-{number[7:]}"
        else:
            return "잘못된 번호 자릿수입니다."
            
    else:
        return "지원하지 않는 번호 체계입니다."

# --- 테스트 ---
print(format_phone_number("01012345678"))    # 결과: 010-1234-5678 (11자리)
print(format_phone_number("0111234567"))     # 결과: 011-123-4567 (10자리)
print(format_phone_number("01612345678"))    # 결과: 016-1234-5678 (11자리)
print(format_phone_number("0101234567"))     # 결과: 잘못된 010 번호 형식입니다.
