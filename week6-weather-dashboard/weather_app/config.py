import os
from pathlib import Path
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")

class Config:
    API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()
    BASE_URL = os.getenv("BASE_URL", "https://api.openweathermap.org/data/2.5").strip()
    DEFAULT_CITY = os.getenv("DEFAULT_CITY", "New Delhi").strip()
    DEFAULT_UNITS = os.getenv("DEFAULT_UNITS", "metric").strip().lower()
    CACHE_DURATION = int(os.getenv("CACHE_DURATION_SECONDS", "600"))
    TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
    DATA_DIR = project_root / "data"
    CACHE_DIR = DATA_DIR / "cache"
    FAVORITES_FILE = DATA_DIR / "favorites.json"
    EXPORTS_DIR = DATA_DIR / "exports"

    @classmethod
    def ensure_directories(cls):
        cls.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cls.EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
        if not cls.FAVORITES_FILE.exists():
            cls.FAVORITES_FILE.write_text("[\"New Delhi\", \"Mumbai\", \"Bengaluru\", \"Kolkata\", \"Chennai\"]", encoding="utf-8")
