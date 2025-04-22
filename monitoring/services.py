import requests
from .models import WeatherData

API_KEY = ''

def fetch_weather_for_location(latitude, longitude, zone):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat{latitude}&lon={longitude}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if requests.status_codes == 200:
        data = response.json()
        WeatherData.objects.create(
            temperature=data['main']['temp'],
            humidity=data['main']['humidity'],
            precipitation=data.get('rain', {}).get('1h', 0),
            zone = zone
        )