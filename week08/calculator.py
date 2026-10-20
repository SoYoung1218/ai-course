
import datetime
import math
import re


class ParkingCalculator:
    def __init__(self):
        self.history = []
        self.MAX_DAILY_FEE = 20000
        self.FREE_MINUTES = 30
        self.RATE_PER_10_MIN = 500

    def _parse_time(self, time_str):
        """HH:mm 시간 형식 및 유효성 검사"""

        # 1. 빈 입력 검사
        if not time_str or time_str.strip() == "":
            raise ValueError("입력 값을 모두 채워주세요.")

        # 2. 시간 형식 검사
        if not re.fullmatch(r"[0-9]{2}:[0-9]{2}", time_str):
            raise ValueError(
                "올바른 시간 형식(HH:mm)을 입력하세요."
            )

        # 3. 시간 범위 검사
        h, m = map(int, time_str.split(":"))

        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError(
                "시간 범위를 확인하세요 (00:00 ~ 23:59)."
            )

        return datetime.time(h, m)

    def calculate_fee(self, in_time_str, out_time_str):
        """주차요금 계산 및 기록 저장"""

        # 1. 입차 및 출차 시각 검사
        in_time = self._parse_time(in_time_str)
        out_time = self._parse_time(out_time_str)

        # 2. 시간 계산
        base_date = datetime.date(2026, 1, 1)

        dt_in = datetime.datetime.combine(
            base_date, in_time
        )
        dt_out = datetime.datetime.combine(
            base_date, out_time
        )

        # 3. 자정 통과 및 시간 순서 검사
        if dt_out <= dt_in:
            raise ValueError(
                "자정을 넘기는 주차는 지원하지 않습니다."
            )

        # 4. 총 주차 시간 계산
        duration = dt_out - dt_in
        total_minutes = int(
            duration.total_seconds() / 60
        )

        # 5. 요금 계산
        # 30분까지 무료
        if total_minutes <= self.FREE_MINUTES:
            fee = 0
        else:
            # 30분 초과 시 10분마다 500원
            extra_minutes = (
                total_minutes - self.FREE_MINUTES
            )

            # 10분 미만도 10분으로 올림
            units = math.ceil(extra_minutes / 10)
            fee = units * self.RATE_PER_10_MIN

        # 6. 하루 최대 요금 20,000원
        fee = min(fee, self.MAX_DAILY_FEE)

        # 7. 주차 시간 표시
        hours, minutes = divmod(total_minutes, 60)

        if hours > 0:
            duration_str = f"{hours}시간 {minutes}분"
        else:
            duration_str = f"{minutes}분"

        # 8. 계산 기록 저장
        entry = {
            "in": in_time_str,
            "out": out_time_str,
            "duration": duration_str,
            "fee": fee
        }

        self.history.append(entry)

        return entry

    def remove_entry(self, index):
        """선택한 주차 기록 삭제"""

        if 0 <= index < len(self.history):
            self.history.pop(index)
        else:
            raise IndexError(
                "잘못된 목록 인덱스입니다."
            )

    def get_total_sum(self):
        """오늘의 총 주차요금 계산"""

        return sum(
            item["fee"] for item in self.history
        )

    def get_history(self):
        """전체 주차 기록 반환"""

        return self.history
