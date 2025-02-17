'''
This script interacts with the Jellyfin API to:
1. Fetch episodes of Arrowverse series from the Jellyfin server.
2. Collect the necessary episode details (like SeriesName, SeasonNumber, and EpisodeName).
3. Sort and organize these episodes by their correct sequence.
4. Create a new playlist titled "Arrowverse" in Jellyfin.
5. Add the selected episodes to the created playlist using the appropriate episode IDs.

The script ensures that the episodes are correctly fetched, ordered, and added to the playlist
for easy access within the Jellyfin server.
'''

import requests

# 🔹 CONFIGURE THESE
JELLYFIN_SERVER = "http://192.168.100.69:8096"  # Replace with your server address
API_KEY = "api_key"  # Replace with your API key
USER_ID = "user_id"  # Replace with your Jellyfin user ID

# 🔹 List of Arrowverse series (Modify if needed)
ARROWVERSE_SHOWS = [
    "Arrow", "The Flash", "Supergirl", "DC's Legends of Tomorrow",
    "Batwoman", "Black Lightning", "Superman & Lois", "Constantine"
]

def check_user():
    url = f"{JELLYFIN_SERVER}/Users/Public?api_key={API_KEY}"
    response = requests.get(url)

    print("✅ Status Code:", response.status_code)
    print("✅ User ID fetched successfully!:", get_user_id())
    ## print("Response Text:", response.text)

def get_user_id():
    url = f"{JELLYFIN_SERVER}/Users?api_key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            users = response.json()
            for user in users:
                print(f"User ID: {user['Id']}, Name: {user['Name']}")
            return users[0]['Id']  # Return the first user's ID for now
        except ValueError:
            print("❌ Error parsing response.")
    else:
        print("❌ Failed to fetch user information.")

    return None


# 🔹 Fetch all episodes from Jellyfin with pagination support
def get_episodes():
    url = f"{JELLYFIN_SERVER}/Users/{USER_ID}/Items"
    params = {
        "Recursive": "true",
        "IncludeItemTypes": "Episode",
        "Fields": "PremiereDate,SeriesName,Name,Id,IndexNumber,ParentIndexNumber",  # Specify the fields you need
        "Limit": 50,  # Number of items per request
        "StartIndex": 0,  # Starting point
        "api_key": API_KEY
    }

    episodes = []
    while True:
        response = requests.get(url, params=params)
        ## print("🔹 API Status Code:", response.status_code)  # Debugging
        ## print("🔹 Raw Response:", response.text[:500])  # Print first 500 chars
        ## print("🔹 Full Response:", response.text)

        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            print("❌ Failed to decode JSON! Check API URL and key.")
            break

        if "Items" not in response_json:
            print("⚠️ No episodes found!")
            break

        for item in response_json["Items"]:
            if item["SeriesName"] in ARROWVERSE_SHOWS and "PremiereDate" in item:
                episodes.append({
                    "id": item["Id"],
                    "title": item["Name"],
                    "show": item["SeriesName"],
                    "season": item["ParentIndexNumber"],
                    "episode": item["IndexNumber"],
                    "air_date": item["PremiereDate"]
                })

                # print(f"📺 {item['SeriesName']} - S{item['ParentIndexNumber']}E{item['IndexNumber']} - {item['Name']}")

        # Check if there are more items to fetch
        if len(response_json["Items"]) < params["Limit"]:
            break

        # Update StartIndex for the next set of results
        params["StartIndex"] += params["Limit"]
        print("🔄 Moving to the next set of episodes...")

    print("🔹 Found Arrowverse episodes:", len(episodes))

    # Sort by SeasonId and then by IndexNumber (episode number)
    sorted_episodes = sorted(episodes, key=lambda x: (x['air_date']))

    # Now print the sorted episodes
    for episode in sorted_episodes:
        print(f"📺 {episode['id']} : {episode['show']} - S{episode['season']}E{episode['episode']} - {episode['title']}")

    return sorted_episodes

# 🔹 Create a playlist
def create_playlist(episode_ids):
    playlist_url = f"{JELLYFIN_SERVER}/Playlists?api_key={API_KEY}"
    playlist_data = {
        "Name": "Arrowverse",
        "UserId": USER_ID,
        "Ids": episode_ids  # Ensure this is a list of strings
    }

    response = requests.post(playlist_url, json=playlist_data)
    print("🔹 Response: ", response.text)

    if response.status_code == 200:
        print("✅ Playlist created successfully!")
    else:
        print("❌ Failed to create playlist:", response.text)
        print("Response code:", response.status_code)



# 🔹 Run the script
if __name__ == "__main__":
    print("🔹 Checking Jellyfin user...")
    check_user()

    print("🔍 Fetching Arrowverse episodes from Jellyfin...")
    episodes = get_episodes()

    if not episodes:
        print("⚠️ No Arrowverse episodes found!")
    else:
        print(f"📅 Found {len(episodes)} episodes. Creating playlist...")
        episode_ids = [ep["id"] for ep in episodes]
        create_playlist(episode_ids)
