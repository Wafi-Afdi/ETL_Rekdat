import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os



FILE_PATH = os.getenv('FILE_PATH')


def main():
    load_dotenv()
    # Read JSON data
    file_location_price_history = os.path.join(FILE_PATH, 'steamspy_metadata.json')
    with open(file_location_price_history, 'r') as f:
        data = json.load(f)

    # Konfigurasi koneksi ke database PostgreSQL
    db_config = {
        "dbname": os.getenv('DB_NAME'),
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASSWORD'),
        "host": os.getenv('DB_HOST'),
        "port": os.getenv('DB_PORT'),
        "sslmode": "require",
    }

    # Prepare data for insertion
    price_history_data = []
    for game in data:
        appid = int(game["appid"])
        for record in game["history"]:
            price_history_data.append((
                appid,
                record["timestamp"],
                record["price"],
                record["regular_price"]
            ))

    # SQL query to insert data with ON CONFLICT DO NOTHING
    price_history_query = """
    INSERT INTO game_price_history (appid, timestamp, price, regular_price)
    VALUES %s
    ON CONFLICT DO NOTHING;
    """

    # Database connection
    conn = psycopg2.connect(
        **db_config
    )
    cursor = conn.cursor()

    # Perform bulk insert
    execute_values(cursor, price_history_query, price_history_data)
    conn.commit()

    # Close connection
    cursor.close()
    conn.close()
    print("Proses upload data berhasil")
