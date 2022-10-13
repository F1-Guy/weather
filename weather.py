from datetime import datetime
from typing import Any, Dict, List
import requests
from requests import ConnectionError

# TODO:
# See what kind of error checking and handling to use
# Remove constans and make them be configurable

LOCATION_NAME = 'Eindhoven'
UNITS = 'metric'
COUNT = 8
API_KEY = 'f05ef9a17b18d9558976be06364d9c45'


class DataPoint:
    """
    Represents a single data point retrieved from the API.
    The data point can be either current weather or one of the forecast time steps.
    It contains all of the attributes deemed necessary for the forecast module.
    """
    dt: datetime
    temp: float
    humidity: int
    id: int
    description: str
    icon: str
    city_name: str
    rain_last_hour: float
    rain_three_hours: float

    def __init__(self, json: Dict[str, Any]) -> None:
        """Not all of the attributes are always present in the data.
        The attributes that are not present are set to empty values.

        Args:
            json (Dict)): JSON current weather data retruned from OpenWeatherMap API

        Returns:
            None
        """
        self.dt = datetime.fromtimestamp(json['dt'])
        self.temp = json.get('main', {})['temp']
        self.humidity = json.get('main', {})['humidity']
        self.id = json.get('weather', [])[0]['id']
        self.description = json.get('weather', [])[0]['description']
        self.icon = json.get('weather', [])[0]['icon']
        self.city_name = json.get('name', {})
        self.rain_last_hour = json.get('rain', {}).get('1h', {})
        self.rain_three_hours = json.get('rain', {}).get('3h', {})


class Forecast:
    """Represents a forecast as a list of data points retrieved from the API.
    Each data point represents a single time step.
    """
    data: List[DataPoint]

    def __init__(self, json: Dict) -> None:
        """Initializes the forecast object with a list of data points.
        Automatically populates the list from the list contained in the response.

        Args:
            json (Dict)): JSON forecast data retruned from OpenWeatherMap API

        Returns:
            None
        """
        self.data = [DataPoint(i) for i in json['list']]


class WeatherAPI:
    """
    Contains all the data needed for the forecast module
    and methods for retrieving and updating that data.

    Args:
        location_name (str): Name of the location to get weather for
    """
    current: DataPoint
    forecast: Forecast

    def __init__(self, location_name: str) -> None:
        """Initializes the weather API object with the current weather and forecast data."""
        self.location_name = location_name
        self.update()

    def update(self) -> None:
        """Updates the current weather and forecast data."""
        self.get_weather(self.location_name)

    def get_weather(self, location_name: str) -> None:
        """
        Makes a GET request to the OpenWeatherMap API and retrieves the current weather and forecast form different endpoints.

        Args:
            location_name (str): Name of the location to get weather for

        Returns:
            None

        Errors:
            ValueError: If the response from the API is not valid
        """
        try:
            current = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={location_name}&appid={API_KEY}&units={UNITS}', timeout=5)
            forecast = requests.get(
                f'https://api.openweathermap.org/data/2.5/forecast?q={location_name}&appid={API_KEY}&units={UNITS}&cnt={COUNT}', timeout=5)
        except ConnectionError as ex:
            print(ex)

        current_json = current.json()
        forecast_json = forecast.json()

        if not current_json or not forecast_json or current_json['cod'] != 200 or forecast_json['cod'] != '200':
            raise ValueError('Invalid response from the API')

        self.current = DataPoint(current_json)
        self.forecast = Forecast(forecast_json)


if __name__ == "__main__":
    weather = WeatherAPI(LOCATION_NAME)

    print('Current temp:')
    print(f'{weather.current.dt}: {weather.current.temp}')

    print()

    print('Forecast temps:')
    for time_step in weather.forecast.data:
        print(f'{time_step.dt}: {time_step.temp}')
