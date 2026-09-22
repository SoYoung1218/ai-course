import flet as ft
from calc import Calculator

def main(page: ft.Page):
    page.title = "계산기"
    page.window.width = 340
    page.window.height = 520
    page.window.resizable = False

    calc = Calculator()

    display = ft.Text(value="0", size=40, text_align=ft.TextAlign.RIGHT)

    def update_display():
        display.value = calc.display
        page.update()

    def on_button_click(e):
        key = e.control.data
        calc.press(key)
        update_display()

    def on_key_down(e: ft.KeyboardEvent):
        key = e.key
        if key == "Enter":
            key = "="
        elif key == "Backspace":
            key = "BS"
        elif key == "Escape":
            key = "C"
        
        calc.press(key)
        update_display()

    page.on_keyboard_event = on_key_down

    def make_button(label, key, bgcolor):
        return ft.Button(
            content=ft.Text(label, size=20, color=ft.Colors.WHITE),
            data=key,
            on_click=on_button_click,
            expand=1,
            height=60,
            bgcolor=bgcolor,
        )

    page.add(
        ft.Container(
            content=display,
            alignment=ft.Alignment.CENTER_RIGHT,
            padding=10,
            height=90
        ),
        ft.Column([
            ft.Row([
                make_button("C", "C", ft.Colors.GREY_600),
                make_button("+/-", "+/-", ft.Colors.GREY_600),
                make_button("%", "%", ft.Colors.GREY_600),
                make_button("÷", "/", ft.Colors.ORANGE),
            ]),
            ft.Row([
                make_button("7", "7", ft.Colors.GREY_800),
                make_button("8", "8", ft.Colors.GREY_800),
                make_button("9", "9", ft.Colors.GREY_800),
                make_button("×", "*", ft.Colors.ORANGE),
            ]),
            ft.Row([
                make_button("4", "4", ft.Colors.GREY_800),
                make_button("5", "5", ft.Colors.GREY_800),
                make_button("6", "6", ft.Colors.GREY_800),
                make_button("−", "-", ft.Colors.ORANGE),
            ]),
            ft.Row([
                make_button("1", "1", ft.Colors.GREY_800),
                make_button("2", "2", ft.Colors.GREY_800),
                make_button("3", "3", ft.Colors.GREY_800),
                make_button("+", "+", ft.Colors.ORANGE),
            ]),
            ft.Row([
                make_button("0", "0", ft.Colors.GREY_800),
                make_button(".", ".", ft.Colors.GREY_800),
                make_button("⌫", "BS", ft.Colors.GREY_800),
                make_button("=", "=", ft.Colors.ORANGE),
            ]),
        ])
    )

if __name__ == "__main__":
    ft.run(main)
