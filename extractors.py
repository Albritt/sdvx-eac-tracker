from __future__ import annotations
from PIL import Image
import csv
import pytesseract
from pathlib import Path
from config import load_config
config = load_config()

def extract_scores(path:str|Path):
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
                row[config['csv']['song_title']] = score['title']
            if config['csv']['artist']:
                row[config['csv']['artist']] = score['artist']
            if config['csv']['level']:
                row[config['csv']['level']] = score['level']
            if config['csv']['difficulty']:
                row[config['csv']['difficulty']] = score['difficulty']
            if config['csv']['score']:
                row[config['csv']['score']] = score['score']
            if config['csv']['exscore']:
                row[config['csv']['exscore']] = score['exscore']
            scores.append(score)
    return scores

def extract_img(path: Path):
    title_coords = (385, 995, 895, 1027)
    artist_coords = (385, 1030, 895, 1062)
    score_coords = (420, 1065, 807, 1123) 
    
    img = Image.open('sv6c_BryONPDgWT.jpg')
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

