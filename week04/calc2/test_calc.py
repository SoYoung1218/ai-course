from calc import Calculator

def run_test():
    tests = [
        ([], "0"),
        (["1", "2", "+", "3", "="], "15"),
        (["2", "+", "3", "*", "4", "="], "20"),
        (["5", "+", "-", "3", "="], "2"),
        (["0", ".", "1", "+", "0", ".", "2", "="], "0.3"),
        (["6", "/", "3", "="], "2"),
        (["7", "/", "2", "="], "3.5"),
        (["5", "/", "0", "="], "0으로 나눌 수 없습니다"),
        (["5", "/", "0", "=", "7"], "0으로 나눌 수 없습니다"),
        (["5", "/", "0", "=", "C"], "0"),
        (["1", ".", ".", "5"], "1.5"),
        (["."], "0."),
        (["0", "0", "7"], "7"),
        (["1", "2", "3", "BS"], "12"),
        (["5", "BS"], "0"),
        (["9", "+/-"], "-9"),
        (["5", "0", "%"], "0.5"),
        (["2", "+", "3", "=", "4"], "4"),
        (["2", "+", "3", "=", "+", "4", "="], "9"),
        (["2", "+", "3", "=", "="], "5"),
    ]

    passed = 0
    for i, (inputs, expected) in enumerate(tests):
        calc = Calculator()
        actual = "0"
        for key in inputs:
            actual = calc.press(key)
        
        if actual == expected:
            passed += 1
        else:
            print(f"Test {i+1} Failed!")
            print(f"  Inputs: {' '.join(inputs)}")
            print(f"  Expected: {expected}")
            print(f"  Actual: {actual}")
            return

    print(f"모든 테스트 통과 ({passed}개)")

if __name__ == "__main__":
    run_test()
