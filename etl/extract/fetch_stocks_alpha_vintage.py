import requests
import json
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

FILE_PATH = os.getenv('FILE_PATH')

# Replace with your Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = os.getenv('API_KEY_ALPHA')
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
COMPANY_SYMBOL="DEVO.L"

def extract_stock_price_daily(symbol="EA"):
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

def extract_stock_price_monthly(symbol="EA"):
    """
    Extract stock price from Alpha Vantage for the given symbol.
    :param symbol: Stock ticker symbol (default: "EA").
    :return: A dictionary containing stock data.
    """
    params = {
        "function": "TIME_SERIES_MONTHLY",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "datatype":"json",
    }

    response = requests.get(ALPHA_VANTAGE_URL, params=params)
    data = response.json()
    return data


# Test the extract function
def main():
    stock_data_daily = extract_stock_price_daily(COMPANY_SYMBOL)
    if stock_data_daily:
        print("Extracted Data:", stock_data_daily)
        output_file = os.path.join(FILE_PATH, "stock_daily.json")
        with open(output_file, "w") as file:
            json.dump(stock_data_daily, file, indent=4)  # indent=4 makes the JSON human-readable
    else:
        print("Failed to extract stock data.")
    stock_data_monthly = extract_stock_price_monthly(COMPANY_SYMBOL)
    if stock_data_monthly:
        print("Stock Data Extracted")
        output_file = os.path.join(FILE_PATH, "stock_monthly.json")
        with open(output_file, "w") as file:
            json.dump(stock_data_monthly, file, indent=4)  # indent=4 makes the JSON human-readable
    else:
        print("Failed to extract stock data.")
        
main()