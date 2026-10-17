import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_weather(city, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("Error: Invalid API Key. Please provide a valid OpenWeatherMap API key in .env or via argument.")
            return None
        elif response.status_code == 404:
            print(f"Error: City '{city}' not found.")
            return None
        else:
            print(f"Error: API returned status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None

def display_weather(data):
    if not data:
        return
    city = data.get("name", "Unknown")
    country = data.get("sys", {}).get("country", "")
    main = data.get("main", {})
    weather = data.get("weather", [{}])[0]
    wind = data.get("wind", {})

    print("\n" + "=" * 40)
    print(f"Weather for {city}, {country}")
    print("=" * 40)
    print(f"Condition   : {weather.get('main', 'N/A')} ({weather.get('description', 'N/A')})")
    print(f"Temperature : {main.get('temp', 'N/A')} °C")
    print(f"Feels Like  : {main.get('feels_like', 'N/A')} °C")
    print(f"Humidity    : {main.get('humidity', 'N/A')} %")
    print(f"Pressure    : {main.get('pressure', 'N/A')} hPa")
    print(f"Wind Speed  : {wind.get('speed', 'N/A')} m/s")
    print("=" * 40 + "\n")

def main():
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    city = sys.argv[1] if len(sys.argv) > 1 else "New Delhi"
    
    if not api_key:
        print("Note: OPENWEATHER_API_KEY not found in environment or .env file.")
        print("Demonstrating weather response structure using fallback demo data:")
        demo_data = {
            "name": city,
            "sys": {"country": "IN"},
            "main": {"temp": 26.5, "feels_like": 25.8, "humidity": 52, "pressure": 1013},
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "wind": {"speed": 3.6}
        }
        display_weather(demo_data)
        return

    data = fetch_weather(city, api_key)
    display_weather(data)

if __name__ == "__main__":
    main()
