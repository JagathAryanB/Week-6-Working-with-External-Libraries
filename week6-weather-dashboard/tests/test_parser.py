from pathlib import Path
import unittest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from weather_app.weather_parser import WeatherParser

class TestWeatherParser(unittest.TestCase):

    def test_celsius_to_fahrenheit(self):
        self.assertEqual(WeatherParser.celsius_to_fahrenheit(0), 32.0)
        self.assertEqual(WeatherParser.celsius_to_fahrenheit(100), 212.0)
        self.assertEqual(WeatherParser.celsius_to_fahrenheit(8), 46.4)

    def test_fahrenheit_to_celsius(self):
        self.assertEqual(WeatherParser.fahrenheit_to_celsius(32), 0.0)
        self.assertEqual(WeatherParser.fahrenheit_to_celsius(212), 100.0)

    def test_format_temperature_metric_and_imperial(self):
        self.assertEqual(WeatherParser.format_temperature(8.0, "metric"), "8°C")
        self.assertEqual(WeatherParser.format_temperature(8.0, "imperial"), "46°F")

    def test_get_condition_icon(self):
        self.assertEqual(WeatherParser.get_condition_icon("clear sky"), "☀️")
        self.assertEqual(WeatherParser.get_condition_icon("light rain"), "🌧️")
        self.assertEqual(WeatherParser.get_condition_icon("overcast clouds"), "☁️")
        self.assertEqual(WeatherParser.get_condition_icon("thunderstorm with rain"), "⛈️")

    def test_degrees_to_cardinal(self):
        self.assertEqual(WeatherParser.degrees_to_cardinal(0), "N")
        self.assertEqual(WeatherParser.degrees_to_cardinal(90), "E")
        self.assertEqual(WeatherParser.degrees_to_cardinal(180), "S")
        self.assertEqual(WeatherParser.degrees_to_cardinal(225), "SW")
        self.assertEqual(WeatherParser.degrees_to_cardinal(270), "W")

    def test_parse_current_weather(self):
        raw_mock = {
            "name": "London",
            "sys": {"country": "GB", "sunrise": 1706168700, "sunset": 1706200200},
            "main": {
                "temp": 8.0,
                "feels_like": 5.0,
                "temp_min": 6.0,
                "temp_max": 9.0,
                "pressure": 1009,
                "humidity": 87
            },
            "weather": [{"description": "light rain"}],
            "wind": {"speed": 6.11, "deg": 225},
            "visibility": 8000,
            "dt": 1706177700
        }
        parsed = WeatherParser.parse_current_weather(raw_mock, "metric")
        self.assertEqual(parsed["city"], "London")
        self.assertEqual(parsed["country"], "GB")
        self.assertEqual(parsed["temp"], "8°C")
        self.assertEqual(parsed["feels_like"], "5°C")
        self.assertEqual(parsed["humidity"], "87%")
        self.assertIn("Light rain", parsed["conditions"])
        self.assertIn("SW", parsed["wind"])
        self.assertEqual(parsed["pressure"], "1009 hPa")
        self.assertEqual(parsed["visibility"], "8 km")

    def test_parse_forecast(self):
        raw_mock = {
            "list": [
                {
                    "dt_txt": "2026-10-18 12:00:00",
                    "main": {"temp_min": 6.0, "temp_max": 9.0, "humidity": 85},
                    "weather": [{"main": "Rain"}]
                },
                {
                    "dt_txt": "2026-10-19 12:00:00",
                    "main": {"temp_min": 4.0, "temp_max": 8.0, "humidity": 78},
                    "weather": [{"main": "Clouds"}]
                }
            ]
        }
        forecast = WeatherParser.parse_forecast(raw_mock, "metric")
        self.assertEqual(len(forecast), 2)
        self.assertEqual(forecast[0]["temp_max"], "9°C")
        self.assertEqual(forecast[0]["temp_min"], "6°C")
        self.assertIn("85%", forecast[0]["humidity"])

if __name__ == "__main__":
    unittest.main()
