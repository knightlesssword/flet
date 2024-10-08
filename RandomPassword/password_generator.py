import random
import string

import flet
from anyio.abc import value
from flet_core import Page, ScrollMode, SnackBar, Text, colors, Slider, Checkbox, TextField, ElevatedButton, Column, \
    FontWeight, TextAlign, Row, MainAxisAlignment, IconButton, icons, CrossAxisAlignment, Container, Icon


def main(page: Page):
    page.title = "Random Password Generator"
    page.window.height = 500
    page.window.width = 600
    page.padding = 20
    page.scroll = ScrollMode.ADAPTIVE

    # default
    password_length = 12
    include_letters = True
    include_numbers = True
    include_symbols = True

    def generate_password(e):
        nonlocal password_length, include_symbols, include_letters, include_numbers

        password_length = int(slider.value)
        include_letters = cb_letters.value
        include_numbers = cb_numbers.value
        include_symbols = cb_symbols.value

        if not (include_numbers or include_letters or include_symbols):
            snack_bar = SnackBar(content=Text("Please check at least one character type!"), bgcolor=colors.RED)
            page.overlay.append(snack_bar)
            snack_bar.open = True
            return

        char_pool = ""
        if include_letters:
            char_pool+=string.ascii_letters
        if include_numbers:
            char_pool+=string.digits
        if include_symbols:
            char_pool+=string.punctuation

        if not char_pool:
            generated_password = ""
        else:
            generated_password = ''.join(random.choice(char_pool) for _ in range(password_length))

        password_field.value = generated_password
        page.update()

    def copy_password(e):
        if password_field.value:
            page.set_clipboard(password_field.value)
            snack_bar = SnackBar(
                content=Text("Password copied to clipboard!"),
                bgcolor=colors.GREEN
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    slider = Slider(
        min=1,
        max=24,
        divisions=23,
        label="{value}",
        value=password_length,
        on_change= lambda e:None,
    )

    cb_letters = Checkbox(label="Include Letters", value=True)
    cb_numbers = Checkbox(label="Include Numbers", value=True)
    cb_symbols = Checkbox(label="Include Special characters", value=True)

    password_field = TextField(
        value="",
        read_only=True,
        width=300,
        text_size=18
    )

    generate_btn = ElevatedButton(text="🔒 Generate Password 🔑", on_click=generate_password)
    copy_btn = ElevatedButton(text="📝 Copy Password ✂️", on_click=copy_password)
    length_display = Text("{}/24".format(password_length), size=16)

    page.add(
        Column([
            Text(
                value="Password Generator",
                size=30,
                color=colors.ORANGE,
                weight=FontWeight.BOLD,
                text_align=TextAlign.CENTER
            ),
            Text(
                value="Adjust the settings below to generate a strong password.",
                size=16,
                color=colors.GREY,
                text_align=TextAlign.CENTER
            ),
            Row([
                    Text("Length:", size=16),
                    slider,
                    length_display,
                ],
                alignment=MainAxisAlignment.CENTER,
            ),
            Column([
                    cb_letters,
                    cb_numbers,
                    cb_symbols,
                ],
                spacing=10,
            ),
            ElevatedButton(
                text="Generate Password",
                on_click=generate_password,
                width=200,
            ),
            Row(
                controls=[
                    password_field,
                    IconButton(icon=icons.COPY, tooltip="Copy to Clipboard", on_click=copy_password),
                ],
                alignment=MainAxisAlignment.CENTER,
                spacing=10,
            ),
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        ),
        Row(
            [
                Text("Made with", size=12),
                Icon(icons.FAVORITE, size=12, color=colors.RED),
                Text("in Flet by Abu Bakr.", size=12)
            ],
            alignment=MainAxisAlignment.CENTER
        )
    )

    def on_slider_change(e):
        nonlocal password_length
        password_length = int(e.control.value)
        length_display.value = "{}/24".format(password_length)
        page.update()

    slider.on_change = on_slider_change
    page.update()

if __name__ == '__main__':
    flet.app(target=main)