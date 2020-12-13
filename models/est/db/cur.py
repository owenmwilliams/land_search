import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
version = os.getenv("version")
db = version.replace('.','')

def con_cur():
    con = psycopg2.connect(database=db, host="localhost", port="5432")
    cur = con.cursor()
    return cur, con
    