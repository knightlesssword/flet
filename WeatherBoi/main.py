import os
import flet
import requests
from flet import Page
from dotenv import load_dotenv
from flet_core import (
    TextField, Text, ElevatedButton, Container, MainAxisAlignment, Row, colors, Icon, icons)

load_dotenv()

def get_weather(city, api_key):
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        weather = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'].title(),
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return weather
    except requests.exceptions.HTTPError as http_err:
        return {'error': f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {'error': f"An error occurred: {err}"}

def main(page: Page):
    page.title = "WeatherBoi"
    page.window.height = 650
    page.window.width = 600
    page.padding = 20

    api_key = os.getenv('API_KEY')

    city_input = TextField(
        label= "Enter city...",
        width= 350,
        autofocus= True
    )

    result_text = Text()

    def fetch_weather(e):
        city = city_input.value.strip()
        if not city:
            result_text.value = "Please enter city name."
            page.update()
            return

        weather = get_weather(city, api_key)
        if 'error' in weather:
            result_text.value = "Unable to find city!\r\n"+weather['error']
        else:
            result_text.value = (
                f"City: {weather['city']}\n"
                f"Temperature: {weather['temperature']}°C\n"
                f"Weather: {weather['description']}\n"
                f"Humidity: {weather['humidity']}%\n"
                f"Wind Speed: {weather['wind_speed']} m/s"
            )
        page.update()

    fetch_button = ElevatedButton(
        text= "Fetch!",
        on_click= fetch_weather
    )

    page.add(
       Row(
           [
               Text("WeatherBoi", color=colors.ORANGE, size=40),
           ],
           alignment=MainAxisAlignment.SPACE_EVENLY
       ),
        Row(

        ),
        Row(
            [
                city_input
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
        Row(
            [
                fetch_button
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
        Row(

        ),
        Row(
            [
                Container(
                    content= result_text,
                    margin=10
                )
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
        Row(

        ),
        Row(
            [
                Text("Made with"),
                Icon(name=icons.FAVORITE, color=colors.RED, size=13),
                Text("in Flet by Abu Bakr.")
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
    )

if __name__ == '__main__':
    flet.app(target=main)