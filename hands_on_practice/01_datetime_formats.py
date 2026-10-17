from datetime import datetime, timezone

def get_formatted_dates():
    now_local = datetime.now()
    now_utc = datetime.now(timezone.utc)
    
    formats = {
        "ISO 8601 (Local)": now_local.isoformat(),
        "ISO 8601 (UTC)": now_utc.isoformat(),
        "Standard Date (YYYY-MM-DD)": now_local.strftime("%Y-%m-%d"),
        "Standard Time 24h (HH:MM:SS)": now_local.strftime("%H:%M:%S"),
        "Standard Time 12h (HH:MM:SS AM/PM)": now_local.strftime("%I:%M:%S %p"),
        "Friendly Date": now_local.strftime("%A, %B %d, %Y"),
        "Short Date (DD/MM/YYYY)": now_local.strftime("%d/%m/%Y"),
        "US Date (MM/DD/YYYY)": now_local.strftime("%m/%d/%Y"),
        "Unix Timestamp": str(int(now_local.timestamp())),
        "RFC 2822 format": now_local.strftime("%a, %d %b %Y %H:%M:%S %z")
    }
    return formats

def main():
    print("=" * 50)
    print("DATE AND TIME FORMATS DEMONSTRATION")
    print("=" * 50)
    for name, value in get_formatted_dates().items():
        print(f"{name:<35}: {value}")
    print("=" * 50)

if __name__ == "__main__":
    main()
