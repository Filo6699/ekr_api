import mysql.connector
from decouple import config as env

mydb = mysql.connector.connect(
    **{
        "user": env("SQL_USER"),
        "password": env("SQL_PASSWORD"),
        "host": env("SQL_HOST"),
        "port": env("SQL_PORT", 3306),
    }
)

mycursor = mydb.cursor()
mycursor.execute("DROP DATABASE IF EXISTS ekr_api;")
mycursor.execute("CREATE DATABASE ekr_api")

mydb.commit()
mydb.close()
