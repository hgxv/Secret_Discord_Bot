import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
TOKEN = os.environ.get("TOKEN")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")


conn = psycopg2.connect(
    database="secrets", host="localhost", user=DB_USER, password=DB_PASS, port=DB_PORT
)
cursor = conn.cursor()
