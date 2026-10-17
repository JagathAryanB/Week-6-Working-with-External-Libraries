import json
import os
from pathlib import Path
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from .config import Config
from .weather_api import WeatherAPI
from .weather_parser import WeatherParser
from .weather_display import WeatherDisplay

class WeatherApp:

    def __init__(self):
        Config.ensure_directories()
        self.api = WeatherAPI(
            api_key=Config.API_KEY,
            base_url=Config.BASE_URL,
            cache_dir=Config.CACHE_DIR,
            cache_duration=Config.CACHE_DURATION
        )
        self.current_city = Config.DEFAULT_CITY
        self.units = Config.DEFAULT_UNITS
        self.favorites = self.load_favorites()

    def load_favorites(self):
        try:
            if Config.FAVORITES_FILE.exists():
                with open(Config.FAVORITES_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return ["New Delhi", "Mumbai", "Bengaluru", "Kolkata", "Chennai"]

    def save_favorites(self):
        try:
            with open(Config.FAVORITES_FILE, "w", encoding="utf-8") as f:
                json.dump(self.favorites, f, indent=2)
        except Exception as e:
            print(f"Error saving favorites: {e}")

    def show_dashboard(self, city=None):
        if city:
            self.current_city = city

        raw_current = self.api.get_current_weather(self.current_city)
        raw_forecast = self.api.get_forecast(self.current_city)

        parsed_current = WeatherParser.parse_current_weather(raw_current, self.units)
        parsed_forecast = WeatherParser.parse_forecast(raw_forecast, self.units)

        if parsed_current.get("cached"):
            cache_info = f"Using cached data ({Config.CACHE_DURATION // 60} minutes old)"
        else:
            cache_info = "Live data fetched from API"

        WeatherDisplay.display_ascii_art_banner(parsed_current.get("condition_text", "clear"))
        WeatherDisplay.display_full_dashboard(parsed_current, parsed_forecast, cache_info)

    def search_city_interactive(self):
        print("\n--- City Search ---")
        query = input("Enter city name (or prefix to autocomplete): ").strip()
        if not query:
            print("Search cancelled.")
            return

        suggestions = self.api.search_cities(query)
        print("\nMatching suggestions:")
        for idx, s in enumerate(suggestions, 1):
            print(f"  [{idx}] {s}")
        print(f"  [{len(suggestions) + 1}] Use exact entered text: '{query}'")

        choice = input(f"Select option (1-{len(suggestions) + 1}) [1]: ").strip()
        if not choice:
            selected = suggestions[0].split(",")[0].strip()
        elif choice.isdigit() and 1 <= int(choice) <= len(suggestions):
            selected = suggestions[int(choice) - 1].split(",")[0].strip()
        else:
            selected = query

        self.show_dashboard(selected)

    def detect_ip_location(self):
        print("\nDetecting your current location via IP...")
        geo = self.api.detect_location_by_ip()
        detected_city = geo.get("city", "London")
        print(f"Detected Location: {detected_city}, {geo.get('country', '')}")
        self.show_dashboard(detected_city)

    def compare_cities_interactive(self):
        print("\n--- Weather Comparison ---")
        city1 = input(f"Enter first city [{self.current_city}]: ").strip() or self.current_city
        city2 = input("Enter second city [Mumbai]: ").strip() or "Mumbai"

        raw1 = self.api.get_current_weather(city1)
        raw2 = self.api.get_current_weather(city2)

        p1 = WeatherParser.parse_current_weather(raw1, self.units)
        p2 = WeatherParser.parse_current_weather(raw2, self.units)

        WeatherDisplay.display_comparison(p1, p2)

    def manage_favorites_interactive(self):
        print("\n--- Favorite Cities Management ---")
        print("Current Favorites:")
        for idx, fav in enumerate(self.favorites, 1):
            print(f"  [{idx}] {fav}")
        print("\nOptions: (A)dd city, (R)emove city, (V)iew city weather, (B)ack")
        choice = input("Select an option [B]: ").strip().upper()

        if choice == "A":
            new_city = input("Enter city name to add: ").strip()
            if new_city and new_city not in self.favorites:
                self.favorites.append(new_city)
                self.save_favorites()
                print(f"Added '{new_city}' to favorites.")
        elif choice == "R":
            target = input("Enter city name or number to remove: ").strip()
            if target.isdigit() and 1 <= int(target) <= len(self.favorites):
                removed = self.favorites.pop(int(target) - 1)
                self.save_favorites()
                print(f"Removed '{removed}' from favorites.")
            elif target in self.favorites:
                self.favorites.remove(target)
                self.save_favorites()
                print(f"Removed '{target}' from favorites.")
        elif choice == "V":
            target = input("Enter favorite number to view: ").strip()
            if target.isdigit() and 1 <= int(target) <= len(self.favorites):
                self.show_dashboard(self.favorites[int(target) - 1])

    def show_alerts(self):
        print(f"\n--- Weather Alerts & Warnings for {self.current_city} ---")
        raw_current = self.api.get_current_weather(self.current_city)
        parsed = WeatherParser.parse_current_weather(raw_current, self.units)
        temp_val = parsed.get("temp_raw", 15.0)

        alerts = []
        if temp_val < 0:
            alerts.append("⚠️ FREEZING ALERT: Sub-zero temperatures detected. Watch for black ice.")
        elif temp_val > 35:
            alerts.append("🔥 HEAT ADVISORY: Extreme heat warning. Stay hydrated and avoid prolonged sun exposure.")

        if "rain" in parsed.get("condition_text", "").lower():
            alerts.append("🌧️ PRECIPITATION NOTICE: Wet roads and reduced visibility expected.")
        elif "thunder" in parsed.get("condition_text", "").lower():
            alerts.append("⛈️ SEVERE THUNDERSTORM WARNING: Lightning and gusty winds in the vicinity.")
        elif "snow" in parsed.get("condition_text", "").lower():
            alerts.append("❄️ WINTER WEATHER WARNING: Snow accumulation may affect travel.")

        if not alerts:
            alerts.append("✅ No active severe weather warnings for this location. Conditions are normal.")

        for a in alerts:
            print("  " + a)
        print("-" * 55)

    def show_history(self):
        history_records = self.api.get_historical_weather(self.current_city, days=5)
        WeatherDisplay.display_historical_table(self.current_city, history_records, self.units)

    def export_csv(self):
        raw_current = self.api.get_current_weather(self.current_city)
        raw_forecast = self.api.get_forecast(self.current_city)
        parsed_forecast = WeatherParser.parse_forecast(raw_forecast, self.units)

        filename = f"weather_export_{self.current_city.lower().replace(' ', '_')}.csv"
        out_path = Config.EXPORTS_DIR / filename
        success = self.api.export_weather_to_csv(raw_current, parsed_forecast, out_path)
        if success:
            print(f"\nSuccessfully exported weather data to: {out_path.resolve()}")
        else:
            print("\nFailed to export weather data.")

    def toggle_units(self):
        self.units = "imperial" if self.units == "metric" else "metric"
        print(f"\nSwitched temperature units to: {self.units.upper()}")
        self.show_dashboard()

    def run_menu(self):
        self.show_dashboard()

        while True:
            cmd = input("Command (refresh / search / compare / favorites / detect / alerts / history / export / units / help / q): ").strip().lower()

            if cmd in ["q", "quit", "exit"]:
                print("Goodbye!")
                break
            elif cmd in ["refresh", "r", ""]:
                self.show_dashboard()
            elif cmd in ["search", "s"]:
                self.search_city_interactive()
            elif cmd in ["detect", "ip", "location"]:
                self.detect_ip_location()
            elif cmd in ["compare", "c"]:
                self.compare_cities_interactive()
            elif cmd in ["favorites", "fav", "f"]:
                self.manage_favorites_interactive()
            elif cmd in ["alerts", "a", "warning"]:
                self.show_alerts()
            elif cmd in ["history", "hist", "h"]:
                self.show_history()
            elif cmd in ["export", "csv"]:
                self.export_csv()
            elif cmd in ["units", "u"]:
                self.toggle_units()
            elif cmd in ["help", "?"]:
                WeatherDisplay.display_help()
            else:
                self.show_dashboard(cmd)

def main():
    app = WeatherApp()
    if len(sys.argv) > 1:
        initial_city = sys.argv[1].strip()
        app.show_dashboard(initial_city)
        if "--interactive" in sys.argv:
            app.run_menu()
    else:
        app.run_menu()

if __name__ == "__main__":
    main()
