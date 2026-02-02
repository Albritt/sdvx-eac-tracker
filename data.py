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

def make_jacket_paths(song_path: Path, charts:dict[str,dict[str,str|int]]):
    for diff_name in charts.keys():
        jacket_path = Path(f"{song_path}/{diff_name}.jpg")
        if jacket_path.is_file():
            continue
        else:
            write_jacket(jacket_path, charts[diff_name]['jacket_url'])

def write_jacket(jacket_path: Path, jacket_url:str):
    jacket_path.parent.mkdir(parents=True,exist_ok=True)
    content = request_jacket(jacket_url)
    with open(jacket_path, 'wb') as jacket:
        jacket.write(content)


