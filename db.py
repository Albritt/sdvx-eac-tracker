import pandas as pd
import sqlite3
from sqlalchemy import create_engine


def setup_db():
    conn = sqlite3.connect("sdvxkonasute.db")
    cursor = conn.cursor()
    table_names = ['music', 'charts', 'scores']
    for table in table_names:
        with open(f"tables/{table}.sql", 'r') as sql_file:
            sql = sql_file.read()
        cursor.executescript(sql)
        conn.commit()
    conn.close()

