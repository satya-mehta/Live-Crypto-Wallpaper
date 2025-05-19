import requests
import json
import time


def fetch_coin_data():
    url = "https://api.coindcx.com/exchange/ticker"
    response = requests.get(url)
    data = response.json()
    print(data)
    # Find the NOTINR trading pair
    coin_data = next((item for item in data if item["market"] == "NOTINR"), None)
    print("---------------------------------------------------------")
    print(coin_data)
    if coin_data:
        coin_details = {
            "last_price": round(float(coin_data["last_price"]), 3),
            "high": round(float(coin_data["high"]), 3),
            "change_24_hour": round(float(coin_data["change_24_hour"]), 3),
            "bid": round(float(coin_data["bid"]), 3)
        }

        with open('coin_data.json', 'w') as file:
            json.dump(coin_details, file, indent=4)


if __name__ == "__main__":
    while True:
        fetch_coin_data()
        time.sleep(10)  # Update every minute
