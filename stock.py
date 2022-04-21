import requests

def lookup(symbol):
    """Look up quote for symbol."""
    # Contact API
    try:
        api_key = 'pk_ab5edca00a504528a72de0b5ea47677a'
        
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
    
stock = lookup('TSLA')
print(f"{stock['name']} is trading at ${stock['price']}!")