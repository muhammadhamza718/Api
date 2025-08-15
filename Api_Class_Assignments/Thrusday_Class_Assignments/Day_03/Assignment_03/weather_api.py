# weather_api.py
import requests
from decouple import config

# Load the API key from the environment
API_KEY = config("WEATHER_API_KEY")

def get_weather(city: str) -> str:
    """
    Fetches the current temperature for a given city using the OpenWeatherMap API.
    
    Args:
        city (str): The name of the city to get weather data for.
    
    Returns:
        str: A message with the current temperature in Celsius or an error message.
    """
    # Step 1: Get latitude and longitude using the Geocoding API
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geo_response = requests.get(geo_url)
    
    if geo_response.status_code != 200 or not geo_response.json():
        return "City not found. Please check the city name and try again."
    
    location = geo_response.json()[0]
    lat = location["lat"]
    lon = location["lon"]
    
    # Step 2: Fetch weather data using the Current Weather Data API
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    weather_response = requests.get(weather_url)
    
    if weather_response.status_code != 200:
        return "An error occurred while fetching weather data."
    
    weather_data = weather_response.json()
    temp = weather_data["main"]["temp"]
    
    return f"The current temperature in {city} is {temp}°C."