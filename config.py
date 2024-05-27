import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

TOKEN = os.environ.get("TOKEN")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
ADMIN_ID = ["277500369343610880", "193033705411969024", "175633545660858368"]


conn = psycopg2.connect(
    database="secrets", host="localhost", user=DB_USER, password=DB_PASS, port=DB_PORT
)
cursor = conn.cursor()
