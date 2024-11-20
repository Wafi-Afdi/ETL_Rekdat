import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from psycopg2.extras import execute_values
import numpy as np


def main():
# Read the CSV file
    df = pd.read_csv('steamcharts_batch_data.csv')

    # Clean and transform data
    # Remove % from "Percentage Gain" and convert to float
    df['Percentage Gain'] = (
        df['Percentage Gain']
        .str.replace('%', '', regex=False)
        .replace('-', None)  # Replace '-' with None
        .astype(float) / 100
    )

    # Convert "Gain" to numeric, handling missing values (e.g., '-')
    df['Gain'] = pd.to_numeric(df['Gain'], errors='coerce')

    # Convert other columns to appropriate types
    df['Average Players'] = pd.to_numeric(df['Average Players'], errors='coerce')
    df['Peak Players'] = pd.to_numeric(df['Peak Players'], errors='coerce')

    # Transform 'Month' into actual datetime
    def parse_month(month):
        if month == "Last 30 Days":
            return pd.Timestamp.now().replace(day=1)  # Use the current month's first day
        else:
            return pd.to_datetime(month, format='%B %Y', errors='coerce')

    df['Month'] = df['Month'].apply(parse_month)

    # Create a DataFrame for the 'game' table
    game_df = df[['appId']].drop_duplicates().reset_index(drop=True).rename(columns={'appId': 'appid'})
    game_df['appid'] = game_df['appid'].astype(object)




    # Create a DataFrame for the 'player_chart' table
    player_chart_df = df[['Month', 'appId', 'Average Players', 'Gain', 'Percentage Gain', 'Peak Players']]
    player_chart_df = player_chart_df.rename(columns={
        'Month': 'month',
        'appId': 'appid',
        'Average Players': 'average_players',
        'Gain': 'gain',
        'Percentage Gain': 'percentage_gain',
        'Peak Players': 'peak_players'
    })

    # Set up the database connection (replace with your database credentials)
    engine = create_engine('postgresql://postgres:password@localhost:5432/rekdat')

    # Database connection (replace with your credentials)
    conn = psycopg2.connect(
        dbname="rekdat",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()

    game_df.head()

    # menghindari duplication pada tabel games
    game_query = """
    INSERT INTO steam_game (appid) VALUES %s
    ON CONFLICT (appid) DO NOTHING;
    """
    execute_values(cursor, game_query, [(row['appid'],) for _, row in game_df.iterrows()])

    # menghindari duplication pada tabel player_chart
    player_chart_query = """
    INSERT INTO player_chart (month, appid, average_players, gain, percentage_gain, peak_players)
    VALUES %s
    ON CONFLICT (month, appid)
    DO UPDATE SET
        average_players = EXCLUDED.average_players,
        gain = EXCLUDED.gain,
        percentage_gain = EXCLUDED.percentage_gain,
        peak_players = EXCLUDED.peak_players;
    """

    # Data preparation for execute_values
    player_chart_data = [
        (
            row['month'],
            row['appid'],
            row['average_players'],
            row['gain'],
            row['percentage_gain'],
            row['peak_players']
        )
        for _, row in player_chart_df.iterrows()
    ]

    # Execute query
    execute_values(cursor, player_chart_query, player_chart_data)

    # Commit changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    # Write the DataFrames to PostgreSQL



    print("Data loaded successfully!")


main()

