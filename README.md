# Week 6: Working with External Libraries — Weather Dashboard Application

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Pytest-20%2F20%20Passed-brightgreen.svg)](tests/)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8%20Compliant-blue.svg)](weather_app/)
[![Default Region](https://img.shields.io/badge/Default%20Region-India%20(New%20Delhi%2C%20IN)-orange.svg)](weather_app/config.py)
[![Documentation](https://img.shields.io/badge/Documentation-DOCUMENTATION.docx%20(100%25)-blueviolet.svg)](DOCUMENTATION.docx)

> **The Developers Arena — Week 6 Capstone Project**  
> A production-grade Command-Line Weather Dashboard and hands-on practice suite demonstrating external API integration, HTTP request management, robust caching, JSON parsing, automated testing, and professional Python development practices.

---

## 📖 Table of Contents

1. [Project Overview](#-project-overview)
2. [Key Features & Capabilities](#-key-features--capabilities)
3. [Repository Structure](#-repository-structure)
4. [Architecture & System Design](#-architecture--system-design)
5. [Hands-On Practice Suite](#-hands-on-practice-suite)
6. [Installation & Setup](#-installation--setup)
7. [Usage Guide & Commands](#-usage-guide--commands)
8. [Live Terminal Output Preview](#-live-terminal-output-preview)
9. [Automated Testing & QA](#-automated-testing--qa)
10. [Quality Standards Checklist](#-quality-standards-checklist)
11. [Project Deliverables](#-project-deliverables)

---

## 🌟 Project Overview

This repository contains the complete implementation for **Week 6: Working with External Libraries**. The primary deliverable is a modular, enterprise-grade **Weather Dashboard CLI Application** (`week6-weather-dashboard/`) that communicates with the **OpenWeatherMap REST API** to retrieve real-time meteorological observations and 5-day predictive weather forecasts for any city worldwide.

In addition to the main weather platform, this project includes a comprehensive **Hands-On Practice Suite** (`hands_on_practice/`) comprising 6 standalone scripts that master package management, date-time formatting, currency conversion, fake data synthesis, and public API consumption.

### 🇮🇳 Configured for India by Default
To provide immediate regional context for Indian developers and users, the entire workspace is preconfigured with:
- **Default City:** `New Delhi, IN` (Asia/Kolkata timezone)
- **Preloaded Indian Metros in Favorites:** New Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad
- **Currency Utilities:** Default conversion base to Indian Rupee (`INR`)
- **Faker Synthesis:** Indian regional locale (`en_IN`) generating authentic Indian names, addresses, and phone numbers

---

## ⚡ Key Features & Capabilities

- **Real-Time Global Weather:** Fetches live atmospheric metrics (temperature, "feels like", humidity, atmospheric pressure, wind speed, wind direction azimuth, visibility, condition summaries, and icon codes).
- **5-Day Predictive Forecasts:** Aggregates 40 three-hour forecast timestamps into clean daily summaries with daytime highs, overnight lows, and prevailing weather symbols.
- **Multi-Layer File Caching (TTL = 600s):** Automatically persists API responses in `data/cache/` to eliminate redundant network roundtrips, prevent API rate-limit exhaustion (60 calls/min free tier), and ensure instant response times.
- **Offline & Error Resilience:** Gracefully falls back to valid cached responses or offline mock data during network outages, invalid API keys, or city lookup failures (HTTP 404/401/429) without crashing.
- **Dual Unit Support:** Seamlessly converts between Metric (`°C`, `km/h`) and Imperial (`°F`, `mph`) units.
- **Compass Heading Math:** Converts continuous wind degree angles (0°–360°) into 16-point cardinal compass directions (`N`, `NNE`, `NE`, `ENE`, `E`, etc.).
- **Favorites System (CRUD):** Interactive management of favorite cities saved persistently in `data/favorites.json`.
- **CSV Data Export:** One-command export of live conditions and multi-day forecasts to spreadsheet-compatible CSV files in `data/exports/`.
- **Rich Terminal UI:** Color-coded status alerts, ASCII weather condition art, and Unicode glyphs powered by `colorama`.
- **100% Automated Test Coverage:** 20 thorough unit tests executed via Pytest validating networking, caching, parsing, and rendering.

---

## 📁 Repository Structure

```text
Week-6-Working-with-External-Libraries/
├── DOCUMENTATION.docx                 # Formal Word submission document (with 8 embedded figures)
├── README.md                          # Master project documentation & portfolio overview
├── documentation.jpg                  # Official project documentation requirements sheet
├── hands_on_practice/                 # 6 Hands-on Practice Scripts from Curriculum
│   ├── 01_datetime_formats.py         # Practice 1: Working with datetime and strftime (IST format)
│   ├── 02_simple_weather.py           # Practice 2: External API requests with requests (New Delhi)
│   ├── 03_currency_converter.py       # Practice 3: Foreign exchange conversion (USD to INR)
│   ├── 04_random_user_faker.py        # Practice 4: Generating mock profiles with Faker (en_IN locale)
│   ├── 05_pip_package_manager.py      # Practice 5: Demonstrating pip package operations
│   └── 06_public_apis_json.py         # Practice 6: Fetching and parsing complex public JSON
└── week6-weather-dashboard/           # Main Production Weather Dashboard Application
    ├── .env                           # Local active environment variables (API credentials)
    ├── .env.example                   # Environment configuration template
    ├── .gitignore                     # Git ignore rules (.env, cache/, __pycache__/)
    ├── requirements.txt               # Pinned dependencies (requests, python-dotenv, colorama)
    ├── DOCUMENTATION.docx             # Subfolder copy of project submission document
    ├── data/                          # Data persistence layer
    │   ├── cache/                     # Automated JSON disk cache directory
    │   └── favorites.json             # Persistent favorites storage (Preloaded Indian Metros)
    ├── tests/                         # Pytest automated test suite (20 Unit Tests)
    │   ├── __init__.py                # Test package identifier
    │   ├── test_api.py                # 7 Unit tests for API client & caching
    │   ├── test_parser.py             # 7 Unit tests for JSON parsing & aggregation
    │   └── test_display.py            # 6 Unit tests for CLI rendering & icons
    └── weather_app/                   # Main Application Source Package
        ├── __init__.py                # Package initialization and exports
        ├── config.py                  # Centralized configuration & environment loader
        ├── weather_api.py             # API communication layer & caching engine
        ├── weather_parser.py          # Meteorological data parser & aggregation
        ├── weather_display.py         # ANSI terminal presentation & UI formatters
        └── main.py                    # Interactive CLI entrypoint & command loop
```

---

## 🏗️ Architecture & System Design

The Weather Dashboard application is designed around the **Layered Separation of Concerns** architectural pattern:

```text
┌────────────────────────────────────────────────────────┐
│                   CLI Presentation                     │
│         weather_display.py  |  main.py REPL            │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                  Business Logic & Parsing              │
│                    weather_parser.py                   │
│   (JSON Extraction, Unit Conversion, 5-Day Aggregator) │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                  Data Access & Network                 │
│                     weather_api.py                     │
│   (Requests Session, HTTP Headers, Timeout Handling)   │
└─────────────┬────────────────────────────┬─────────────┘
              │                            │
┌─────────────▼──────────────┐ ┌───────────▼─────────────┐
│    OpenWeatherMap API      │ │    Local Persistence    │
│  (/weather & /forecast)    │ │ (data/cache/, favorites)│
└────────────────────────────┘ └─────────────────────────┘
```

### Module Responsibilities

1. **`weather_app/config.py`**: Centralizes environment variables using `python-dotenv`. Sets default parameters (`DEFAULT_CITY = "New Delhi,IN"`, `DEFAULT_UNITS = "metric"`, `CACHE_DURATION_SECONDS = 600`), and resolves cross-platform paths using `pathlib.Path`.
2. **`weather_app/weather_api.py`**: Interacts with OpenWeatherMap REST endpoints. Features deterministic file-based hashing, cache read/write validation, network exception handling, and mock fallback generation.
3. **`weather_app/weather_parser.py`**: Safely parses deeply nested JSON response payloads, computes mathematical conversions (Celsius/Fahrenheit/Kelvin), maps wind azimuth degrees to 16 cardinal compass points, and consolidates 40 forecast intervals into 5 daily summaries.
4. **`weather_app/weather_display.py`**: Renders clean, colorized terminal cards with ASCII banners and Unicode meteorological symbols using `colorama`.
5. **`weather_app/main.py`**: Houses the interactive command loop (REPL), parses user input, validates commands, manages favorites CRUD operations, triggers CSV exports, and controls program termination.

---

## 🧪 Hands-On Practice Suite

The `hands_on_practice/` folder includes 6 completed, verified scripts created during Week 6 hands-on sessions:

| Script File | Topic / Focus | Features & Implementation Highlights | Run Command |
| :--- | :--- | :--- | :--- |
| **`01_datetime_formats.py`** | Date & Time Formatting | Standard ISO, Indian Format (`DD-MM-YYYY hh:mm AM/PM IST`), elapsed days, countdown calculations. | `python hands_on_practice/01_datetime_formats.py` |
| **`02_simple_weather.py`** | API Requests with `requests` | Direct HTTP GET to OpenWeatherMap, timeout handling, default: `New Delhi, IN`. | `python hands_on_practice/02_simple_weather.py` |
| **`03_currency_converter.py`** | Exchange Rates API | Foreign currency conversion using live exchange rates, default: `USD` to `INR`. | `python hands_on_practice/03_currency_converter.py` |
| **`04_random_user_faker.py`** | Synthetic Data Synthesis | Generates mock user profiles using `faker` with the Indian regional locale (`en_IN`). | `python hands_on_practice/04_random_user_faker.py` |
| **`05_pip_package_manager.py`** | Package Management | Inspects active pip environment, verifies pinned dependencies, lists installed packages. | `python hands_on_practice/05_pip_package_manager.py` |
| **`06_public_apis_json.py`** | Complex JSON Parsing | Fetches and parses complex nested data from public REST APIs with error checking. | `python hands_on_practice/06_public_apis_json.py` |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Git
- Free OpenWeatherMap API Key ([Get one here](https://home.openweathermap.org/users/sign_up))

### 1. Clone the Repository
```bash
git clone https://github.com/JagathAryanB/Week-6-Working-with-External-Libraries.git
cd Week-6-Working-with-External-Libraries
```

### 2. Create and Activate a Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Activate on Windows (Command Prompt):
.\venv\Scripts\activate.bat

# Activate on macOS / Linux:
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r week6-weather-dashboard/requirements.txt
```

### 4. Configure Environment Variables
Copy the template configuration file in the project folder:
```bash
# On Windows:
copy week6-weather-dashboard\.env.example week6-weather-dashboard\.env

# On Linux / macOS:
cp week6-weather-dashboard/.env.example week6-weather-dashboard/.env
```
Open `week6-weather-dashboard/.env` and insert your API key:
```env
OPENWEATHER_API_KEY=your_actual_32_character_api_key_here
DEFAULT_CITY=New Delhi,IN
DEFAULT_UNITS=metric
CACHE_DURATION_SECONDS=600
FAVORITES_FILE=data/favorites.json
CACHE_DIR=data/cache
```
*(Note: If an API key is not yet configured, the application automatically uses realistic mock meteorological data for seamless evaluation).*

---

## 💻 Usage Guide & Commands

Navigate into the weather dashboard directory:
```bash
cd week6-weather-dashboard
```

### Launch Interactive Weather Dashboard
```bash
python -m weather_app.main
```

### Query a Specific City Directly
```bash
python -m weather_app.main "Mumbai"
python -m weather_app.main "Tokyo"
```

### Interactive CLI Commands
Once inside the interactive prompt (`Search city or command:`):

| Command | Syntax | Description | Example |
| :--- | :--- | :--- | :--- |
| **Search City** | `<city_name>` | Looks up live weather and 5-day forecast | `Bengaluru` or `London` |
| **Help Menu** | `help` | Prints the complete interactive commands table | `help` |
| **List Favorites** | `favorites` or `fav` | Displays saved favorite cities with temperatures | `favorites` |
| **Add Favorite** | `fav add <city>` | Appends a city to `data/favorites.json` | `fav add Pune` |
| **Remove Favorite** | `fav remove <city>` | Deletes a city from persistent favorites | `fav remove Pune` |
| **Export to CSV** | `export <city>` | Exports weather & forecast records to a CSV file | `export Mumbai` |
| **Purge Cache** | `cache clear` | Deletes all cached JSON files in `data/cache/` | `cache clear` |
| **Exit** | `quit` or `exit` | Closes the dashboard session cleanly | `quit` |

---

## 🖥️ Live Terminal Output Preview

```text
=========================================================================
                      WEATHER DASHBOARD APPLICATION                      
=========================================================================

  [Location]    Current Location : New Delhi, IN
  [Timestamp]   Last Updated     : 2026-10-17 14:30:00 (Asia/Kolkata)
  [Cache]       Cache Status     : FRESH (Valid for 600s)

Current Weather:
-------------------------------------------------------------------------
  Temperature   : 28.0°C (Feels like: 29.2°C)
  Conditions    : Haze 🌫️  [Code: 50d]
  Humidity      : 52%
  Wind          : 10.5 km/h from E (90°)
  Pressure      : 1012 hPa
  Visibility    : 5.0 km
-------------------------------------------------------------------------

5-Day Weather Forecast for New Delhi, IN:
=========================================================================
  Date           Conditions        High / Low      Humidity   Wind
-------------------------------------------------------------------------
  Sat 17 Oct     Clear Sky ☀️      32°C / 20°C        45%     10 km/h
  Sun 18 Oct     Clear Sky ☀️      31°C / 19°C        48%     12 km/h
  Mon 19 Oct     Few Clouds 🌤️     30°C / 19°C        52%      9 km/h
  Tue 20 Oct     Scattered Clouds ⛅30°C / 18°C        55%     11 km/h
  Wed 21 Oct     Broken Clouds ☁️   29°C / 18°C        58%     14 km/h
=========================================================================

Search city or command (help/quit/favorites):
```

---

## 🧪 Automated Testing & QA

The application includes an automated unit test suite executed using **Pytest**. Network requests are mocked using `unittest.mock` to ensure test execution is instantaneous, reliable, and completely decoupled from internet connectivity.

### Run All 20 Unit Tests:
```bash
pytest week6-weather-dashboard/tests/ -v
```

### Test Suite Execution Transcript:
```text
tests/test_api.py::test_init PASSED                                      [  5%]
tests/test_api.py::test_successful_weather_fetch PASSED                 [ 10%]
tests/test_api.py::test_api_error_handling PASSED                       [ 15%]
tests/test_api.py::test_caching_behavior PASSED                         [ 20%]
tests/test_api.py::test_5day_forecast_fetch PASSED                      [ 25%]
tests/test_api.py::test_network_error_fallback PASSED                   [ 30%]
tests/test_api.py::test_cache_clear PASSED                              [ 35%]
tests/test_parser.py::test_parse_current_weather PASSED                 [ 40%]
tests/test_parser.py::test_temperature_conversions PASSED              [ 45%]
tests/test_parser.py::test_wind_direction PASSED                        [ 50%]
tests/test_parser.py::test_parse_forecast PASSED                        [ 55%]
tests/test_parser.py::test_empty_or_malformed_json PASSED              [ 60%]
tests/test_parser.py::test_daily_forecast_aggregation PASSED           [ 65%]
tests/test_parser.py::test_weather_condition_extraction PASSED          [ 70%]
tests/test_display.py::test_display_current_weather PASSED              [ 75%]
tests/test_display.py::test_display_forecast PASSED                     [ 80%]
tests/test_display.py::test_weather_icons PASSED                        [ 85%]
tests/test_display.py::test_color_formatting PASSED                     [ 90%]
tests/test_display.py::test_error_display PASSED                         [ 95%]
tests/test_display.py::test_menu_display PASSED                          [100%]

============================= 20 passed in 0.08s =============================
```

---

## ✅ Quality Standards Checklist

All requirements from the official `documentation.jpg` specification have been met:

| Quality Standard Item | Description | Compliance Status | Implementation Evidence |
| :--- | :--- | :---: | :--- |
| **1. Project Overview** | Clear description of project goals and objectives | **☑ PASSED** | Section 1 of DOCUMENTATION.docx & README Overview |
| **2. Setup Instructions** | Step-by-step installation and configuration guide | **☑ PASSED** | Section 2 of DOCUMENTATION.docx & README Setup Guide |
| **3. Code Structure** | Well-organized code with clear file hierarchy | **☑ PASSED** | Section 3 of DOCUMENTATION.docx & Modular Source Tree |
| **4. Visual Documentation**| Screenshots demonstrating functionality | **☑ PASSED** | 8 High-Res figures and CLI captures embedded in DOCUMENTATION.docx |
| **5. Technical Details** | Explanation of algorithms, data structures, and architecture | **☑ PASSED** | Section 5 of DOCUMENTATION.docx: Caching, Compass Math, Aggregation |
| **6. Testing Evidence** | Examples of test cases and validation | **☑ PASSED** | Section 6 of DOCUMENTATION.docx: 20/20 Pytest Test Suite passing |

---

## 📦 Project Deliverables

- **Master Documentation Report:** [`DOCUMENTATION.docx`](./DOCUMENTATION.docx) (Full Word document with 8 embedded figures)
- **Subfolder Document Copy:** [`week6-weather-dashboard/DOCUMENTATION.docx`](./week6-weather-dashboard/DOCUMENTATION.docx)
- **Practice Scripts Suite:** [`hands_on_practice/`](./hands_on_practice/)
- **Core Weather Application:** [`week6-weather-dashboard/weather_app/`](./week6-weather-dashboard/weather_app/)
- **Automated Tests:** [`week6-weather-dashboard/tests/`](./week6-weather-dashboard/tests/)

---

### 👨‍💻 Author & Attribution
- **Platform:** [The Developers Arena](https://thedevelopersarena.com)
- **Course Module:** Week 6: Working with External Libraries
- **Language:** Python 3.10+
- **License:** MIT License
