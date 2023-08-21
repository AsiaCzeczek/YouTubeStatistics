import logging
import azure.functions as func
from dotenv import dotenv_values

secrets = dotenv_values(".env")
secret_val = secrets["SECRET_1"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This is kitek!" + secret_val,
             status_code=200
        )
