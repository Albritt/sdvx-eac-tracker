from config import load_config
from scraper import scrape_sdvx
from data import write_to_json, read_from_json, update_jackets, normalize_data
from db import setup_db, populate_tables
import pandas as pd
import psycopg
from sqlalchemy import create_engine
from pathlib import Path

def main():
    config = load_config()
    #songs = scrape_sdvx(url=config['site_url'], headers=config['session_headers'], domain_name=config['domain_name'],max_page=1)
    #write_to_json(songs, config['home_dir'] )
    songs = read_from_json(config['home_dir'])
    update_jackets(songs, config['home_dir'])
    music, charts = normalize_data(songs)
    

    chart_df = pd.DataFrame(charts)
    music_df = pd.DataFrame(music) 
    if Path('sdvxkonasute.db').is_file() is False:
        setup_db()
    populate_tables(music, charts)
    #new_songs = read_from_json(config['home_dir'])

if __name__ == "__main__":
    main()
