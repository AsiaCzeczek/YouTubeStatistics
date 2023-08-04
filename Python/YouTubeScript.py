import requests
import sys

page_token = "&"
country_code = "PL"
api_key = "AIzaSyDjN-VCXHbQdsCBevxYA9-Jb-wG4dzSh-U"

request_url = (f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet,contentDetails,"
               f"liveStreamingDetails,localizations,player,recordingDetails,status,"
               f"topicDetails&chart=mostPopular&regionCode={country_code}&maxResults=1&key={api_key}")
request = requests.get(request_url)
if request.status_code == 429:
    print("Temp-Banned due to excess requests, please wait and continue later")
    sys.exit()
response = request.json()
print(response)
