import requests
import time
import json
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

FILE_PATH = os.getenv('FILE_PATH')


# Define the list of appids
appids = [20]  # Add more appids as needed

output_file = os.path.join(FILE_PATH, "steamspy_metadata.json")

# Function to fetch data for each appid and store in a list
def fetch_and_save_data(app_array):
    app_data = []

    for appid in app_array:
        try:
            # Make the API request to SteamSpy API
            response = requests.get(f'https://steamspy.com/api.php?request=appdetails&appid={appid}')
            data = response.json()

            app_data.append(data)

            # Wait 0.5 seconds before making the next request to avoid rate limiting
            print(f"Successfully fetched {appid}, Waiting 0.5 seconds till next fetch")
            time.sleep(0.5)

        except Exception as e:
            print(f"Error fetching data for appid {appid}: {e}")

    # Save the collected data to a JSON file
    with open(output_file, 'w') as outfile:
        json.dump(app_data, outfile, indent=2)

    print(f"Data saved to {output_file}")

# Call the function to fetch and save data
def main():
    with open(os.path.join(FILE_PATH, "scraped_steam_data.json"), 'r') as f:
        cleaned_data = json.load(f)
    df = pd.DataFrame(cleaned_data)
    df['release_date'] = pd.to_datetime(df['release_date'])  # Convert release_date back to datetime
    filtered_df = df[df['release_date'] > '2022-01-01']
    app_ids = df['appid'].tolist()

    fetch_and_save_data(app_ids)

    
# main()