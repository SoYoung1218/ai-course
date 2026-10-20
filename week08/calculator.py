import datetime
import math

class ParkingCalculator:
    def __init__(self):
        self.history = []  # List of dicts: {'in': str, 'out': str, 'duration': str, 'fee': int}
        self.MAX_DAILY_FEE = 20000
        self.FREE_MINUTES = 30
        self.RATE_PER_10_MIN = 500

    def _parse_time(self, time_str):
        """Parses HH:mm string to datetime.time object."""
        if not time_str:
            raise ValueError("입력 값을 모두 채워주세요.")
        
        try:
            return datetime.datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            # Check if it's just a format error or range error
            if ":" not in time_str:
                raise ValueError("올바른 시간 형식(HH:mm)을 입력하세요.")
            
            parts = time_str.split(":")
            if len(parts) != 2:
                raise ValueError("올바른 시간 형식(HH:mm)을 입력하세요.")
            
            try:
                h, m = int(parts[0]), int(parts[1])
                if not (0 <= h < 24 and 0 <= m < 60):
                    raise ValueError("시간 범위를 확인하세요 (00:00 ~ 23:59).")
                return datetime.time(h, m)
            except ValueError as e:
                if "time" in str(e) or "range" in str(e):
                    raise ValueError("시간 범위를 확인하세요 (00:00 ~ 23:59).")
                raise ValueError("올바른 시간 형식(HH:mm)을 입력하세요.")

    def calculate_fee(self, in_time_str, out_time_str):
        """Calculates fee and adds to history."""
        in_time = self._parse_time(in_time_str)
        out_time = self._parse_time(out_time_str)

        # Create dummy datetimes for comparison and duration calculation
        # Using a fixed date to allow time delta calculation
        base_date = datetime.date(2026, 1, 1)
        dt_in = datetime.datetime.combine(base_date, in_time)
        dt_out = datetime.datetime.combine(base_date, out_time)

        if dt_out <= dt_in:
            raise ValueError("자정을 넘기는 주차는 지원하지 않습니다.")

        duration = dt_out - dt_in
        total_minutes = duration.total_seconds() / 60

        # Fee calculation
        if total_minutes <= self.FREE_MINUTES:
            fee = 0
        else:
            extra_minutes = total_minutes - self.FREE_MINUTES
            # 10 min increments, rounding up
            units = math.ceil(extra_minutes / 10)
            fee = units * self.RATE_PER_10_MIN

        # Cap at max daily fee
        fee = min(fee, self.MAX_DAILY_FEE)

        # Format duration string
        hours, remainder = divmod(int(total_minutes), 60)
        minutes = remainder
        duration_str = f"{hours}시간 {minutes}분" if hours > 0 else f"{minutes}분"

        # Add to history
        entry = {
            'in': in_time_str,
            'out': out_time_str,
            'duration': duration_str,
            'fee': fee
        }
        self.history.append(entry)
        return entry

    def remove_entry(self, index):
        """Removes an entry from history by index."""
        if 0 <= index < len(self.history):
            self.history.pop(index)
        else:
            raise IndexError("잘못된 목록 인덱스입니다.")

    def get_total_sum(self):
        """Returns the sum of all fees in history."""
        return sum(item['fee'] for item in self.history)

    def get_history(self):
        """Returns the entire history."""
        return self.history
