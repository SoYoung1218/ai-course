import unittest
from calculator import ParkingCalculator

class TestParkingCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = ParkingCalculator()

    def test_free_period(self):
        # 1. 09:00 ~ 09:30 (30분) -> 0원
        res = self.calc.calculate_fee("09:00", "09:30")
        self.assertEqual(res['fee'], 0)

    def test_extra_minutes_rounding(self):
        # 2. 09:00 ~ 09:31 (31분) -> 500원
        res = self.calc.calculate_fee("09:00", "09:31")
        self.assertEqual(res['fee'], 500)

    def test_sixty_minutes(self):
        # 3. 09:00 ~ 10:00 (60분) -> 1,500원
        res = self.calc.calculate_fee("09:00", "10:00")
        self.assertEqual(res['fee'], 1500)

    def test_max_daily_fee(self):
        # 4. 00:00 ~ 23:59 (23시간 59분) -> 20,000원
        res = self.calc.calculate_fee("00:00", "23:59")
        self.assertEqual(res['fee'], 20000)

    def test_invalid_order(self):
        # 5. 10:00 ~ 09:00 -> 에러 (자정 통과 불가)
        with self.assertRaisesRegex(ValueError, "자정을 넘기는 주차는 지원하지 않습니다."):
            self.calc.calculate_fee("10:00", "09:00")

    def test_invalid_format(self):
        # 6. 25:00 -> 에러 (잘못된 시간 형식/범위)
        with self.assertRaisesRegex(ValueError, "시간 범위를 확인하세요"):
            self.calc.calculate_fee("25:00", "26:00")

    def test_empty_input(self):
        # 7. 빈 입력
        with self.assertRaisesRegex(ValueError, "입력 값을 모두 채워주세요."):
            self.calc.calculate_fee("", "09:00")

    def test_removal_and_sum(self):
        # 삭제 및 합계 재계산 테스트
        self.calc.calculate_fee("09:00", "09:30") # 0원
        self.calc.calculate_fee("09:00", "10:00") # 1500원
        self.assertEqual(self.calc.get_total_sum(), 1500)
        
        self.calc.remove_entry(0)
        self.assertEqual(self.calc.get_total_sum(), 1500)
        
        self.calc.remove_entry(0)
        self.assertEqual(self.calc.get_total_sum(), 0)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParkingCalculator)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    print("\n" + "="*30)
    print(f"테스트 결과: 성공 {result.testsRun - len(result.failures) - len(result.errors)} / 실패 {len(result.failures) + len(result.errors)}")
    print("="*30)
    
    if not result.errors and not result.failures:
        exit(0)
    else:
        exit(1)
