import requests
import pyodbc
from datetime import datetime
from . import youtube_videos
from . import youtube_channels
#import youtube_videos
#import youtube_channels


def get_youtube_json_response(request):
    http_response = requests.get(request)
    if http_response.status_code == 429:
        raise Exception("Temp-Banned due to excess requests, please wait and continue later")
    return http_response.json()


def get_db_connection(server, database, username, password):
    return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


def insert_or_update_rows(conn, rows, compare_column_name):
    with conn.cursor() as cursor:

        table_name = rows[0]['TableName']

        columns = [key for key in list(rows[0].keys())[1:]]
        columns_str = ", ".join(columns)
        values_questionmark_str = ", ".join(["?" for col in columns])
        insert_sql = f"insert into {table_name} ({columns_str}) values ({values_questionmark_str})"

        columns_questionmark_str = ", ".join([f"{col} = ?" for col in columns])
        update_sql = f"update {table_name} set {columns_questionmark_str} where {compare_column_name} = ?"

        results = cursor.execute(f"select {compare_column_name} from {table_name}").fetchall()
        existing_values = [getattr(row, compare_column_name) for row in results]

        for row in rows:
            comapre_column_value = row[compare_column_name]
            values_to_save = list(row.values())[1:]
            if comapre_column_value in existing_values:
                cursor.execute(update_sql, values_to_save + [comapre_column_value])
            else:
                cursor.execute(insert_sql, values_to_save)


def insert_rows(conn, rows):
    with conn.cursor() as cursor:
        table_name = rows[0]['TableName']

        columns = [key for key in list(rows[0].keys())[1:]]
        columns_str = ", ".join(columns)
        values_questionmark_str = ", ".join(["?" for col in columns])
        insert_sql = f"insert into {table_name} ({columns_str}) values ({values_questionmark_str})"

        for row in rows:
            values_to_save = list(row.values())[1:]
            cursor.execute(insert_sql, values_to_save)


def update_db_for_country(api_key, server, username, password, country_code):
    database = 'YoutubeStats'
    max_results = 30

    videos_request = youtube_videos.videos_request(max_results, country_code, api_key)
    current_datetime = datetime.now()
    videos_json_response = get_youtube_json_response(videos_request)
    videos_rows = youtube_videos.videos_rows(videos_json_response)
    statistic_rows = youtube_videos.statistic_rows(videos_json_response, current_datetime, country_code)

    channels_id = [x['ChannelId'] for x in videos_rows]
    unique_channels_ids = list(set(channels_id))
    channels_request = youtube_channels.channels_request(unique_channels_ids, max_results, api_key)
    current_datetime = datetime.now()
    channels_json_response = get_youtube_json_response(channels_request)
    channels_rows = youtube_channels.channels_rows(channels_json_response)
    channels_statistic_rows = youtube_channels.channels_statistic_rows(channels_json_response, current_datetime)

    with get_db_connection(server, database, username, password) as conn:
        insert_or_update_rows(conn, channels_rows, "ChannelId")
        insert_rows(conn, channels_statistic_rows)

        insert_or_update_rows(conn, videos_rows, "VideoId")
        insert_rows(conn, statistic_rows)

        conn.commit()


def update_db(api_key, server, username, password):
    countries = ['PL', 'US']
    for country in countries:
        update_db_for_country(api_key, server, username, password, country)


