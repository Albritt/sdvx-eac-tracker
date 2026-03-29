from __future__ import annotations
from PIL import Image
import pytesseract
from pathlib import Path

def extract_scores(path:str|Path, **kwargs):
    path = Path(path)
    if path.is_dir():
        extract_img(path)
    name,ext=path.split('.')
    extractor = SCORE_EXTRACTORS.get(ext.lower())
    if extractor:
        scores = extractor(filepath, kwargs)
    else:
        raise NotImplementedError()

def extract_csv(path:Path):
        raise NotImplementedError()

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

