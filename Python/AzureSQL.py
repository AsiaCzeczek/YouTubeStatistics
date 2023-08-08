import pyodbc
from dotenv import dotenv_values

secrets = dotenv_values(".env")

server = secrets["AZURE_SQL_SERVER"]
username = secrets["AZURE_SQL_USERNAME"]
password = '{' + secrets["AZURE_SQL_PASSWORD"] + '}'

database = 'YoutubeStats'
driver = "{ODBC Driver 17 for SQL Server}"

with pyodbc.connect('DRIVER= '+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM dbo.Videos")
        row = cursor.fetchone()
        while row:
            print (row)
            row = cursor.fetchone()