import os
from dotenv import load_dotenv
import requests
import time


load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CITIES = ["London", "New York", "Tokyo"]
CITY_CACHE = {}

def get_weather(city):
    if city in CITY_CACHE:
        print(f"Using cached weather data for {city}")
        data = CITY_CACHE[city]
        return data
    else:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "imperial"
        }
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params=params
        )
        time.sleep(1)
        if response.status_code == 200:
            print(f"Caching weather data for {city}")
            CITY_CACHE[city] = response.json()
            data = response.json()
            return data
    return False


def display_weather(weather_data):
    countrycode = weather_data["sys"]["country"]
    country = requests.get('https://restcountries.com/v3.1/alpha/'+countrycode).json()[0]

    print(f"Country: {str(country["name"]["common"])}")
    print()

    print('weather info')
    print(f'Temperature: {str(weather_data['main']['temp'])} °F')
    print(f'Conditions: {str(weather_data['weather'][0]['main'])}')
    print(f'Humidity: {str(weather_data['main']['humidity'])} %')
    print()

    print('country info')
    print(f'Capital: {str(country["capital"][0])}')
    print(f'Population: {str(country["population"])}')
    print(f'Languages: {str(list(country["languages"].values())[0])}')
    print(f'Currency: {str(list(country["currencies"].values())[0]["name"])} {str(list(country["currencies"].values())[0]["symbol"])}')

    return country


def main():
    if not API_KEY:
        print("Error: OPENWEATHER_API_KEY not found in .env file")
        return

    print("Weather Dashboard")
    print("=" * 40)
    while True:
        city_input = input("Choose a city: (quit to exit)")
        if city_input == "quit":
            break
        else:
            weather = get_weather(city_input)
            if weather:
                display_weather(weather)

if __name__ == "__main__":
    main()