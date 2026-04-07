from __future__ import annotations
from typing import Any
from PIL import Image
import csv
import pytesseract
from pathlib import Path
from config import load_config
config = load_config()

def extract_scores(path:str|Path) -> dict[str, Any]:
    path = Path(path)
    if path.is_dir():
        extract_img(path)
    name,ext=path.split('.')
    extractor = SCORE_EXTRACTORS.get(ext.lower())
    if extractor:
        scores = extractor(path)
        return scores
    else:
        raise NotImplementedError()

def extract_csv(path:Path):
    scores = []
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            score = {}
            if config['csv']['song_title']:
                score['title'] = row[config['csv']['song_title']]
            if config['csv']['artist']:
                score['artist'] = row[config['csv']['artist']]
            if config['csv']['level']:
                score['level'] = row[config['csv']['level']]
            if config['csv']['difficulty']:
                score['difficulty'] = row[config['csv']['difficulty']]
            if config['csv']['score']:
                score['score'] = row[config['csv']['score']]
            if config['csv']['exscore']:
                score['exscore'] = row[config['csv']['exscore']]
            if config['csv']['medal']:
                score['medal'] = row[config['csv']['medal']]
            if config['csv']['achieved_at']:
                score['csv'] = row[config['csv']['achieved_at']]
            scores.append(score)
    return scores

def extract_img(path: Path):
    title_coords = (385, 995, 895, 1027)
    artist_coords = (385, 1030, 895, 1062)
    score_coords = (420, 1065, 807, 1123) 
    
    for file in list(path.glob('**/*.png')):
        img = Image.open(file)
        img = img.transpose(Image.ROTATE_270)
        cropped_img = img.crop(score_coords)
        extracted_title = pytesseract.image_to_string(cropped_img,lang='jpn')
        #img = pytesseract.image_to_string(img,lang='eng+jpn')
        print(extracted_title)
        #print(img)
        cropped_img.save('new.jpg')
    
def extract_json(path:Path):
    raise NotImplementedError()

def extract_txt(path:Path):
    raise NotImplementedError()
SCORE_EXTRACTORS = {
        '.txt' : extract_txt,
        '.csv' : extract_csv,
        '.json': extract_json
}

