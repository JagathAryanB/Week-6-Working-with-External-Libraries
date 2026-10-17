# Week 6: Working with External Libraries

> **Source:** [The Developers Arena](https://thedevelopersarena.com)  
> **Topic:** Week 6: Working with External Libraries — Weather Dashboard Application  
> **Original Source Image:** [`implementation.jpg`](./implementation.jpg)  
> **Detailed Implementation Spec:** [`IMPLEMENTATION.md`](./IMPLEMENTATION.md)

---

## 📸 Complete Original Image Reference
Below is the full original reference image preserved in high resolution:

![Complete Implementation Guide](./implementation.jpg)

---

## 📑 Table of Contents
1. [Header & Overview](#-header--overview)
2. [Theory Concepts](#-theory-concepts)
3. [Hands-On Practice](#-hands-on-practice)
4. [Project: Weather Dashboard Application](#-project-weather-dashboard-application)
5. [Technical Requirements](#-technical-requirements)
6. [Step-by-Step Guide](#-step-by-step-guide)
   - [Structured Overview](#structured-overview)
   - [Verbatim Numbered List (Items 1–46)](#verbatim-numbered-list-items-146)
7. [Sample Code: `weather_api.py`](#-sample-code-weather_apipy)
   - [Complete & Functional Code](#complete--functional-code)
   - [Exact Visible Text (Screenshot Verbatim)](#exact-visible-text-screenshot-verbatim)
8. [Sample Output](#-sample-output)
9. [Submission Requirements & GitHub Structure](#-submission-requirements)

---

## 🌐 Header & Overview

- **Platform:** The Developers Arena
- **URL:** `thedevelopersarena.com/task...`
- **Module:** Week 6: Working with External Libraries

---

## 📚 Theory Concepts:

- **Package Management:** Understanding pip and virtual environments
- **Date & Time:** Working with datetime module for time operations
- **HTTP Requests:** Making API calls with requests library
- **JSON Data:** Parsing and working with JSON responses
- **Environment Variables:** Managing API keys and configuration
- **API Documentation:** Reading and understanding API documentation

---

## 🛠️ Hands-On Practice:

- Create a program that displays current date and time in different formats
- Build a weather app that fetches data from OpenWeatherMap API
- Make a currency converter using real exchange rates from an API
- Create a program that generates random user data using Faker library
- Practice installing and managing packages with pip
- Work with JSON data from various public APIs

---

## 🎯 Project: Weather Dashboard Application

Build a comprehensive weather application that fetches current weather, forecasts, and historical data from a weather API. Display the information in a user-friendly format with multiple views and customization options. This project teaches API integration, error handling, and working with external data sources.

---

## 🛠️ Technical Requirements:

- Integrate with a free weather API (OpenWeatherMap, WeatherAPI, etc.)
- Fetch current weather for any city worldwide
- Display 5-day weather forecast
- Show weather details: temperature, humidity, wind speed, conditions
- Implement city search with autocomplete suggestions
- Add temperature unit conversion (Celsius/Fahrenheit)
- Implement error handling for API failures
- Cache API responses to reduce calls
- Create a user-friendly command-line interface

---

## 📋 Step-by-Step Guide:

### Structured Overview

#### Step 1: API Setup & Exploration
- • Sign up for free API key from OpenWeatherMap or similar
- • Explore API documentation and test endpoints
- • Understand the JSON response structure
- • Set up environment variables for API key

#### Step 2: Project Structure
- • Create project folder with modular structure
- • Set up requirements.txt with dependencies
- • Create configuration file for API settings
- • Set up .env file for sensitive data

#### Step 3: API Client Module
- • Create weather_api.py module
- • Implement functions to fetch current weather
- • Implement functions to fetch forecast
- • Add error handling for network issues
- • Implement request caching

#### Step 4: Data Processing Module
- • Create weather_parser.py module
- • Parse JSON responses into usable data
- • Convert temperatures between units
- • Format dates and times properly
- • Create weather condition icons/mappings

#### Step 5: Display Module
- • Create weather_display.py module
- • Format weather data for display
- • Create ASCII art for weather conditions
- • Implement color-coded temperature display
- • Create forecast display with daily summaries

#### Step 6: User Interface
- • Build interactive menu system
- • Implement city search with validation
- • Add settings for units and display options
- • Create help system and documentation
- • Add favorite cities feature

#### Step 7: Advanced Features
- • Add weather alerts and warnings
- • Implement historical weather data
- • Add location detection by IP
- • Create weather data export to CSV
- • Add weather comparison between cities

---

### Verbatim Numbered List (Items 1–46)

```text
1. Step 1: API Setup & Exploration
2. • Sign up for free API key from OpenWeatherMap or similar
3. • Explore API documentation and test endpoints
4. • Understand the JSON response structure
5. • Set up environment variables for API key
6. 
7. Step 2: Project Structure
8. • Create project folder with modular structure
9. • Set up requirements.txt with dependencies
10. • Create configuration file for API settings
11. • Set up .env file for sensitive data
12. 
13. Step 3: API Client Module
14. • Create weather_api.py module
15. • Implement functions to fetch current weather
16. • Implement functions to fetch forecast
17. • Add error handling for network issues
18. • Implement request caching
19. 
20. Step 4: Data Processing Module
21. • Create weather_parser.py module
22. • Parse JSON responses into usable data
23. • Convert temperatures between units
24. • Format dates and times properly
25. • Create weather condition icons/mappings
26. 
27. Step 5: Display Module
28. • Create weather_display.py module
29. • Format weather data for display
30. • Create ASCII art for weather conditions
31. • Implement color-coded temperature display
32. • Create forecast display with daily summaries
33. 
34. Step 6: User Interface
35. • Build interactive menu system
36. • Implement city search with validation
37. • Add settings for units and display options
38. • Create help system and documentation
39. • Add favorite cities feature
40. 
41. Step 7: Advanced Features
42. • Add weather alerts and warnings
43. • Implement historical weather data
44. • Add location detection by IP
45. • Create weather data export to CSV
46. • Add weather comparison between cities
```

---

## 💻 Sample Code: `weather_api.py`

### Complete & Functional Code
*(This version provides the full implementation with completed lines where horizontal overflow occurred in the screenshot)*

```python
# weather_api.py
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import time
from typing import Optional, Dict, Any

class WeatherAPI:
    """Handles all weather API interactions"""

    def __init__(self, api_key: str, base_url: str = "http://api.openweathermap.org/data/2.5"):
        self.api_key = api_key
        self.base_url = base_url
        self.cache_dir = Path("data/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_duration = 600  # 10 minutes in seconds

    def _get_cached_data(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get data from cache if valid"""
        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            # Check if cache is still valid
            cache_time = cache_file.stat().st_mtime
            if time.time() - cache_time < self.cache_duration:
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except:
                    pass
        return None

    def _save_to_cache(self, cache_key: str, data: Dict):
        """Save data to cache"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass

    def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict[str, Any]]:
        """Make API request with error handling"""
        try:
            params['appid'] = self.api_key
            params['units'] = 'metric'  # Use metric units

            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                print("Error: Invalid API key")
            elif response.status_code == 404:
                print("Error: City not found")
            elif response.status_code == 429:
                print("Error: API rate limit exceeded")
            else:
                print(f"Error: API request failed with status code {response.status_code}")

        except requests.exceptions.Timeout:
            print("Error: Request timed out")
        except requests.exceptions.ConnectionError:
            print("Error: Network connection error")
        except Exception as e:
            print(f"Error: {e}")

        return None

    def get_current_weather(self, city: str, country_code: str = "") -> Optional[Dict[str, Any]]:
        """Get current weather for a city"""
        cache_key = f"current_{city}_{country_code}" if country_code else f"current_{city}"

        # Check cache first
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data

        # Build query
        query = city
        if country_code:
            query = f"{city},{country_code}"

        # Make API request
        params = {'q': query}
        data = self._make_request("weather", params)

        if data:
            self._save_to_cache(cache_key, data)

        return data
```

### Exact Visible Text (Screenshot Verbatim)
*(Raw characters exactly as visible within the right-edge viewport cutoff of the mobile screenshot)*

```python
# weather_api.py
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import time
from typing import Optional, Dict, Any

class WeatherAPI:
    """Handles all weather API interactions"""

    def __init__(self, api_key: str, base_url: str = "http:/
        self.api_key = api_key
        self.base_url = base_url
        self.cache_dir = Path("data/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_duration = 600  # 10 minutes in seconds

    def _get_cached_data(self, cache_key: str) -> Optional[D
        """Get data from cache if valid"""
        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            # Check if cache is still valid
            cache_time = cache_file.stat().st_mtime
            if time.time() - cache_time < self.cache_duratio
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except:
                    pass
        return None

    def _save_to_cache(self, cache_key: str, data: Dict):
        """Save data to cache"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass

    def _make_request(self, endpoint: str, params: Dict) ->
        """Make API request with error handling"""
        try:
            params['appid'] = self.api_key
            params['units'] = 'metric'  # Use metric units

            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                print("Error: Invalid API key")
            elif response.status_code == 404:
                print("Error: City not found")
            elif response.status_code == 429:
                print("Error: API rate limit exceeded")
            else:
                print(f"Error: API request failed with statu

        except requests.exceptions.Timeout:
            print("Error: Request timed out")
        except requests.exceptions.ConnectionError:
            print("Error: Network connection error")
        except Exception as e:
            print(f"Error: {e}")

        return None

    def get_current_weather(self, city: str, country_code: s
        """Get current weather for a city"""
        cache_key = f"current_{city}_{country_code}" if coun

        # Check cache first
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data

        # Build query
        query = city
        if country_code:
            query = f"{city},{country_code}"

        # Make API request
        params = {'q': query}
        data = self._make_request("weather", params)

        if data:
            self._save_to_cache(cache_key, data)

        return data
```

---

## 📊 Sample Output:

```text
🌤️  WEATHER DASHBOARD
======================

📍 Current Location: London, GB
🕒 Last Updated: 2024-01-25 10:15:00

Current Weather:
----------------
Temperature:  8°C (Feels like: 5°C)
Conditions:   Light rain 🌧️
Humidity:     87%
Wind:         22 km/h from SW
Pressure:     1009 hPa
Visibility:   8 km
Sunrise:      07:45
Sunset:       16:30

5-Day Forecast:
----------------
Thu 25 Jan:  🌧️   9°C / 6°C  (Humidity: 85%)
Fri 26 Jan:  ☁️   8°C / 4°C  (Humidity: 78%)
Sat 27 Jan:  ⛅   7°C / 3°C  (Humidity: 75%)
Sun 28 Jan:  ☀️   9°C / 4°C  (Humidity: 70%)
Mon 29 Jan:  ☀️  10°C / 5°C  (Humidity: 68%)

API Status: Using cached data (5 minutes old)
Type 'refresh' to update, 'search' for new city, or 'q
```

---

## 📥 Submission Requirements:

### GitHub Structure:

```text
week6-weather-dashboard/
├── weather_app/
│   ├── __init__.py
│   ├── config.py
│   ├── weather_api.py
│   ├── weather_parser.py
│   ├── weather_display.py
│   └── main.py
├── data/
│   ├── cache/
│   └── favorites.json
├── tests/
│   ├── test_api.py
│   ├── test_parser.py
│   └── test_display.py
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

#### Exact List Representation:
- • week6-weather-dashboard/
- • |—— weather_app/
- • |   |—— __init__.py
- • |   |—— config.py
- • |   |—— weather_api.py
- • |   |—— weather_parser.py
- • |   |—— weather_display.py
- • |   └── main.py
- • |—— data/
- • |   |—— cache/
- • |   └── favorites.json
- • |—— tests/
- • |   |—— test_api.py
- • |   |—— test_parser.py
- • |   └── test_display.py
- • |—— requirements.txt
- • |—— .env.example
- • |—— README.md
- • └── .gitignore
