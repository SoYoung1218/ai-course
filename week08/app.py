
import tkinter as tk
from tkinter import ttk, messagebox
from calculator import ParkingCalculator


class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("주차 요금 계산기")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)

        self.calculator = ParkingCalculator()
        self._setup_ui()

    def _setup_ui(self):
        # 1. 시간 입력 영역
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.pack(fill="x")

        # 입차 시각
        tk.Label(
            input_frame,
            text="입차 시각 (HH:mm):"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.ent_in = tk.Entry(input_frame, width=12)
        self.ent_in.grid(row=0, column=1, padx=5, pady=5)

        # 출차 시각
        tk.Label(
            input_frame,
            text="출차 시각 (HH:mm):"
        ).grid(row=0, column=2, padx=5, pady=5)

        self.ent_out = tk.Entry(input_frame, width=12)
        self.ent_out.grid(row=0, column=3, padx=5, pady=5)

        # 2. 계산 버튼 (입력창 아래 중앙)
        button_frame = tk.Frame(self.root, pady=5)
        button_frame.pack(fill="x")

        btn_calc = tk.Button(
            button_frame,
            text="계산하기",
            command=self._on_calculate,
            width=18,
            height=1
        )
        btn_calc.pack()

        # 3. 계산 기록 목록
        table_frame = tk.Frame(self.root, padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)

        columns = ("in", "out", "duration", "fee")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading("in", text="입차")
        self.tree.heading("out", text="출차")
        self.tree.heading("duration", text="주차 시간")
        self.tree.heading("fee", text="요금")

        self.tree.column("in", width=80, anchor="center")
        self.tree.column("out", width=80, anchor="center")
        self.tree.column("duration", width=100, anchor="center")
        self.tree.column("fee", width=100, anchor="e")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # 4. 삭제 버튼 및 총합계
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(fill="x")

        btn_delete = tk.Button(
            control_frame,
            text="선택 항목 삭제",
            command=self._on_delete
        )
        btn_delete.pack(side="left", padx=5)

        self.lbl_total = tk.Label(
            control_frame,
            text="오늘의 총 합계: 0원",
            font=("Helvetica", 12, "bold")
        )
        self.lbl_total.pack(side="right", padx=5)

    def _format_currency(self, amount):
        return f"{amount:,}원"

    def _update_display(self):
        # 기존 목록 초기화
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 계산 기록 표시
        for entry in self.calculator.get_history():
            self.tree.insert(
                "",
                "end",
                values=(
                    entry["in"],
                    entry["out"],
                    entry["duration"],
                    self._format_currency(entry["fee"])
                )
            )

        # 총합계 갱신
        total = self.calculator.get_total_sum()
        self.lbl_total.config(
            text=f"오늘의 총 합계: {self._format_currency(total)}"
        )

    def _on_calculate(self):
        in_val = self.ent_in.get()
        out_val = self.ent_out.get()

        try:
            self.calculator.calculate_fee(in_val, out_val)
            self._update_display()

            self.ent_in.delete(0, tk.END)
            self.ent_out.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("입력 오류", str(e))

    def _on_delete(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning(
                "알림",
                "삭제할 항목을 선택해주세요."
            )
            return

        index = self.tree.index(selected_item[0])

        try:
            self.calculator.remove_entry(index)
            self._update_display()

        except Exception as e:
            messagebox.showerror("삭제 오류", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()
