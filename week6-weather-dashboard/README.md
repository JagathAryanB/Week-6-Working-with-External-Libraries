# Week 6: Weather Dashboard Application

A modular Command-Line Weather Dashboard built with Python, integrating with the OpenWeatherMap API, featuring local JSON response caching, 5-day forecasts, color-coded temperature displays, ASCII weather art, IP-based geolocation, city comparisons, and CSV data exports.

---

## Project Structure

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

---

## Features

- **Current Weather Worldwide:** Real-time temperature, "feels like", humidity, wind speed & direction, pressure, visibility, sunrise, and sunset.
- **5-Day Weather Forecast:** Daily summary forecasts with temperature ranges, expected condition icons, and humidity.
- **Response Caching:** Automatic 10-minute file-based JSON caching to reduce redundant network calls.
- **City Search with Autocomplete:** Fast lookup for worldwide cities with input validation.
- **Auto Location Detection:** Automatically detects current city and country using IP geolocation.
- **Weather Comparison:** Side-by-side comparison of current weather metrics between any two cities.
- **Favorites System:** Save and manage favorite locations stored in `data/favorites.json`.
- **Weather Alerts & Warnings:** Automatic warnings for freezing temperatures, extreme heat, rain, and storms.
- **Historical Weather:** Multi-day historical records table.
- **CSV Data Export:** Exports structured current and forecast weather records to CSV in `data/exports/`.
- **Visual Terminal UI:** ASCII art condition banners and color-coded temperature ratings using `colorama`.

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd week6-weather-dashboard
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Add your OpenWeatherMap API key in `.env`:
   ```env
   OPENWEATHER_API_KEY=your_key_here
   ```
   *(Note: The app includes built-in fallback data if an API key is not yet configured, allowing full demonstration right out of the box).*

---

## Usage

### Run the Interactive Weather Dashboard:
```bash
python -m weather_app.main
```

### View Weather for a Specific City directly:
```bash
python -m weather_app.main "Tokyo"
```

### Run All Unit Tests:
```bash
pytest tests/ -v
# Or with standard unittest:
python -m unittest discover tests/
```
