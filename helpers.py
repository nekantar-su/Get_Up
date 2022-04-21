import requests
import os

def lookup(symbol):
    """Look up quote for symbol."""
    # Contact API
    try:
        api_key = os.environ.get("IEX_KEY")
        url = "https://cloud.iexapis.com/stable/stock/"+symbol+"/quote?token="+api_key
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None