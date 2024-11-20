import requests
import time
import json
import pandas as pd




from dotenv import load_dotenv
import os

load_dotenv()

API_KEY_ITAD_ = os.getenv('KMXNIJQWWLLILJQW')

# Function to get game data from the API
def get_game_id(app_id):
    try:
        # Replace 'your_api_key' with your actual API key
        response = requests.get(f'https://api.isthereanydeal.com/games/lookup/v1', 
                                params={'key': API_KEY_ITAD_, 'appid': app_id})
        data = response.json()
        if data.get('status_code') != 200:
            raise Exception(data['reason_phrase'])
        if data.get('found'):
            return data['game']['id']  # Return the game id if found
        else:
            return None
    except Exception as e:
        print(f"Error fetching data for appid {app_id}: {e}")
        return None

# Function to process the array of appIds
def process_app_ids(app_ids_):
    game_data_dict = {}  # Initialize an empty dictionary
    
    for app_id in app_ids_:
        game_data = get_game_id(app_id)
        if game_data:
            game_data_dict[game_data] = app_id # Store the game data in an array
        print(f"Waiting 2 seconds before next request...")
        time.sleep(2)  # Sleep for 2 seconds before making the next request
    
    print(game_data_dict)
    return game_data_dict

# Next Step get prices

def get_game_price_history(game_id, since="2022-01-01T00:00:00Z", shops="61"):
    try:
        # Replace 'your_api_key' with your actual API key
        response = requests.get(f'https://api.isthereanydeal.com/games/history/v2', 
                                params={'key': API_KEY_ITAD_, 'id': game_id, 'shops': shops, 'since': since})
        data = response.json()
        # Check if the response contains valid data
        if data.get('status_code') != 200:
            raise Exception(data['reason_phrase'])
        if data:
            return data
        return None
    except Exception as e:
        print(f"Error fetching data for game id {game_id}: {e}")
        return None

# Function to process the dictionary of game IDs and get their history data
def process_game_histories(game_dict):
    all_game_histories = []

    # Iterate over the dictionary of game IDs
    for game_id, appid in game_dict.items():
        game_history = get_game_price_history(game_id)
        
        # If the game history is available, process and store it
        if game_history:
            formatted_history = []
            for entry in game_history:
                # Extract relevant details from the history data
                timestamp = entry.get('timestamp')
                shop = entry.get('shop', {}).get('name', 'Unknown Shop')
                price = entry.get('deal', {}).get('price', {}).get('amount', 'No Price')
                regular_price = entry.get('deal', {}).get('regular', {}).get('amount', 'No Regular Price')
                currency = entry.get('deal', {}).get('price', {}).get('currency', 'USD')
                
                formatted_history.append({
                    'timestamp': timestamp,
                    'shop': shop,
                    'price': price,
                    'regular_price': regular_price,
                    'currency': currency
                })
            
            # Store the game history along with the game id in the result list
            all_game_histories.append({
                'game_id': game_id,
                'appid': appid,  # Include the AppID as well
                'history': formatted_history
            })
        print(f"Waiting 2 seconds before next request...")
        time.sleep(2)  # Sleep for 2 seconds before making the next request

    return all_game_histories

# Call the process_app_ids function
if __name__ == "__main__":
    # Array of appids you want to look up
    with open('cleaned_data.json', 'r') as f:
        cleaned_data = json.load(f)
    df = pd.DataFrame(cleaned_data)
    df['release_date'] = pd.to_datetime(df['release_date'])  # Convert release_date back to datetime
    filtered_df = df[df['release_date'] > '2023-09-17']
    app_ids = filtered_df['appid'].tolist()


    game_data_array = process_app_ids(app_ids)
    print("SELESAI1", game_data_array)
    game_histories = process_game_histories(game_data_array)
    print("SELESAI2")
    if game_histories:
        output_file = "game_histories.json"
        with open(output_file, "w") as file:
            json.dump(game_histories, file, indent=4)  # indent=4 makes the JSON human-readable
