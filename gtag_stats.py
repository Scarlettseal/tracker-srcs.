import requests
from bs4 import BeautifulSoup
import json

# URL of the Steam Charts page for the game
url = "https://steamcharts.com/app/1533390"
# Your Discord webhook URL
webhook_url = "https://discord.com/api/webhooks/1304891196799320104/HzhbNexWb25uxSQuvu9-kvHG3pobYtfEaxjHd5pYYWtDJLZ6OPN_dYWWvR7VFEkmznR2"


def get_player_data():
    # Send a GET request to the Steam Charts page
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the "Playing X min ago" value
        try:
            playing_recent = soup.find("div", class_="app-stat").find("span", class_="num").text.strip()
        except AttributeError:
            playing_recent = "N/A"
        
        # Find the "24-hour peak" value
        try:
            peak_24hr = soup.find("div", string="24-hour peak").find_next_sibling("span", class_="num").text.strip()
        except AttributeError:
            peak_24hr = "N/A"
        
        # Find the "All-time peak" value
        try:
            all_time_peak = soup.find("div", string="All-time peak").find_next_sibling("span", class_="num").text.strip()
        except AttributeError:
            all_time_peak = "N/A"
        
        # Find the game's thumbnail image
        try:
            thumbnail_url = soup.find("img", class_="app-logo")["src"]
            if thumbnail_url.startswith("/"):
                thumbnail_url = "https://steamcharts.com" + thumbnail_url
        except (AttributeError, TypeError):
            thumbnail_url = None
        
        return {
            "Playing Recently": playing_recent,
            "24-Hour Peak": peak_24hr,
            "All-Time Peak": all_time_peak,
            "Thumbnail": thumbnail_url
        }
    else:
        print("Failed to retrieve data from Steam Charts")
        return None

def send_embed_to_discord(data):
    # Prepare the embed payload
    embed = {
        "title": "Steam Charts - Lost Ark",
        "url": url,
        "color": 3447003,
        "fields": [
            {"name": "Playing Recently", "value": data["Playing Recently"], "inline": True},
            {"name": "24-Hour Peak", "value": data["24-Hour Peak"], "inline": True},
            {"name": "All-Time Peak", "value": data["All-Time Peak"], "inline": True}
        ]
    }
    
    # Add the thumbnail if available
    if data["Thumbnail"]:
        embed["thumbnail"] = {"url": data["Thumbnail"]}
    
    payload = {
        "embeds": [embed]
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    # Send the embed message via POST request
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 204:
        print("Embed sent to Discord successfully!")
    else:
        print(f"Failed to send embed to Discord: {response.status_code}")

def main():
    # Get player data
    data = get_player_data()
    
    if data:
        # Send the data to Discord as an embed
        send_embed_to_discord(data)
    else:
        print("Could not retrieve player data.")

if __name__ == "__main__":
    main()
