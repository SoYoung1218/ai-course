import unittest
from calculator import ParkingCalculator


class TestParkingCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = ParkingCalculator()

    def test_free_period(self):
        # 30분 딱 맞게 주차 (무료)
        record = self.calc.calculate_fee("09:00", "09:30")
        self.assertEqual(record["fee"], 0)

    def test_extra_fee_rounding(self):
        # 31분 주차 (500원)
        record = self.calc.calculate_fee("09:00", "09:31")
        self.assertEqual(record["fee"], 500)

        # 40분 주차 (500원)
        record = self.calc.calculate_fee("09:00", "09:40")
        self.assertEqual(record["fee"], 500)

        # 41분 주차 (1000원)
        record = self.calc.calculate_fee("09:00", "09:41")
        self.assertEqual(record["fee"], 1000)

    def test_long_duration_max_fee(self):
        # 매우 긴 주차 (최대 20,000원 제한)
        record = self.calc.calculate_fee("00:00", "23:59")
        self.assertEqual(record["fee"], 20000)

    def test_invalid_format(self):
        # 올바르지 않은 시간 형식
        with self.assertRaisesRegex(
            ValueError, "올바른 시간 형식"
        ):
            self.calc.calculate_fee("9:0", "10:00")

        with self.assertRaisesRegex(
            ValueError, "올바른 시간 형식"
        ):
            self.calc.calculate_fee("abc", "10:00")

    def test_out_of_range(self):
        # 시간 범위 초과
        with self.assertRaisesRegex(
            ValueError, "시간 범위를 확인"
        ):
            self.calc.calculate_fee("25:00", "26:00")

    def test_exit_before_entry(self):
        # 출차 시각이 입차 시각보다 빠른 경우
        with self.assertRaisesRegex(
            ValueError, "자정을 넘기는 주차는 지원하지 않습니다"
        ):
            self.calc.calculate_fee("10:00", "09:00")

    def test_empty_input(self):
        # 빈 입력
        with self.assertRaisesRegex(
            ValueError, "입력 값을 모두 채워주세요"
        ):
            self.calc.calculate_fee("", "10:00")

    def test_delete_and_total(self):
        # 주차 기록 추가
        self.calc.calculate_fee("09:00", "10:00")  # 1500원
        self.calc.calculate_fee("11:00", "11:30")  # 0원
        self.calc.calculate_fee("13:00", "14:00")  # 1500원

        # 총합계 확인
        self.assertEqual(self.calc.get_total_sum(), 3000)

        # 첫 번째 기록 삭제
        self.calc.remove_entry(0)

        # 삭제 후 총합계 확인
        self.assertEqual(self.calc.get_total_sum(), 1500)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(
        TestParkingCalculator
    )

    result = unittest.TextTestRunner(
        verbosity=0
    ).run(suite)

    print("\n" + "=" * 30)
    print("테스트 완료!")
    print(
        f"통과: {result.testsRun - len(result.failures) - len(result.errors)} / {result.testsRun}"
    )
    print(f"실패: {len(result.failures)}")
    print(f"에러: {len(result.errors)}")
    print("=" * 30)

    if not result.wasSuccessful():
        exit(1)
