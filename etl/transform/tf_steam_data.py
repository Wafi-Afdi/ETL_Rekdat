import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values
import os

load_dotenv()

FILE_PATH = os.getenv('FILE_PATH')

db_config = {
    "dbname": os.getenv('DB_NAME'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "host": os.getenv('DB_HOST'),
    "port": os.getenv('DB_PORT'),
    "sslmode" : "require",
}


# Load JSON data
def load_json_data(file_path):
    return pd.read_json(file_path)

# Insert data into PostgreSQL with `ON CONFLICT DO NOTHING`
def insert_with_conflict_handling(conn, table_name, data, conflict_columns):
    cursor = conn.cursor()
    columns = ', '.join(data.columns)
    values = ', '.join([f"%({col})s" for col in data.columns])
    conflict_clause = f"ON CONFLICT ({', '.join(conflict_columns)}) DO NOTHING"

    query = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({values})
        {conflict_clause};
    """
    try:
        # Convert DataFrame to dictionary records and execute
        for record in data.to_dict(orient='records'):
            cursor.execute(query, record)
        conn.commit()
        print(f"Data inserted into {table_name} successfully!")
    except Exception as e:
        print(f"Error inserting into {table_name}: {e}")
        conn.rollback()

# Main function
def main():
    # Load data
    steam_data = load_json_data(os.path.join(FILE_PATH, 'steamspy_metadata.json'))
    cleaned_data = load_json_data(os.path.join(FILE_PATH, 'scraped_steam_data.json'))

    # Merge data
    merged_data = pd.merge(steam_data, cleaned_data, on="appid", how="inner")
    merged_data["discount"] = merged_data["discount"].fillna(0).replace([np.inf, -np.inf], 0).astype(int)
    merged_data["price"] = merged_data["price"].astype(float) / 100
    merged_data["initialprice"] = merged_data["initialprice"].astype(float) / 100
    merged_data["release_date"] = pd.to_datetime(merged_data["release_date"])
    merged_data = merged_data.where(pd.notnull(merged_data), None)  # Replace NaN with None

    # Process genres and languages
    def process_column_data(merged_data, column_name, new_column_name):
        records = []
        for _, row in merged_data.iterrows():
            appid = row["appid"]
            values = row[column_name].split(", ") if row[column_name] else ["Unknown"]
            for value in values:
                records.append({"appid": appid, new_column_name: value})
        return pd.DataFrame(records)

    genres_df = process_column_data(merged_data, "genre", "genre")
    languages_df = process_column_data(merged_data, "languages", "language")
    merged_data = merged_data.drop(columns=["tags", "genre", "languages"])

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        **db_config
    )

    # Insert data into tables
    insert_with_conflict_handling(conn, "steam_game", merged_data, ["appid"])
    insert_with_conflict_handling(conn, "genres", genres_df, ["appid", "genre"])
    insert_with_conflict_handling(conn, "languages", languages_df, ["appid", "language"])

    # Close connection
    conn.close()

if __name__ == "__main__":
    main()
