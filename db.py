import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from datetime import datetime

#TODO: Maybe use Decimal instead of float for max?, also maybe use a dict instead
def add_score(song_title: str, artist: str, level:int, diff:str, score: int, exscore:int, max_score: float|None = None,
              medal: str|None = None, achieved_time: datetime|None = None , clear_type: str|None = None):
    chart_id = get_chart_id(song_title, artist, level, diff)
    with sqlite3.connect("sdvxkonasute.db") as conn:
        cursor = conn.cursor()
        cursor.execute(r"""INSERT INTO scores(chart_id, score, medal, achieved_at, exscore, max_score, medal, clear_type)
                            values (?, ?, ?, ?, ?, ?, ?, ?) """,(chart_id, score, medal, achieved_time, exscore, max_score, medal, clear_type))

def get_chart_id(song_title:str, artist:str, level:int, diff:str) -> int:
    with sqlite3.connect("sdvxkonasute.db") as conn:
        cursor = conn.cursor()
        cursor.execute(r"""SELECT charts.chart_id
                            FROM charts
                            INNER JOIN music ON music.music_id = charts.music_id
                            WHERE music.title = ? AND music.artist = ?
                            AND charts.level = ? AND charts.difficulty = ?""", (song_title, artist, level, diff))
        row = cursor.fetchone()
        return(row.chart_id)

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
