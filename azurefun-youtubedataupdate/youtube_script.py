import requests
import pyodbc
from . import youtube_requests


def get_youtube_response(api_key, country_code, base_request, map_response):
    request = f"https://www.googleapis.com/youtube/v3/{base_request}&regionCode={country_code}&key={api_key}"
    http_response = requests.get(request)
    if http_response.status_code == 429:
        raise Exception("Temp-Banned due to excess requests, please wait and continue later")
    response = http_response.json()
    return map_response(response)


def get_db_connection(server, database, username, password):
    return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


def save_data_to_db(conn, response_dicts):
    with conn as conn2:
        with conn2.cursor() as cursor:
            table_name = response_dicts[0]['TableName']
            columns = [key for key in list(response_dicts[0].keys())[1:]]
            columns_str = ", ".join(columns)
            values_questionmark_str = ", ".join(["?" for col in columns])
            sql = f"insert into {table_name} ({columns_str}) values ({values_questionmark_str})"
            for dict in response_dicts:
                cursor.execute(sql, list(dict.values())[1:])
        conn2.commit()


def update_db(api_key, server, username, password):
    database = 'YoutubeStats'
    country_code = "PL"
    response_dicts = get_youtube_response(api_key, country_code, youtube_requests.videos_request(1), youtube_requests.videos_dictionaries)
    conn = get_db_connection(server, database, username, password)
    save_data_to_db(conn, response_dicts)