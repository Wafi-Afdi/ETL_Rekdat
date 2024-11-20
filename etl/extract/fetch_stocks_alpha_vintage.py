import requests
import json
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Replace with your Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = os.getenv('API_KEY_ALPHA')
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"

def extract_stock_price(symbol="EA"):
    """
    Extract stock price from Alpha Vantage for the given symbol.
    :param symbol: Stock ticker symbol (default: "EA").
    :return: A dictionary containing stock data.
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "datatype":"json",
        "outputsize" : "full"
    }

    response = requests.get(ALPHA_VANTAGE_URL, params=params)
    data = response.json()
    return data


# Test the extract function
if __name__ == "__main__":
    stock_data = extract_stock_price("DEVO.L")
    if stock_data:
        print("Extracted Data:", stock_data)
        output_file = "stocks.json"
        with open(output_file, "w") as file:
            json.dump(stock_data, file, indent=4)  # indent=4 makes the JSON human-readable
    else:
        print("Failed to extract stock data.")
