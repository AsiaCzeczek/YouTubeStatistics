import logging
import azure.functions as func
import os
from azurefun-youtubedataupdate import youtube_script

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function update DB request.')

    api_key = os.environ["YOUTUBE_DATA_API_KEY"]
    server = os.environ["AZURE_SQL_SERVER"]
    username = os.environ["AZURE_SQL_USERNAME"]
    password = '{' + os.environ["AZURE_SQL_PASSWORD"] + '}'

    youtube_script.update_db(api_key, server, username, password)

    return func.HttpResponse(
             "DB updated",
             status_code=200
        )
