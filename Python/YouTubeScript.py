import requests
import pyodbc
from dotenv import dotenv_values

secrets = dotenv_values(".env")

country_code = "PL"
api_key = secrets["YOUTUBE_DATA_API_KEY"]


def get_name_and_likes_of_most_popular_video(country_code, api_key):
    request_url = (f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet,contentDetails,"
                   f"liveStreamingDetails,localizations,player,recordingDetails,status,"
                   f"topicDetails&chart=mostPopular&regionCode={country_code}&maxResults=1&key={api_key}")
    http_response = requests.get(request_url)
    if http_response.status_code == 429:
        raise Exception("Temp-Banned due to excess requests, please wait and continue later")
    response = http_response.json()
    name = response["items"][0]["snippet"]["title"]
    likes = response["items"][0]["statistics"]["likeCount"]
    return name, likes


def save_data_to_database(server, database, username, password, name, likes):
    with pyodbc.connect(
            'DRIVER= {ODBC Driver 17 for SQL Server};SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as conn:
        with conn.cursor() as cursor:
            sql = "insert into Videos (Name, Likes) values (?, ?)"
            cursor.execute(sql, name, likes)

        conn.commit()


name, likes = get_name_and_likes_of_most_popular_video(country_code, api_key)

server = secrets["AZURE_SQL_SERVER"]
username = secrets["AZURE_SQL_USERNAME"]
password = '{' + secrets["AZURE_SQL_PASSWORD"] + '}'
database = 'YoutubeStats'

save_data_to_database(server, database, username, password, name, likes)
