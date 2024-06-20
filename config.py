import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

TOKEN = os.environ.get("TOKEN")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
CHANNEL = int(os.environ.get("CHANNEL"))
ADMIN_ID = [int(id) for id in os.environ.get("ADMIN_ID").split(", ")]
IS_EVENT_ON = False

conn = psycopg2.connect(
    database="secrets", host="localhost", user=DB_USER, password=DB_PASS, port=DB_PORT
)
cursor = conn.cursor()

cursor.execute(
    "SELECT EXISTS (SELECT 1 AS result FROM pg_tables WHERE tablename = 'users');"
)
tableExists = cursor.fetchone()[0]

if not tableExists:
    cursor.execute(
        "CREATE TABLE users (id serial PRIMARY KEY, user_id varchar, number_secrets integer);"
    )
    cursor.execute(
        "CREATE TABLE secrets (id serial PRIMARY KEY, secret text, available bool, user_id int REFERENCES users (id));"
    )
    cursor.execute("CREATE TABLE event (id serial PRIMARY KEY, is_event_on bool);")
    cursor.execute("INSERT INTO event (is_event_on) VALUES (%s);", [False])
    conn.commit()
