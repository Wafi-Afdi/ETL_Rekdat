import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

FILE_PATH = os.getenv('FILE_PATH')


def scrape_steamcharts_batch(app_ids):
    """
    Scrape SteamCharts data for a list of app IDs and save it to a single CSV file.

    Parameters:
        app_ids (list): A list of Steam app IDs to scrape data for.
    """
    # Open a single CSV file to save the data for all apps
    csv_file = os.path.join(FILE_PATH, 'steamcharts_batch_data.csv')
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['appId', 'Month', 'Average Players', 'Gain', 'Percentage Gain', 'Peak Players'])

        # Loop through each app_id and scrape data
        for app_id in app_ids:
            url = f'https://steamcharts.com/app/{app_id}'
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"Failed to fetch data for App ID {app_id}. HTTP Status Code: {response.status_code}")
                continue
            
            # Parse the HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the table
            table = soup.find('table', class_='common-table')
            if not table:
                print(f"Table not found for App ID {app_id}.")
                continue
            
            # Find all rows in the table
            rows = table.find_all('tr', class_=['odd', 'even'])  # Includes both 'odd' and 'even' rows
            for row in rows:
                columns = row.find_all('td')
                if len(columns) == 5:  # Ensure all columns are present
                    month = columns[0].text.strip()
                    avg_players = columns[1].text.strip()
                    gain = columns[2].text.strip()
                    percent_gain = columns[3].text.strip()
                    peak_players = columns[4].text.strip()
                    # Write the row to the CSV
                    writer.writerow([app_id, month, avg_players, gain, percent_gain, peak_players])
    
    print(f"Data successfully written to {csv_file}")

# List of app IDs to scrape
# Load the cleaned JSON data
def main():
    with open('cleaned_data.json', 'r') as f:
        cleaned_data = json.load(f)
    
    # Convert JSON to DataFrame
    df = pd.DataFrame(cleaned_data)
    
    # Filter DataFrame to get appid for release_date after 2020
    df['release_date'] = pd.to_datetime(df['release_date'])  # Convert release_date back to datetime
    filtered_df = df[df['release_date'] > '2022-01-01']
    filtered_app_ids = filtered_df['appid'].tolist()
    
    # Scrape data for each app ID in the list
    scrape_steamcharts_batch(filtered_app_ids)
