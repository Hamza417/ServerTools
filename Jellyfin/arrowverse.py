import os
import requests
import sys
import logging
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 🔹 CONFIGURE THESE
JELLYFIN_SERVER = os.getenv("JELLYFIN_SERVER")
API_KEY = os.getenv("API_KEY")
USER_ID = os.getenv("USER_ID")

# 🔹 List of Arrowverse series (Modify if needed)
ARROWVERSE_SHOWS = [
    "Arrow", "The Flash", "Supergirl", "DC's Legends of Tomorrow",
    "Batwoman", "Black Lightning", "Superman & Lois", "Constantine",
    "Vixen", "Freedom Fighters: The Ray", "DC's Stargirl"
]


def make_request(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None


def check_user():
    url = f"{JELLYFIN_SERVER}/Users/Public?api_key={API_KEY}"
    response = make_request(url)
    if response:
        logging.info("User ID fetched successfully!")
        logging.info(get_user_id())


def get_user_id():
    url = f"{JELLYFIN_SERVER}/Users?api_key={API_KEY}"
    response = make_request(url)
    if response:
        try:
            users = response.json()
            for user in users:
                logging.info(f"User ID: {user['Id']}, Name: {user['Name']}")
            return users[0]['Id']  # Return the first user's ID for now
        except ValueError:
            logging.error("Error parsing response.")
    return None


def get_episodes():
    url = f"{JELLYFIN_SERVER}/Users/{USER_ID}/Items"
    params = {
        "Recursive": "true",
        "IncludeItemTypes": "Episode",
        "Fields": "PremiereDate,SeriesName,Name,Id,IndexNumber,ParentIndexNumber",
        "Limit": 50,
        "StartIndex": 0,
        "api_key": API_KEY
    }

    episodes_ = []
    while True:
        response = make_request(url, params)
        if not response:
            break

        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            logging.error("Failed to decode JSON! Check API URL and key.")
            break

        if "Items" not in response_json:
            logging.warning("No episodes found!")
            break

        for item in response_json["Items"]:
            if item["SeriesName"].strip() in ARROWVERSE_SHOWS and "PremiereDate" in item:
                episodes_.append({
                    "id": item["Id"],
                    "title": item["Name"],
                    "show": item["SeriesName"],
                    "season": item["ParentIndexNumber"],
                    "episode": item["IndexNumber"],
                    "air_date": item["PremiereDate"]
                })

        if len(response_json["Items"]) < params["Limit"]:
            break

        params["StartIndex"] += params["Limit"]
        sys.stdout.write(f"\r🔍 Fetched {len(episodes_)} Arrowverse episodes..., checking for more")
        sys.stdout.flush()

    sys.stdout.write(f"\r🔍 Fetched {len(episodes_)} Arrowverse episodes.{' ' * 20}\n")
    sys.stdout.flush()

    sorted_episodes = sorted(episodes_, key=lambda x: (x['air_date']))

    return sorted_episodes


def get_playlist_id(playlist_name):
    url = f"{JELLYFIN_SERVER}/Users/{USER_ID}/Items"
    params = {
        "IncludeItemTypes": "Playlist",
        "Recursive": "true",
        "api_key": API_KEY
    }

    response = make_request(url, params)
    if response:
        playlists = response.json().get("Items", [])
        for playlist in playlists:
            if playlist["Name"] == playlist_name:
                return playlist["Id"]

    return None


def create_playlist(_episode_ids):
    playlist_name = "Arrowverse"
    playlist_url = f"{JELLYFIN_SERVER}/Playlists?api_key={API_KEY}"
    playlist_data = {
        "Name": playlist_name,
        "UserId": USER_ID,
        "Ids": _episode_ids
    }

    try:
        response = requests.post(playlist_url, json=playlist_data)
        response.raise_for_status()
        logging.info("Playlist created successfully!")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to create playlist: {e}")


if __name__ == "__main__":
    logging.info("Checking Jellyfin user...")
    check_user()

    logging.info("Fetching Arrowverse episodes from Jellyfin...")
    episodes = get_episodes()

    if not episodes:
        logging.warning("No Arrowverse episodes found!")
    else:
        episode_ids = [ep["id"] for ep in episodes]
        create_playlist(episode_ids)
