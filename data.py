import json
from pathlib import Path
from typing import Any


def write_to_json(songs:list[dict], base_dir: str = ""):
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