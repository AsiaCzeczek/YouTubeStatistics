import logging
import azure.functions as func
import os
from . import youtube_script


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function update DB request.')

    api_key = os.environ["YOUTUBE_DATA_API_KEY"]
    server = os.environ["AZURE_SQL_SERVER"]
    username = os.environ["AZURE_SQL_USERNAME"]
    password = '{' + os.environ["AZURE_SQL_PASSWORD"] + '}'

    try:
        youtube_script.update_db(api_key, server, username, password)
        logging.info("Update correct.")
    except Exception as error:
        logging.error("Update error.")
        return func.HttpResponse(str(error), status_code=500) 

    return func.HttpResponse("DB updated", status_code=200)
