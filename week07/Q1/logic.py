from typing import Union, Tuple

def convert_units(value: float, from_unit: str, to_unit: str) -> Tuple[bool, Union[float, str]]:
    """
    단위 변환을 수행하는 메인 함수.
    
    Args:
        value: 변환할 수치
        from_unit: 현재 단위
        to_unit: 목표 단위
        
    Returns:
        Tuple[bool, Union[float, str]]: (성공 여부, 변환된 값 또는 에러 메시지)
    """
    length_units = {"mm", "cm", "m", "km"}
    temp_units = {"°C", "°F"}

    # 1. 범주 혼합 체크
    from_is_length = from_unit in length_units
    from_is_temp = from_unit in temp_units
    to_is_length = to_unit in length_units
    to_is_temp = to_unit in temp_units

    if (from_is_length and to_is_temp) or (from_is_temp and to_is_length):
        return False, "길이와 온도는 함께 변환할 수 없습니다."

    # 2. 길이 변환 수행
    if from_is_length and to_is_length:
        return True, convert_length(value, from_unit, to_unit)

    # 3. 온도 변환 수행
    if from_is_temp and to_is_temp:
        return True, convert_temperature(value, from_unit, to_unit)

    return False, "지원하지 않는 단위입니다."

def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """길이 단위 간 변환 (기준: m)"""
    # mm, cm, m, km -> m (Base unit: m)
    to_meters = {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0
    }
    
    # 입력값을 m로 변환
    meters = value * to_meters[from_unit]
    # m를 목표 단위로 변환
    result = meters / to_meters[to_unit]
    return round(result, 4)

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """온도 단위 간 변환 (기준: °C)"""
    # °C -> °F 공식: (Celsius * 9/5) + 32
    # °F -> °C 공식: (Fahrenheit - 32) * 5/9
    
    if from_unit == to_unit:
        return value
    
    if from_unit == "°C" and to_unit == "°F":
        return round((value * 9/5) + 32, 2)
    
    if from_unit == "°F" and to_unit == "°C":
        return round((value - 32) * 5/9, 2)
    
    return value
