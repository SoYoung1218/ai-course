import logic

def test_unit_converter():
    # 테스트 케이스 정의: (입력값, 현재단위, 대상단위, 기대값)
    # 기대값은 정확한 일치를 위해 문자열로 처리하거나, 
    # 숫자일 경우 float 비교를 위해 약간의 오차를 허용할 수 있지만 여기선 정밀도에 맞춰 작성합니다.
    test_cases = [
        # 길이 변환 테스트
        (1000, "mm", "m", 1.0),
        (1, "m", "cm", 100.0),
        (5, "km", "m", 5000.0),
        (10, "cm", "mm", 100.0),
        
        # 온도 변환 테스트
        (0, "°C", "°F", 32.0),
        (100, "°C", "°F", 212.0),
        (32, "°F", "°C", 0.0),
        (-40, "°C", "°F", -40.0),
        
        # 범주 혼합 에러 테스트 (성공 여부가 False여야 함)
        (10, "cm", "°C", "길이와 온도는 함께 변환할 수 없습니다."),
        (25, "°F", "m", "길이와 온도는 함께 변환할 수 없습니다."),
    ]

    passed_count = 0
    failed_cases = []

    for i, (val, from_u, to_u, expected) in enumerate(test_cases):
        # logic.convert_units는 (success, result)를 반환함
        # 혼합 에러의 경우 success=False, result="메시지"
        # 정상의 경우 success=True, result=숫자
        
        if isinstance(expected, str):
            # 에러 메시지를 기대하는 경우
            success, actual = logic.convert_units(val, from_u, to_u)
            if not success and actual == expected:
                passed_count += 1
            else:
                failed_cases.append((f"{val} {from_u} -> {to_u}", expected, actual))
        else:
            # 숫자를 기대하는 경우
            success, actual = logic.convert_units(val, from_u, to_u)
            if success and abs(actual - expected) < 1e-7:
                passed_count += 1
            else:
                actual_str = actual if success else "Error"
                failed_cases.append((f"{val} {from_u} -> {to_u}", expected, actual_str))

    # 결과 출력
    total_tests = len(test_cases)
    if failed_cases:
        for fail in failed_cases:
            print(f"[실패] 입력: {fail[0]} | 기대값: {fail[1]} | 실제값: {fail[2]}")
        print(f"\n테스트 실패: {total_tests - passed_count}/{total_tests}")
    else:
        print(f"모든 테스트 통과 ({passed_count}개)")

if __name__ == "__main__":
    test_unit_converter()
