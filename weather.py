import sys
import requests
from datetime import datetime
from typing import Any, Dict, List

LOCATION_NAME = "Eindhoven"
UNITS = "metric"
COUNT = 80
API_KEY = "f05ef9a17b18d9558976be06364d9c45"


class DataPoint:
    dt: datetime
    temp: float
    humidity: int
    id: int
    description: str
    icon: str
    city_name: str
    rain_last_hour: float | None
    rain_three_hours: float | None

    def __init__(self, json: Dict[str, Any]) -> None:
        self.dt = datetime.fromtimestamp(json["dt"])
        self.temp = json.get("main", {})["temp"]
        self.humidity = json.get("main", {})["humidity"]
        self.id = json.get("weather", [])[0]["id"]
        self.description = json.get("weather", [])[0]["description"]
        self.icon = json.get("weather", [])[0]["icon"]
        self.city_name = json.get("name", {})
        self.rain_last_hour = json.get("rain", {}).get("1h", {})
        self.rain_three_hours = json.get("rain", {}).get("3h", {})


class Forecast:
    data: List[DataPoint]

    def __init__(self, json_list: Dict):
        self.data = [DataPoint(i) for i in json_list["list"]]


class WeatherAPI:
    current: DataPoint
    forecast: Forecast

    def __init__(self, location_name):
        self.location_name = location_name
        self.update()

    def update(self):
        self.get_weather(self.location_name)

    def get_weather(self, location_name: str):
        try:
            current = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={location_name}&appid={API_KEY}&units={UNITS}")
            forecast = requests.get(
                f"https://api.openweathermap.org/data/2.5/forecast?q={location_name}&appid={API_KEY}&units={UNITS}&cnt={COUNT}")
        except:
            print("An error has occured while fetching data from the API",
                  file=sys.stderr)
            return

        current_json = current.json()
        forecast_json = forecast.json()

        if not current_json or not forecast_json or current_json["cod"] != 200 or forecast_json["cod"] != "200":
            print("An error occured while reading data", file=sys.stderr)
            return

        self.current = DataPoint(current_json)
        self.forecast = Forecast(forecast_json)


if __name__ == "__main__":
    weather = WeatherAPI(LOCATION_NAME)
    print(weather.current.temp)
    print(weather.forecast.data[0].temp)
