import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from weather_app.weather_api import WeatherAPI

class TestWeatherAPI(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cache_dir = Path(self.temp_dir.name) / "cache"
        self.api = WeatherAPI(
            api_key="mock_test_key",
            base_url="https://api.openweathermap.org/data/2.5",
            cache_dir=self.cache_dir,
            cache_duration=60
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_cache_save_and_retrieve(self):
        test_data = {"city": "Berlin", "temp": 20.5}
        self.api._save_to_cache("test_berlin", test_data)

        retrieved = self.api._get_cached_data("test_berlin")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.get("city"), "Berlin")
        self.assertEqual(retrieved.get("temp"), 20.5)

    def test_cache_miss_for_nonexistent_key(self):
        retrieved = self.api._get_cached_data("non_existent_key")
        self.assertIsNone(retrieved)

    @patch("requests.get")
    def test_make_request_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "Tokyo", "cod": 200}
        mock_get.return_value = mock_response

        data = self.api._make_request("weather", {"q": "Tokyo"})
        self.assertIsNotNone(data)
        self.assertEqual(data.get("name"), "Tokyo")

    @patch("requests.get")
    def test_make_request_invalid_key(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        data = self.api._make_request("weather", {"q": "Tokyo"})
        self.assertIsNone(data)

    def test_get_current_weather_fallback_when_no_api(self):
        api_no_key = WeatherAPI(api_key="", cache_dir=self.cache_dir)
        data = api_no_key.get_current_weather("London")
        self.assertIsNotNone(data)
        self.assertEqual(data.get("name"), "London")
        self.assertIn("main", data)

    def test_get_forecast_fallback_structure(self):
        api_no_key = WeatherAPI(api_key="", cache_dir=self.cache_dir)
        data = api_no_key.get_forecast("Paris")
        self.assertIsNotNone(data)
        self.assertIn("list", data)
        self.assertGreaterEqual(len(data["list"]), 5)

    def test_search_cities(self):
        results = self.api.search_cities("lon")
        self.assertTrue(any("London" in r for r in results))

    def test_export_weather_to_csv(self):
        csv_file = Path(self.temp_dir.name) / "test_export.csv"
        current_mock = {
            "name": "London",
            "sys": {"country": "GB"},
            "main": {"temp": 8.0, "feels_like": 5.0, "temp_min": 6.0, "temp_max": 9.0, "humidity": 87},
            "weather": [{"description": "light rain"}],
            "wind": {"speed": 6.1}
        }
        forecast_mock = [
            {"date_str": "2026-10-18", "temp_avg": 8.0, "temp_min": 5.0, "temp_max": 10.0, "condition": "Clouds", "humidity": 80}
        ]
        success = self.api.export_weather_to_csv(current_mock, forecast_mock, csv_file)
        self.assertTrue(success)
        self.assertTrue(csv_file.exists())
        content = csv_file.read_text(encoding="utf-8")
        self.assertIn("London", content)
        self.assertIn("light rain", content)

if __name__ == "__main__":
    unittest.main()
