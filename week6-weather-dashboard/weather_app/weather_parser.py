from datetime import datetime, timezone
from typing import Dict, Any, List

class WeatherParser:

    CONDITION_ICONS = {
        "thunderstorm": "⛈️",
        "thunder": "⛈️",
        "heavy intensity rain": "🌧️",
        "moderate rain": "🌧️",
        "light rain": "🌧️",
        "rain": "🌧️",
        "light snow": "❄️",
        "snow": "❄️",
        "few clouds": "🌤️",
        "scattered clouds": "⛅",
        "broken clouds": "☁️",
        "overcast clouds": "☁️",
        "clouds": "☁️",
        "clear": "☀️",
        "sunny": "☀️",
        "mist": "🌫️",
        "fog": "🌫️",
        "haze": "🌫️"
    }

    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        return round((celsius * 9 / 5) + 32, 1)

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        return round((fahrenheit - 32) * 5 / 9, 1)

    @staticmethod
    def format_temperature(temp_celsius: float, unit: str = "metric") -> str:
        if unit == "imperial":
            temp_f = WeatherParser.celsius_to_fahrenheit(temp_celsius)
            return f"{round(temp_f)}°F"
        return f"{round(temp_celsius)}°C"

    @classmethod
    def get_condition_icon(cls, condition_text: str) -> str:
        key = condition_text.lower().strip()
        for cond, icon in cls.CONDITION_ICONS.items():
            if cond in key:
                return icon
        return "🌤️"

    @staticmethod
    def degrees_to_cardinal(degrees: float) -> str:
        directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                      "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        idx = int((degrees + 11.25) / 22.5) % 16
        return directions[idx]

    @staticmethod
    def format_timestamp(timestamp: int, tz_offset: int = 0) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def format_time_only(timestamp: int) -> str:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%H:%M")

    @classmethod
    def parse_current_weather(cls, data: Dict[str, Any], units: str = "metric") -> Dict[str, Any]:
        if not data:
            return {}

        main = data.get("main", {})
        wind = data.get("wind", {})
        weather = data.get("weather", [{}])[0]
        sys_data = data.get("sys", {})

        temp_c = main.get("temp", 0.0)
        feels_like_c = main.get("feels_like", 0.0)
        temp_min_c = main.get("temp_min", 0.0)
        temp_max_c = main.get("temp_max", 0.0)

        wind_speed_ms = wind.get("speed", 0.0)
        wind_kmh = wind_speed_ms * 3.6
        wind_deg = wind.get("deg", 0.0)
        wind_dir = cls.degrees_to_cardinal(wind_deg)

        if units == "imperial":
            wind_str = f"{round(wind_kmh * 0.621371)} mph from {wind_dir}"
        else:
            wind_str = f"{round(wind_kmh)} km/h from {wind_dir}"

        condition_desc = weather.get("description", "Unknown").capitalize()
        condition_icon = cls.get_condition_icon(condition_desc)

        visibility_m = data.get("visibility", 10000)
        visibility_km = round(visibility_m / 1000)

        dt_ts = data.get("dt", int(datetime.now().timestamp()))
        sunrise_ts = sys_data.get("sunrise", dt_ts - 28000)
        sunset_ts = sys_data.get("sunset", dt_ts + 3000)

        return {
            "city": data.get("name", "Unknown"),
            "country": sys_data.get("country", ""),
            "updated_at": cls.format_timestamp(dt_ts),
            "temp_raw": temp_c,
            "temp": cls.format_temperature(temp_c, units),
            "feels_like": cls.format_temperature(feels_like_c, units),
            "temp_min": cls.format_temperature(temp_min_c, units),
            "temp_max": cls.format_temperature(temp_max_c, units),
            "conditions": f"{condition_desc} {condition_icon}".strip(),
            "condition_text": condition_desc,
            "condition_icon": condition_icon,
            "humidity": f"{main.get('humidity', 0)}%",
            "humidity_val": main.get("humidity", 0),
            "wind": wind_str,
            "pressure": f"{main.get('pressure', 1013)} hPa",
            "visibility": f"{visibility_km} km",
            "sunrise": cls.format_time_only(sunrise_ts),
            "sunset": cls.format_time_only(sunset_ts),
            "cached": data.get("_cached", False)
        }

    @classmethod
    def parse_forecast(cls, data: Dict[str, Any], units: str = "metric") -> List[Dict[str, Any]]:
        raw_list = data.get("list", [])
        if not raw_list:
            return []

        days_grouped: Dict[str, List[Dict[str, Any]]] = {}
        for entry in raw_list:
            dt_txt = entry.get("dt_txt", "")
            if dt_txt:
                date_key = dt_txt.split(" ")[0]
            else:
                date_key = datetime.fromtimestamp(entry.get("dt", 0)).strftime("%Y-%m-%d")

            if date_key not in days_grouped:
                days_grouped[date_key] = []
            days_grouped[date_key].append(entry)

        parsed_forecast = []
        for date_str, entries in list(days_grouped.items())[:5]:
            temps_min = [e.get("main", {}).get("temp_min", e.get("main", {}).get("temp", 0)) for e in entries]
            temps_max = [e.get("main", {}).get("temp_max", e.get("main", {}).get("temp", 0)) for e in entries]
            humidities = [e.get("main", {}).get("humidity", 0) for e in entries]
            
            mid_idx = len(entries) // 2
            weather_mid = entries[mid_idx].get("weather", [{}])[0]
            cond_desc = weather_mid.get("main", "Clear")
            icon = cls.get_condition_icon(cond_desc)

            min_val = min(temps_min) if temps_min else 0
            max_val = max(temps_max) if temps_max else 0
            avg_hum = round(sum(humidities) / len(humidities)) if humidities else 0

            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            day_label = date_obj.strftime("%a %d %b")

            parsed_forecast.append({
                "date_key": date_str,
                "day_label": day_label,
                "icon": icon,
                "temp_max": cls.format_temperature(max_val, units),
                "temp_min": cls.format_temperature(min_val, units),
                "temp_avg": round((min_val + max_val) / 2, 1),
                "humidity": f"(Humidity: {avg_hum}%)",
                "condition": cond_desc
            })

        return parsed_forecast
