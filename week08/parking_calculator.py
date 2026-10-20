
from datetime import datetime
import math
import re

class ParkingCalculator:
    def __init__(self):
        self.records = []

    def calculate_fee(self, entry_str, exit_str):
        # 1. 빈 입력 검사
        if not entry_str or not exit_str:
            raise ValueError("입력 값을 모두 채워주세요.")

        # 2. 시간 형식 검사 (HH:mm)
        for time_str in [entry_str, exit_str]:
            if not re.fullmatch(r"\d{2}:\d{2}", time_str):
                raise ValueError("올바른 시간 형식(HH:mm)을 입력하세요.")

        # 3. 시간 범위 검사
        for time_str in [entry_str, exit_str]:
            hour, minute = map(int, time_str.split(":"))

            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("시간 범위를 확인하세요.")

        # 4. 시간 변환
        entry_time = datetime.strptime(entry_str, "%H:%M")
        exit_time = datetime.strptime(exit_str, "%H:%M")

        # 5. 출차 시각 검사
        if exit_time <= entry_time:
            raise ValueError("출차 시각은 입차 시각보다 뒤여야 합니다.")

        # 6. 주차 시간 계산
        duration = exit_time - entry_time
        total_minutes = duration.total_seconds() / 60

        # 7. 요금 계산
        # 30분 무료, 이후 10분당 500원
        free_minutes = 30

        if total_minutes <= free_minutes:
            fee = 0
        else:
            extra_minutes = total_minutes - free_minutes
            intervals = math.ceil(extra_minutes / 10)
            fee = intervals * 500

        # 8. 일일 최대 요금 20,000원
        if fee > 20000:
            fee = 20000

        # 9. 주차 시간 표시
        hours = int(total_minutes // 60)
        minutes = int(total_minutes % 60)

        if hours > 0:
            duration_str = f"{hours}시간 {minutes}분"
        else:
            duration_str = f"{minutes}분"

        # 10. 결과 저장
        record = {
            "entry": entry_str,
            "exit": exit_str,
            "duration": duration_str,
            "fee": fee
        }

        self.records.append(record)
        return record

    def delete_record(self, index):
        if 0 <= index < len(self.records):
            del self.records[index]

    def get_total_fee(self):
        return sum(record["fee"] for record in self.records)

    def get_records(self):
        return self.records