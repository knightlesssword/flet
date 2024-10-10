import flet
from flet import (
    Page,
    Text,
    TextField,
    Dropdown,
    ElevatedButton,
    Column,
    Row,
    ProgressRing,
)
from flet_core import KeyboardType, FontWeight, MainAxisAlignment, CrossAxisAlignment, dropdown, colors, Markdown, \
    MarkdownExtensionSet, Icon, icons, Alignment, border, Container, IconButton, ThemeMode
from freecurrencyapi import Client
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

def main(page: Page):
    page.title = "Currency Converter"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.window.width = 600
    page.window.height = 650
    page.padding = 10
    page.window.theme_mode = ThemeMode.DARK


    # UI Components
    currencies_dropdown_from = Dropdown(label="From", width=200, hint_text="From Currency", border_color=colors.WHITE)
    currencies_dropdown_to = Dropdown(label="To", width=200, hint_text="To Currency", border_color=colors.WHITE)
    amount_field = TextField(label="Amount", width=200, value="1", keyboard_type=KeyboardType.NUMBER, border_color=colors.WHITE)
    convert_button = ElevatedButton(text="Convert", on_click=lambda e: convert_currency())
    status_button = ElevatedButton(text="Check Quota", on_click=lambda e: check_quota())
    convert_result = Text(size=20)
    status_text = Text(size=16)
    error_message = Text(color="red")
    progress = ProgressRing(visible=False)

    if API_KEY:
        api = Client(API_KEY)
    else:
        error_message.value = "No API key found!"

    # Function to fetch and populate currencies
    def fetch_currencies():
        try:
            response = api.currencies()  # Call currencies endpoint
            if "data" in response:
                currencies = response["data"]
                currency_items = [
                    dropdown.Option(key=code, text=f"{code}", alignment=Alignment(0,0))
                    for code, details in currencies.items()
                ]
                currencies_dropdown_from.options = currency_items
                currencies_dropdown_to.options = currency_items

                # Set default selections
                currencies_dropdown_from.value = "USD"
                currencies_dropdown_to.value = "EUR"
                page.update()
            else:
                handle_error("Failed to fetch currencies.")
        except Exception as ex:
            error_message.value = f"Error fetching currencies: {ex}"
            update_results_visibility()
            page.update()

    # Function to handle currency conversion
    def convert_currency():
        error_message.value = ""
        convert_result.value = ""
        progress.visible = True
        page.update()

        from_currency = currencies_dropdown_from.value
        to_currency = currencies_dropdown_to.value
        amount = amount_field.value

        if not from_currency or not to_currency:
            error_message.value = "Please select both currencies."
            progress.visible = False
            update_results_visibility()
            page.update()
            return

        try:
            amount_float = float(amount)
        except ValueError:
            error_message.value = "Enter a valid number for amount."
            progress.visible = False
            update_results_visibility()
            page.update()
            return

        try:
            response = api.latest(base_currency=from_currency)  # Call latest rates
            if "data" in response:
                converted_amount = response["data"][to_currency]
                total_amount = round(amount_float * converted_amount, 2)
                convert_result.value = f"{amount_float} {from_currency} = {total_amount} {to_currency}"
            else:
                handle_error("Failed to fetch latest rates.")
        except Exception as ex:
            error_message.value = f"Conversion error: {ex}"
            update_results_visibility()
        finally:
            progress.visible = False
            update_results_visibility()
            page.update()

    # Function to check API quota
    def check_quota():
        status_text.value = ""
        error_message.value = ""
        progress.visible = True
        page.update()

        try:
            response = api.status()  # Call status endpoint
            if "quotas" in response:
                month_quota = response["quotas"]["month"]
                status_text.value = (
                    f"Monthly Quota:\nTotal: {month_quota['total']}\nUsed: {month_quota['used']}\nRemaining: {month_quota['remaining']}"
                )
            else:
                handle_error("Failed to fetch quota status.")
        except Exception as ex:
            error_message.value = f"Error checking quota: {ex}"
            update_results_visibility()
        finally:
            progress.visible = False
            update_results_visibility()
            page.update()

    # Function to handle errors
    def handle_error(message):
        error_message.value = message
        update_results_visibility()

    # Initial fetch of currencies
    fetch_currencies()

    def open_url(e):
        page.launch_url(e.data)

    def update_results_visibility():
        if convert_result.value or status_text.value or error_message.value:
            result_area_container.visible = True
        else:
            result_area_container.visible = False
        page.update()

    result_area_container = Container(
            Column(
                [
                    progress,
                    convert_result,
                    status_text,
                    error_message,
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
        ),
        border=border.all(2),
        border_radius=6,
        padding=5,
        visible=False,
        alignment=Alignment(0,0)
    )

    def toggle_theme(e):
        if page.theme_mode == ThemeMode.LIGHT:
            page.theme_mode = ThemeMode.DARK
            page.bg_color = colors.BLACK
            e.control.icon = icons.BRIGHTNESS_5
        else:
            page.theme_mode = ThemeMode.LIGHT
            page.bg_color = colors.LIGHT_BLUE
            e.control.icon = icons.BRIGHTNESS_3
        page.update()

    switch_button = IconButton(
        icon=icons.BRIGHTNESS_3,  # Moon icon for dark mode
        on_click=toggle_theme,
        icon_color=colors.YELLOW,
        bgcolor=colors.TRANSPARENT,
    )

    # UI Layout
    page.add(
        Column(
            [
                Text("Currency Converter", size=30, weight=FontWeight.BOLD, color=colors.ORANGE),
                Row(
                    [
                        currencies_dropdown_from,
                        Text("          "),
                        currencies_dropdown_to,
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                amount_field,
                Row(
                    [
                        convert_button,
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                Row(
                    [
                        status_button,
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                result_area_container,
                Row(
                    [
                        Text("Powered by", color=colors.GREY, size=13),
                        Markdown(
                            "[FreecurrencyAPI](https://app.freecurrencyapi.com/)",
                            extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            on_tap_link=open_url,
                            expand=False,
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                Row(
                    [
                        switch_button
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                Row(
                    [
                        Text("Made with"),
                        Icon(name=icons.FAVORITE, color=colors.RED, size=13),
                        Text("in Flet by Abu Bakr."),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

if __name__ == "__main__":
    flet.app(target=main)
