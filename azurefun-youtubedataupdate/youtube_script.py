import requests
import pyodbc

def get_name_and_likes_of_most_popular_video(api_key, country_code):
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


def get_db_connection(server, database, username, password):
    return pyodbc.connect(
            'DRIVER= {ODBC Driver 17 for SQL Server};SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


def save_data_to_db(conn, name, likes):
    with conn as conn2:
        with conn2.cursor() as cursor:
            sql = "insert into Videos (Name, Likes) values (?, ?)"
            cursor.execute(sql, name, likes)

        conn2.commit()

def update_db(api_key, server, username, password):
    database = 'YoutubeStats'
    country_code = "PL"
    name, likes = get_name_and_likes_of_most_popular_video(api_key, country_code)
    conn = get_db_connection(server, database, username, password)
    save_data_to_db(conn, name, likes)