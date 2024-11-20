from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json
import pandas as pd

def infinite_scroll(driver, pause_time=3):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll to the bottom
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(pause_time)  # Wait for content to load

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # Break the loop if no new content is loaded
            break
        last_height = new_height


def scrape_any_publisher(URL_site):
    # Set up Selenium WebDriver (using Chrome here)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(options=options)
    
    # Navigate to Ubisoft page
    driver.get(URL_site)
    time.sleep(3)  # Wait for initial content to load
    
    # Scroll to load all games (adjust iterations based on content size)
    infinite_scroll(driver=driver, pause_time=3)
    
    # Get the page source after scrolling
    html = driver.page_source
    driver.quit()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all game cards in RecommendationsRows
    recommendations_div = soup.find(id="RecommendationsRows")
    if not recommendations_div:
        print("No recommendations found.")
        return []
    
    game_cards = recommendations_div.find_all("div", class_="recommendation")
    game_links = []
    
    for card in game_cards:
        # Extract data-ds-appid or href attribute
        link_tag = card.find("a", class_="store_capsule")
        title_tag = card.find("span", class_="color_created")
        date_tag = card.find("span", class_="curator_review_date")
        if  link_tag and title_tag and date_tag:
            appid = link_tag.get("data-ds-appid")
            title = title_tag.text.strip()
            release_date = date_tag.text.strip()
            href = link_tag.get("href")
            game_links.append({
                "appid": appid,
                "link": href,
                "title": title,
                "release_date": release_date
            })
    
    return game_links

# Run the scraper
games = scrape_any_publisher("https://store.steampowered.com/publisher/DevolverDigital/#browse")

# turn to json
df = pd.DataFrame(games)

# Convert 'release_date' to datetime format and reformat to YYYY-MM-DD
df['release_date'] = pd.to_datetime(df['release_date'], format='%d %b, %Y').dt.strftime('%Y-%m-%d')

# Display cleaned DataFrame
print(df)

# Save to a new JSON file if needed
cleaned_json = df.to_dict(orient='records')
with open('cleaned_data.json', 'w') as f:
    json.dump(cleaned_json, f, indent=4)
