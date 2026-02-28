import json
from pathlib import Path
from typing import Any
from scraper import request_jacket


def write_to_json(songs:list[dict], base_dir: str = "") -> None:
    if base_dir == "":
        path = "./data/sdvx_data.json"
        output_file = Path(path)
    else:
        path = base_dir + "/data/sdvx_data.json"
        output_file = Path(path)
    output_file.parent.mkdir(parents=True,exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(songs, file, ensure_ascii=False, indent=2)

def read_from_json(base_dir: str = "") -> list[dict[str, Any]]:
    #TODO:Need to handle the case where this is called and there is nothing to return
    if base_dir == "":
        path = "./data/sdvx_data.json"
        input_file = Path(path)
    else:
        path = base_dir + "/data/sdvx_data.json"
        input_file = Path(path)
    with open(input_file, 'r') as file:
        data = json.load(file)
        return data
    
def update_jackets(songs:list[dict[str, Any]], base_dir:str = ""):
    if base_dir == "":
        path ="./data/jackets/"
    else:
        path = base_dir + "/data/jackets/"
    for song in songs:
        music_folder_path = Path(path + song['music_id'])
        make_jacket_paths(music_folder_path, song['charts'])

def make_jacket_paths(song_path: Path, charts:dict[str,dict]):
    for diff_name in charts.keys():
        jacket_path = Path(f"{song_path}/{diff_name}.jpg")
        charts[diff_name]['jacket_path'] = str(jacket_path)
        if jacket_path.is_file():
            continue
        else:
            write_jacket(jacket_path, charts[diff_name]['jacket_url'])

def write_jacket(jacket_path: Path, jacket_url:str):
    #TODO: Should have try around writing to filesystem
    jacket_path.parent.mkdir(parents=True,exist_ok=True)
    content = request_jacket(jacket_url)
    with open(jacket_path, 'wb') as jacket:
        jacket.write(content)


def normalize_data(songs:list[dict[str, Any]]):
    charts = []
    music = []
    for song in songs:
        music.append(extract_music(song))
        charts.extend(extract_charts(song['charts'], song['music_id']))
    return (music, charts)   

def extract_music(song:dict[str, Any]):
    music_dict = {}
    music_dict['music_id'] = song['music_id']
    music_dict['title'] = song['title']
    music_dict['artist'] = song['artist']
    music_dict['genre'] = song['genre']
    music_dict['pack'] = song['pack']
    return music_dict

def extract_charts(charts:dict[str,dict], music_id:str):
    difficulties = []
    for diff_name in charts.keys():
        chart_dict = {}
        chart_dict['chart_id'] = charts[diff_name]['chart_id']
        chart_dict['music_id'] = music_id
        chart_dict['level'] = charts[diff_name]['level']
        chart_dict['difficulty'] = diff_name
        chart_dict['jacket_path'] = charts[diff_name]['jacket_path']
    difficulties.append(chart_dict)
    return difficulties