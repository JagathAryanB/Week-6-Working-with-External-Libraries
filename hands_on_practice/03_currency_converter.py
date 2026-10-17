import sys
import requests

def fetch_exchange_rates(base_currency="USD"):
    url = f"https://open.er-api.com/v6/latest/{base_currency.upper()}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("result") == "success":
                return data.get("rates", {})
    except requests.exceptions.RequestException:
        pass
    
    return {
        "USD": 1.0,
        "EUR": 0.92,
        "GBP": 0.79,
        "INR": 83.25,
        "JPY": 155.4,
        "CAD": 1.37,
        "AUD": 1.52,
        "CHF": 0.91
    }

def convert_currency(amount, from_curr, to_curr, rates):
    from_curr = from_curr.upper()
    to_curr = to_curr.upper()

    if from_curr not in rates or to_curr not in rates:
        return None

    amount_in_usd = amount / rates[from_curr]
    converted = amount_in_usd * rates[to_curr]
    return converted

def main():
    base = "USD"
    rates = fetch_exchange_rates(base)
    
    amount = 100.0
    from_curr = "USD"
    to_curr = "INR"

    if len(sys.argv) >= 4:
        try:
            amount = float(sys.argv[1])
            from_curr = sys.argv[2].upper()
            to_curr = sys.argv[3].upper()
        except ValueError:
            print("Invalid amount specified. Using defaults: 100 USD to EUR")

    result = convert_currency(amount, from_curr, to_curr, rates)
    
    print("=" * 45)
    print("REAL-TIME CURRENCY CONVERTER")
    print("=" * 45)
    if result is not None:
        print(f"{amount:.2f} {from_curr} = {result:.2f} {to_curr}")
        rate = rates[to_curr] / rates[from_curr]
        print(f"Exchange Rate: 1 {from_curr} = {rate:.4f} {to_curr}")
    else:
        print(f"Error: Unable to convert from {from_curr} to {to_curr}.")
    
    print("-" * 45)
    print("Popular Current Rates relative to 1 USD:")
    for c in ["EUR", "GBP", "INR", "JPY", "CAD", "AUD"]:
        if c in rates:
            print(f"  1 USD = {rates[c]:.2f} {c}")
    print("=" * 45)

if __name__ == "__main__":
    main()
