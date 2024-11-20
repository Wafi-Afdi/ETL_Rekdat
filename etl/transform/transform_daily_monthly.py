import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()

FILE_PATH = os.getenv('FILE_PATH')

def main():
    daily_input_path = os.path.join(FILE_PATH, 'stock_daily.json')
    monthly_input_path = os.path.join(FILE_PATH, 'stock_monthly.json')

    # Load data harian dan bulanan
    with open(daily_input_path, 'r') as daily_file:
        daily_data = json.load(daily_file)

    with open(monthly_input_path, 'r') as monthly_file:
        monthly_data = json.load(monthly_file)

    # Ambil simbol saham dari metadata
    daily_symbol = daily_data["Meta Data"]["2. Symbol"]
    monthly_symbol = monthly_data["Meta Data"]["2. Symbol"]

    # Transformasi data harian
    daily_time_series = daily_data["Time Series (Daily)"]
    daily_df = pd.DataFrame.from_dict(daily_time_series, orient='index')
    daily_df.index = pd.to_datetime(daily_df.index)  # Konversi indeks menjadi datetime
    daily_df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume"
    }, inplace=True)
    daily_df.reset_index(inplace=True)  # Pindahkan indeks ke dalam DataFrame
    daily_df.rename(columns={"index": "date"}, inplace=True)  # Ubah nama kolom menjadi "date"
    daily_df = daily_df[["date", "open", "high", "low", "close", "volume"]].astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
    daily_df['daily_change'] = daily_df['close'] - daily_df['open']  # Tambahkan kolom perubahan harian
    daily_df['daily_range'] = daily_df['high'] - daily_df['low']  # Tambahkan kolom rentang harian
    daily_df['symbol'] = daily_symbol  # Tambahkan kolom simbol saham

    # Transformasi data bulanan
    monthly_time_series = monthly_data["Monthly Time Series"]
    monthly_df = pd.DataFrame.from_dict(monthly_time_series, orient='index')
    monthly_df.index = pd.to_datetime(monthly_df.index)  # Konversi indeks menjadi datetime
    monthly_df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume"
    }, inplace=True)
    monthly_df.reset_index(inplace=True)  # Pindahkan indeks ke dalam DataFrame
    monthly_df.rename(columns={"index": "date"}, inplace=True)  # Ubah nama kolom menjadi "date"
    monthly_df = monthly_df[["date", "open", "high", "low", "close", "volume"]].astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
    monthly_df['monthly_change'] = monthly_df['close'] - monthly_df['open']  # Tambahkan kolom perubahan bulanan
    monthly_df['monthly_range'] = monthly_df['high'] - monthly_df['low']  # Tambahkan kolom rentang bulanan
    monthly_df['symbol'] = monthly_symbol  # Tambahkan kolom simbol saham

    # Hasil Transformasi
    print("Data Harian (Transformasi):")
    print(daily_df.head())
    print("\nData Bulanan (Transformasi):")
    print(monthly_df.head())

    # Simpan hasil transformasi ke file CSV
    daily_output_path = os.path.join(FILE_PATH, 'transformed_daily_data_with_date.csv')
    monthly_output_path = os.path.join(FILE_PATH, 'transformed_monthly_data_with_date.csv')

    daily_df.to_csv(daily_output_path, index=False)
    monthly_df.to_csv(monthly_output_path, index=False)

main()
