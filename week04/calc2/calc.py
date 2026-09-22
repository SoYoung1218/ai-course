class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.display = "0"
        self.current_input = "0"
        self.operator = None
        self.prev_value = 0.0
        self.is_result = False
        self.error = False

    def _format(self, val):
        if val == "ERROR":
            return "ERROR"
        # 소수 10자리 반올림
        s = "{:.10f}".format(val).rstrip('0').rstrip('.')
        if s == "" or s == "-0":
            s = "0"
        return s

    def press(self, key: str) -> str:
        if self.error:
            if key == "C":
                self.reset()
            return self.display

        if key == "C":
            self.reset()
            return self.display

        if key == "BS":
            if self.is_result:
                return self.display
            if len(self.current_input) > 1:
                self.current_input = self.current_input[:-1]
                if self.current_input == "-":
                    self.current_input = "0"
            else:
                self.current_input = "0"
            self.display = self.current_input
            return self.display

        if key in "0123456789.":
            if self.is_result:
                self.current_input = ""
                self.prev_value = 0.0
                self.operator = None
                self.is_result = False

            if key == ".":
                if "." in self.current_input:
                    return self.display
                if self.current_input == "0":
                    self.current_input = "0."
                else:
                    self.current_input += "."
            else:
                # 12자리 제한 (소수점, 부호 제외)
                clean = self.current_input.replace("-", "").replace(".", "")
                if len(clean) < 12:
                    if self.current_input == "0":
                        self.current_input = key
                    else:
                        self.current_input += key
            
            # 앞의 0 제거 (0.은 제외)
            if len(self.current_input) > 1 and self.current_input.startswith("0") and self.current_input[1] != ".":
                self.current_input = self.current_input.lstrip("0")
                if not self.current_input or self.current_input.startswith("."):
                    self.current_input = "0" + self.current_input
            
            # -0 처리
            if self.current_input == "-0":
                self.current_input = "0"
                
            self.display = self.current_input
            return self.display

        if key in "+-*/":
            if self.is_result:
                self.current_input = self._format(float(self.display))
                self.is_result = False

            val = float(self.current_input)
            
            if self.operator is None:
                self.prev_value = val
            else:
                # 연산자 우선순위 없이 즉시 계산
                res = self._calc_op(self.prev_value, self.operator, val)
                if res == "ERROR":
                    self.error = True
                    self.display = "0으로 나눌 수 없습니다"
                    return self.display
                self.prev_value = res

            self.operator = key
            self.current_input = "0"
            self.display = "0"
            return self.display

        if key == "=":
            if self.operator is None or self.is_result:
                return self.display
            
            val = float(self.current_input)
            res = self._calc_op(self.prev_value, self.operator, val)
            
            if res == "ERROR":
                self.error = True
                self.display = "0으로 나눌 수 없습니다"
            else:
                self.display = self._format(res)
                self.prev_value = res
                self.current_input = self.display
                self.is_result = True
                self.operator = None
            return self.display

        if key == "+/-":
            if self.is_result:
                return self.display
            if self.current_input != "0":
                if self.current_input.startswith("-"):
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = "-" + self.current_input
                # 부호 뒤 0 처리
                if len(self.current_input) > 2 and self.current_input[1] == "0" and self.current_input[2] != ".":
                    self.current_input = "-" + self.current_input[2:].lstrip("0")
                    if self.current_input == "-": self.current_input = "0"
                    elif self.current_input.startswith("-."): self.current_input = "0" + self.current_input
                if self.current_input == "-0": self.current_input = "0"
                self.display = self.current_input
            return self.display

        if key == "%":
            if self.is_result:
                return self.display
            val = float(self.current_input) / 100.0
            self.current_input = self._format(val)
            self.display = self.current_input
            return self.display

        return self.display

    def _calc_op(self, v1, op, v2):
        try:
            if op == "+": return v1 + v2
            if op == "-": return v1 - v2
            if op == "*": return v1 * v2
            if op == "/":
                if v2 == 0: return "ERROR"
                return v1 / v2
        except ZeroDivisionError:
            return "ERROR"
        return v2
