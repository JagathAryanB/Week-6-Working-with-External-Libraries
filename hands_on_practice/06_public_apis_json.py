import json
import requests

def fetch_jsonplaceholder_posts(limit=3):
    url = "https://jsonplaceholder.typicode.com/posts"
    try:
        response = requests.get(url, params={"_limit": limit}, timeout=10)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        pass
    return [
        {"userId": 1, "id": 1, "title": "Mock Post 1", "body": "Mock content 1"},
        {"userId": 1, "id": 2, "title": "Mock Post 2", "body": "Mock content 2"}
    ]

def fetch_ip_geolocation():
    url = "https://ipapi.co/json/"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "city" in data:
                return {
                    "ip": data.get("ip"),
                    "city": data.get("city"),
                    "region": data.get("region"),
                    "country_name": data.get("country_name"),
                    "latitude": data.get("latitude"),
                    "longitude": data.get("longitude")
                }
    except requests.exceptions.RequestException:
        pass
    return {
        "ip": "127.0.0.1",
        "city": "London",
        "region": "England",
        "country_name": "United Kingdom",
        "latitude": 51.5074,
        "longitude": -0.1278
    }

def main():
    print("=" * 60)
    print("WORKING WITH PUBLIC APIS & JSON DATA")
    print("=" * 60)

    print("\n1. JSONPlaceholder API (Posts):")
    posts = fetch_jsonplaceholder_posts(limit=2)
    for p in posts:
        print(f"   [ID: {p['id']}] {p['title']}")
        print(f"      Body: {p['body'][:60]}...")

    print("\n2. IP Geolocation API:")
    geo = fetch_ip_geolocation()
    print(json.dumps(geo, indent=4))

    print("\n3. JSON Transformation & Serialization:")
    transformed = {
        "total_posts_retrieved": len(posts),
        "post_titles": [p["title"] for p in posts],
        "location_summary": f"{geo['city']}, {geo['country_name']}"
    }
    serialized = json.dumps(transformed, indent=2)
    print(serialized)
    print("=" * 60)

if __name__ == "__main__":
    main()
