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
        for diff_name in dict(song['charts']).keys():
            jacket_path = Path(f"{music_folder_path}/{diff_name}.jpg")
            if jacket_path.is_file():
                continue
            else:
                jacket_url = song['charts'][diff_name]['jacket_url']
                jacket_path.parent.mkdir(parents=True, exist_ok=True)
                content = request_jacket(jacket_url)
                with open(jacket_path, 'wb') as jacket:
                    jacket.write(content)


