import logging
import azure.functions as func
import os
from . import youtube_script


def main(myTimer: func.TimerRequest) -> None:
    logging.info(f'Start db update with timer {"delayed" if myTimer.past_due else "on time"}.')

    api_key = os.environ["YOUTUBE_DATA_API_KEY"]
    server = os.environ["AZURE_SQL_SERVER"]
    username = os.environ["AZURE_SQL_USERNAME"]
    password = '{' + os.environ["AZURE_SQL_PASSWORD"] + '}'

    try:
        youtube_script.update_db(api_key, server, username, password)
        logging.info("Update correct.")
    except Exception as error:
        logging.error(f'Update error. {str(error)}')
        raise
