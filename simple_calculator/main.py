import flet as ft
import logging
from flet import ElevatedButton, FontWeight

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def main(page: ft.Page):

    page.title = "Simple Calculator"
    page.window.height = 550
    page.window.width = 500
    page.window.bg_color = ft.colors.WHITE
    page.window.theme_mode = ft.ThemeMode.DARK

    operator, operand1, new_operand = None, 0, True

    # Result display
    result_text = ft.Text(
        value="0", color=ft.colors.WHITE, size=45, weight=FontWeight.BOLD, text_align=ft.TextAlign.RIGHT
    )

    # Button click event handler
    def button_clicked(e):
        nonlocal operator, operand1, new_operand
        label = e.control.text

        if label == 'AC':
            result_text.value = "0"
            operator, operand1, new_operand = None, 0, True

        elif label in "0123456789.":
            if new_operand or result_text.value == "0":
                result_text.value = label
                new_operand = False
            else:
                if label == "." and "." in result_text.value:
                    return
                result_text.value += label

        elif label in "+-*/":
            try:
                operand1 = float(result_text.value)
                operator = label
                new_operand = True
            except ValueError:
                result_text.value = "Error"
                new_operand = True

        elif label == "+/-":
            if result_text.value.startswith("-"):
                result_text.value = result_text.value[1:]
            elif result_text.value != "0":
                result_text.value = "-" + result_text.value

        elif label == "%":
            try:
                result_text.value = str(float(result_text.value) / 100)
                new_operand = True
            except ValueError:
                result_text.value = "Error"
                new_operand = True

        elif label == "=":
            try:
                operand2 = float(result_text.value)
                result = None
                if operator == "+":
                    result = operand1 + operand2
                elif operator == "-":
                    result = operand1 - operand2
                elif operator == "*":
                    result = operand1 * operand2
                elif operator == "/":
                    result = operand1 / operand2 if operand2 != 0 else "Error"

                result_text.value = str(result) if result != "Error" else "Error"
                operator = None
                new_operand = True
            except ValueError:
                result_text.value = "Error"
                operator = None
                new_operand = True

        page.update()

    # Theme switcher
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            page.bg_color = ft.colors.BLACK
            result_text.color = ft.colors.WHITE
            e.control.icon = ft.icons.BRIGHTNESS_5
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bg_color = ft.colors.LIGHT_BLUE_50
            result_text.color = ft.colors.BLACK
            e.control.icon = ft.icons.BRIGHTNESS_3
        page.update()

    # Create calculator buttons layout

    button_height = page.window.height * 0.09

    buttons = [
        ["AC", "+/-", "%", "/"],
        ["7", "8", "9", "*"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["0", ".", "="]
    ]

    # Rows of buttons
    rows = [
        ft.Row(
            controls=[
                ElevatedButton(
                    text=label,
                    height=button_height,
                    expand=2 if label == "0" else 1,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.ORANGE if label in "+-*/" else ft.colors.GREY_600 if label in ".AC+/-%0123456789" else ft.colors.RED,
                    on_click=button_clicked
                )
                for label in row
            ],
            spacing=5
        )
        for row in buttons
    ]

    # Add the sun/moon toggle button for theme switching
    switch_button = ft.IconButton(
        icon=ft.icons.BRIGHTNESS_3,  # Moon icon for dark mode
        on_click=toggle_theme,
        icon_color=ft.colors.YELLOW,
        bgcolor=ft.colors.TRANSPARENT,
    )

    # Full calculator layout
    calculator_layout = ft.Container(
        width=page.window.width,
        height=page.window.height,
        bgcolor=page.bg_color,
        border_radius=ft.border_radius.all(20),
        padding=20,
        content=ft.Column(
            controls=[
                ft.Row(controls=[result_text], alignment=ft.MainAxisAlignment.END),
                *rows,
                ft.Row(controls=[switch_button], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    ft.Row(
                        controls =[
                            ft.Text("Simple Calculator", size=15, color = ft.colors.ORANGE)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ),
                ft.Container(
                    ft.Row(
                        controls = [
                            ft.Text("Made with", size=12),
                            ft.Icon(ft.icons.FAVORITE, size=12, color=ft.colors.RED),
                            ft.Text("in Flet by Abu Bakr.", size=12)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ),
            ],
            spacing=10
        )
    )

    # Add calculator layout to page
    page.add(calculator_layout)

    # Update layout on window resize
    def on_resize(e):
        try:
            nonlocal button_height
            calculator_layout.width = page.window.width
            calculator_layout.height = page.window.height
            button_height = page.window.height * 0.1
            page.update()
        except ValueError as ex:
            logging.error(msg=[e, ex])

    page.on_resized = on_resize

ft.app(target=main)
