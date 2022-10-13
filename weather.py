import requests
from pprint import pprint
from datetime import datetime

# potential constants
location_name = 'Eindhoven'
units = 'metric'
count = 8
API_KEY = 'f05ef9a17b18d9558976be06364d9c45'


def get_current_weather(location_name: str) -> dict:
    try:
        current = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={location_name}&appid={API_KEY}&units={units}")
    except Exception as ex:
        print(ex)
        return {}

    return current.json()


def get_forecast(location_name: str,) -> dict:
    try:
        forecast = requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?q={location_name}&appid={API_KEY}&units={units}&cnt={count}")
    except Exception as ex:
        print(ex)
        return {}
    return forecast.json()
