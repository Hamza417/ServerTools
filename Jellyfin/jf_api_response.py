import requests

JELLYFIN_SERVER = "http://server_address:8096"
API_KEY = "api_key"

url = f"{JELLYFIN_SERVER}/Users/Public?api_key={API_KEY}"
response = requests.get(url)

print("Status Code:", response.status_code)
print("Response Text:", response.text)
