import requests
import sys
from dotenv import dotenv_values

secrets = dotenv_values(".env")

page_token = "&"
country_code = "PL"
api_key = secrets["YOUTUBE_DATA_API_KEY"]

request_url = (f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet,contentDetails,"
               f"liveStreamingDetails,localizations,player,recordingDetails,status,"
               f"topicDetails&chart=mostPopular&regionCode={country_code}&maxResults=1&key={api_key}")
httpResponse = requests.get(request_url)
if httpResponse.status_code == 429:
    print("Temp-Banned due to excess requests, please wait and continue later")
    sys.exit()
response = httpResponse.json()
print(response)
