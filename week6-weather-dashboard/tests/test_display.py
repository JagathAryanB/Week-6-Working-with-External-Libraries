from io import StringIO
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from weather_app.weather_display import WeatherDisplay

class TestWeatherDisplay(unittest.TestCase):

    def test_temperature_colors(self):
        cold_color = WeatherDisplay.get_temperature_color(-5)
        self.assertIn("36", cold_color)

        cool_color = WeatherDisplay.get_temperature_color(10)
        self.assertIn("34", cool_color)

        pleasant_color = WeatherDisplay.get_temperature_color(18)
        self.assertIn("32", pleasant_color)

        warm_color = WeatherDisplay.get_temperature_color(28)
        self.assertIn("33", warm_color)

        hot_color = WeatherDisplay.get_temperature_color(36)
        self.assertIn("31", hot_color)

    def test_get_ascii_art(self):
        rain_art = WeatherDisplay.get_ascii_art("heavy rain")
        self.assertGreater(len(rain_art), 0)

        sun_art = WeatherDisplay.get_ascii_art("clear sky")
        self.assertGreater(len(sun_art), 0)

        snow_art = WeatherDisplay.get_ascii_art("light snow")
        self.assertGreater(len(snow_art), 0)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_full_dashboard(self, mock_stdout):
        current_mock = {
            "city": "London",
            "country": "GB",
            "updated_at": "2024-01-25 10:15:00",
            "temp_raw": 8.0,
            "temp": "8°C",
            "feels_like": "5°C",
            "conditions": "Light rain 🌧️",
            "humidity": "87%",
            "wind": "22 km/h from SW",
            "pressure": "1009 hPa",
            "visibility": "8 km",
            "sunrise": "07:45",
            "sunset": "16:30"
        }
        forecast_mock = [
            {"day_label": "Thu 25 Jan", "icon": "🌧️", "temp_max": "9°C", "temp_min": "6°C", "humidity": "(Humidity: 85%)"}
        ]
        WeatherDisplay.display_full_dashboard(current_mock, forecast_mock, "Test status")
        output = mock_stdout.getvalue()

        self.assertIn("WEATHER DASHBOARD", output)
        self.assertIn("London, GB", output)
        self.assertIn("8°C", output)
        self.assertIn("Light rain", output)
        self.assertIn("Thu 25 Jan", output)
        self.assertIn("Test status", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_comparison(self, mock_stdout):
        c1 = {"city": "London", "country": "GB", "temp": "8°C", "feels_like": "5°C", "conditions": "Rain", "humidity": "87%", "wind": "22 km/h", "pressure": "1009 hPa", "visibility": "8 km"}
        c2 = {"city": "Tokyo", "country": "JP", "temp": "12°C", "feels_like": "11°C", "conditions": "Clear", "humidity": "60%", "wind": "10 km/h", "pressure": "1018 hPa", "visibility": "10 km"}
        WeatherDisplay.display_comparison(c1, c2)
        output = mock_stdout.getvalue()
        self.assertIn("WEATHER COMPARISON BETWEEN CITIES", output)
        self.assertIn("London, GB", output)
        self.assertIn("Tokyo, JP", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_help(self, mock_stdout):
        WeatherDisplay.display_help()
        output = mock_stdout.getvalue()
        self.assertIn("WEATHER DASHBOARD - HELP", output)
        self.assertIn("Dashboard View", output)
        self.assertIn("City Search", output)

if __name__ == "__main__":
    unittest.main()
