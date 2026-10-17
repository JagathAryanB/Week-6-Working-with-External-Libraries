import sys
from typing import Dict, Any, List
from colorama import Fore, Style, init

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

init(autoreset=True)

class WeatherDisplay:

    ASCII_ART = {
        "sun": [
            r"   \   /   ",
            r"     .-.   ",
            r"  ― (   ) ―",
            r"     `-’   ",
            r"   /   \   "
        ],
        "clouds": [
            r"     .--.   ",
            r"  .-(    ). ",
            r" (___.__)__)"
        ],
        "rain": [
            r"     .-.    ",
            r"    (   ).  ",
            r"   (___(__) ",
            r"    ' ' ' ' ",
            r"   ' ' ' '  "
        ],
        "thunderstorm": [
            r"     .-.    ",
            r"    (   ).  ",
            r"   (___(__) ",
            r"    ⚡  ⚡   ",
            r"    ' ' ' ' "
        ],
        "snow": [
            r"     .-.    ",
            r"    (   ).  ",
            r"   (___(__) ",
            r"    *  *  * ",
            r"   *  *  *  "
        ]
    }

    @staticmethod
    def get_temperature_color(temp_c: float) -> str:
        if temp_c <= 0:
            return Fore.CYAN + Style.BRIGHT
        elif temp_c <= 12:
            return Fore.BLUE + Style.BRIGHT
        elif temp_c <= 22:
            return Fore.GREEN + Style.BRIGHT
        elif temp_c <= 30:
            return Fore.YELLOW + Style.BRIGHT
        else:
            return Fore.RED + Style.BRIGHT

    @classmethod
    def get_ascii_art(cls, condition_text: str) -> List[str]:
        text = condition_text.lower()
        if "thunder" in text:
            return cls.ASCII_ART["thunderstorm"]
        elif "rain" in text or "drizzle" in text:
            return cls.ASCII_ART["rain"]
        elif "snow" in text or "ice" in text:
            return cls.ASCII_ART["snow"]
        elif "cloud" in text or "overcast" in text:
            return cls.ASCII_ART["clouds"]
        else:
            return cls.ASCII_ART["sun"]

    @classmethod
    def display_full_dashboard(cls, current: Dict[str, Any], forecast: List[Dict[str, Any]], cache_info: str = "Live data from API"):
        if not current:
            print("No weather data available to display.")
            return

        loc_str = f"{current.get('city', 'Unknown')}, {current.get('country', '')}".strip(", ")
        temp_color = cls.get_temperature_color(current.get("temp_raw", 15.0))
        
        print("\n" + Fore.YELLOW + Style.BRIGHT + "🌤️  WEATHER DASHBOARD")
        print("=" * 22)
        print(f"\n📍 Current Location: {Fore.WHITE + Style.BRIGHT}{loc_str}")
        print(f"🕒 Last Updated: {current.get('updated_at')}")

        print("\nCurrent Weather:")
        print("----------------")
        print(f"Temperature:  {temp_color}{current.get('temp')} (Feels like: {current.get('feels_like')})")
        print(f"Conditions:   {current.get('conditions')}")
        print(f"Humidity:     {current.get('humidity')}")
        print(f"Wind:         {current.get('wind')}")
        print(f"Pressure:     {current.get('pressure')}")
        print(f"Visibility:   {current.get('visibility')}")
        print(f"Sunrise:      {current.get('sunrise')}")
        print(f"Sunset:       {current.get('sunset')}")

        if forecast:
            print("\n5-Day Forecast:")
            print("----------------")
            for item in forecast:
                print(f"{item['day_label']}:  {item['icon']}   {item['temp_max']} / {item['temp_min']}  {item['humidity']}")

        print(f"\nAPI Status: {Fore.CYAN}{cache_info}")
        print("Type 'refresh' to update, 'search' for new city, or 'q' to quit\n")

    @classmethod
    def display_ascii_art_banner(cls, condition_text: str):
        art_lines = cls.get_ascii_art(condition_text)
        print(Fore.CYAN + Style.BRIGHT)
        for line in art_lines:
            print("   " + line)
        print(Style.RESET_ALL)

    @staticmethod
    def display_comparison(city1_data: Dict[str, Any], city2_data: Dict[str, Any]):
        print("\n" + "=" * 65)
        print("WEATHER COMPARISON BETWEEN CITIES")
        print("=" * 65)
        c1 = f"{city1_data.get('city')}, {city1_data.get('country')}"
        c2 = f"{city2_data.get('city')}, {city2_data.get('country')}"
        
        print(f"{'Metric':<20} | {c1:<20} | {c2:<20}")
        print("-" * 65)
        print(f"{'Temperature':<20} | {city1_data.get('temp'):<20} | {city2_data.get('temp'):<20}")
        print(f"{'Feels Like':<20} | {city1_data.get('feels_like'):<20} | {city2_data.get('feels_like'):<20}")
        print(f"{'Conditions':<20} | {city1_data.get('conditions'):<20} | {city2_data.get('conditions'):<20}")
        print(f"{'Humidity':<20} | {city1_data.get('humidity'):<20} | {city2_data.get('humidity'):<20}")
        print(f"{'Wind':<20} | {city1_data.get('wind'):<20} | {city2_data.get('wind'):<20}")
        print(f"{'Pressure':<20} | {city1_data.get('pressure'):<20} | {city2_data.get('pressure'):<20}")
        print(f"{'Visibility':<20} | {city1_data.get('visibility'):<20} | {city2_data.get('visibility'):<20}")
        print("=" * 65 + "\n")

    @staticmethod
    def display_historical_table(city: str, history: List[Dict[str, Any]], units: str = "metric"):
        print("\n" + "=" * 65)
        print(f"HISTORICAL WEATHER FOR {city.upper()} (Past {len(history)} Days)")
        print("=" * 65)
        unit_sym = "°F" if units == "imperial" else "°C"
        print(f"{'Date':<12} | {'Avg Temp':<10} | {'Min Temp':<10} | {'Max Temp':<10} | {'Humidity':<10} | {'Condition':<12}")
        print("-" * 65)
        for h in history:
            print(f"{h['date']:<12} | {h['temp_avg']}{unit_sym:<8} | {h['temp_min']}{unit_sym:<8} | {h['temp_max']}{unit_sym:<8} | {h['humidity']}%{'':<6} | {h['condition']:<12}")
        print("=" * 65 + "\n")

    @staticmethod
    def display_help():
        print("\n" + "=" * 60)
        print("WEATHER DASHBOARD - HELP & DOCUMENTATION")
        print("=" * 60)
        print("Available Commands & Features:")
        print("  1. Dashboard View     : Displays current weather + 5-day forecast.")
        print("  2. City Search        : Search any global city with autocomplete.")
        print("  3. Auto-Detect IP     : Detects your current city via your IP address.")
        print("  4. Compare Cities     : Side-by-side weather comparison.")
        print("  5. Favorite Cities    : Save and quick-access your favorite cities.")
        print("  6. Weather Alerts     : Shows active weather alerts & advisories.")
        print("  7. Historical Weather : View multi-day historical weather records.")
        print("  8. Export to CSV      : Saves current weather & forecast to CSV.")
        print("  9. Settings           : Toggle Celsius/Fahrenheit units & defaults.")
        print(" 10. Cache Management   : Automatic 10-minute caching to minimize API hits.")
        print("=" * 60 + "\n")
