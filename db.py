import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from datetime import datetime

def add_score(song_title: str, artist: str, grade: str, medal: str, achieved_time: datetime , clear_type: str):
    with sqlite3.connect("sdvxkonasute.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO scores(chart_id, score, medal, achieved_at, ex_score)")

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

def populate_tables(music: dict, charts: dict):
    chart_df = pd.DataFrame(charts)
    music_df = pd.DataFrame(music) 

    engine = create_engine(f"sqlite:///sdvxkonasute.db")

    chart_df.to_sql(name="charts", con=engine, if_exists='replace', index=False)
    music_df.to_sql(name="music", con=engine, if_exists='replace', index=False)