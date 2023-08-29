import requests
import pyodbc
from datetime import datetime
from . import youtube_videos
# import youtube_videos

TABLE_NAME_KEY =youtube_videos.TABLE_NAME

def get_youtube_response(api_key, country_code, max_results, base_request):
    request = f"https://www.googleapis.com/youtube/v3/{base_request}&maxResults={max_results}&regionCode={country_code}&key={api_key}"
    http_response = requests.get(request)
    if http_response.status_code == 429:
        raise Exception("Temp-Banned due to excess requests, please wait and continue later")
    return http_response.json()


def get_db_connection(server, database, username, password):
    return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

def insert_or_update_rows(conn, rows, compare_column_name):
    with conn as conn2:
        with conn2.cursor() as cursor:
            table_name = rows[0][TABLE_NAME_KEY]

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
        conn2.commit()

def insert_rows(conn, rows):
    with conn as conn2:
        with conn2.cursor() as cursor:
            table_name = rows[0][TABLE_NAME_KEY]

            columns = [key for key in list(rows[0].keys())[1:]]
            columns_str = ", ".join(columns)
            values_questionmark_str = ", ".join(["?" for col in columns])
            insert_sql = f"insert into {table_name} ({columns_str}) values ({values_questionmark_str})"

            for row in rows:
                values_to_save = list(row.values())[1:]
                cursor.execute(insert_sql, values_to_save)
        conn2.commit()


def update_db(api_key, server, username, password):
    database = 'YoutubeStats'
    country_code = "PL"
    max_results = 10
    current_datetime = datetime.now()

    conn = get_db_connection(server, database, username, password)

    videos_response = get_youtube_response(api_key, country_code, max_results, youtube_videos.videos_request)
    videos_rows = youtube_videos.videos_rows(videos_response)
    tags_rows = youtube_videos.tags_rows(videos_response)
    statistic_rows = youtube_videos.statistic_rows(videos_response, current_datetime)
    insert_or_update_rows(conn, videos_rows, "VideoId")
    insert_or_update_rows(conn, tags_rows, "TagName")
    insert_rows(conn, statistic_rows)