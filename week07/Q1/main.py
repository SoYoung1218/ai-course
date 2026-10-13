import flet as ft
import logic


def main(page: ft.Page):
    page.title = "단위 변환기"
    page.window.width = 380
    page.window.height = 500
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT

    units = [
        ft.dropdown.Option("mm"),
        ft.dropdown.Option("cm"),
        ft.dropdown.Option("m"),
        ft.dropdown.Option("km"),
        ft.dropdown.Option("°C"),
        ft.dropdown.Option("°F"),
    ]

    value_input = ft.TextField(
        label="값",
        value="",
        width=160,
        text_align=ft.TextAlign.CENTER,
    )

    unit_dropdown = ft.Dropdown(
        label="단위",
        value="cm",
        width=160,
        options=units,
    )

    result_text = ft.TextField(
        label="결과",
        value="",
        width=160,
        read_only=True,
        text_align=ft.TextAlign.CENTER,
    )

    target_unit_dropdown = ft.Dropdown(
        label="단위",
        value="m",
        width=160,
        options=units,
    )

    notice_text = ft.Text(
        value="",
        color=ft.Colors.RED,
        size=14,
    )

    def on_run(e):
        notice_text.value = ""
        result_text.value = ""

        raw_value = value_input.value.strip()

        if not raw_value:
            notice_text.value = "값을 입력해주세요."
            page.update()
            return

        try:
            num_value = float(raw_value)
        except ValueError:
            notice_text.value = "숫자를 입력해주세요."
            page.update()
            return

        success, converted_value = logic.convert_units(
            num_value,
            unit_dropdown.value,
            target_unit_dropdown.value,
        )

        if success:
            if (
                isinstance(converted_value, float)
                and converted_value.is_integer()
            ):
                result_text.value = str(int(converted_value))
            else:
                result_text.value = str(converted_value)
        else:
            notice_text.value = converted_value

        page.update()

    convert_button = ft.Button(
        content=ft.Text("변환"),
        on_click=on_run,
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE,
        width=340,
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
    )

    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[value_input, unit_dropdown],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(
                    "↓",
                    size=30,
                    color=ft.Colors.BLUE_GREY_400,
                ),
                ft.Row(
                    controls=[
                        result_text,
                        target_unit_dropdown,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(
                    content=convert_button,
                    margin=ft.Margin(
                        left=0,
                        top=30,
                        right=0,
                        bottom=10,
                    ),
                ),
                ft.Container(
                    content=notice_text,
                    alignment=ft.Alignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
    )


if __name__ == "__main__":
    ft.run(main)