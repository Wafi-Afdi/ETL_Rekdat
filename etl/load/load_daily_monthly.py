import psycopg2
from psycopg2 import sql
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

FILE_PATH = os.getenv('FILE_PATH')

# Konfigurasi koneksi ke database PostgreSQL
db_config = {
    "dbname": os.getenv('DB_NAME'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "host": os.getenv('DB_HOST'),
    "port": os.getenv('DB_PORT')
}

# Fungsi untuk membuat tabel
def create_tables(conn):
    with conn.cursor() as cursor:
        # Query untuk membuat tabel data harian
        create_daily_table_query = """
        CREATE TABLE IF NOT EXISTS stock_daily (
            date DATE,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            volume BIGINT,
            daily_change FLOAT,
            daily_range FLOAT,
            symbol VARCHAR(10),
            PRIMARY KEY (date, symbol)
        );
        """
        cursor.execute(create_daily_table_query)

        # Query untuk membuat tabel data bulanan
        create_monthly_table_query = """
        CREATE TABLE IF NOT EXISTS stock_monthly (
            date DATE,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            volume BIGINT,
            monthly_change FLOAT,
            monthly_range FLOAT,
            symbol VARCHAR(10),
            PRIMARY KEY (date, symbol)
        );
        """
        cursor.execute(create_monthly_table_query)
        conn.commit()
        print("Tabel berhasil dibuat (jika belum ada).")

# Fungsi untuk memasukkan data ke tabel
def insert_data_to_table(conn, df, table_name):
    with conn.cursor() as cursor:
        for _, row in df.iterrows():
            insert_query = sql.SQL("""
            INSERT INTO {table} (date, open, high, low, close, volume, {change}, {range}, symbol)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (date, symbol) DO NOTHING;
            """).format(
                table=sql.Identifier(table_name),
                change=sql.Identifier("daily_change" if table_name == "stock_daily" else "monthly_change"),
                range=sql.Identifier("daily_range" if table_name == "stock_daily" else "monthly_range")
            )
            cursor.execute(insert_query, tuple(row))
        conn.commit()
        print(f"Data berhasil dimasukkan ke tabel {table_name}.")

# Baca data dari file CSV hasil transformasi
daily_input = os.path.join(FILE_PATH, 'transformed_daily_data_with_date.csv')
monthly_input = os.path.join(FILE_PATH, 'transformed_monthly_data_with_date.csv')

daily_df = pd.read_csv(daily_input)
monthly_df = pd.read_csv(monthly_input)

# Koneksi ke database PostgreSQL
try:
    conn = psycopg2.connect(**db_config)
    print("Berhasil terhubung ke database.")

    # Membuat tabel jika belum ada
    create_tables(conn)

    # Memasukkan data ke tabel PostgreSQL
    insert_data_to_table(conn, daily_df, "stock_daily")
    insert_data_to_table(conn, monthly_df, "stock_monthly")

except Exception as e:
    print("Terjadi kesalahan:", e)

finally:
    if conn:
        conn.close()
        print("Koneksi ke database ditutup.")
