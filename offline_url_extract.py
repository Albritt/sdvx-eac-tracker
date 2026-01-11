from bs4 import BeautifulSoup
from collections import namedtuple
import os
import re

base_url = 'https://p.eagate.573.jp'

def main():
    Song = namedtuple('Song', ['title', 'artist', 'genre', 'pack', 'music_id', 'charts'])
    html_doc = []
    with open('html_doc.txt') as file:
        html_doc = file.read()

    songs:list[Song] = []
    soup = BeautifulSoup(html_doc,'html.parser')
    for tag in soup.find_all(class_="music"):
        genre = tag.find(class_=re.compile("genre *")).text
        info = tag.find("div", class_ = "info")
        sub_info = info.p
        title = info.find_next("p").text
        artist = info.find_next("p").find_next("p").text
        charts: dict[str,dict[str, int]] = {}
        charts_tag = tag.find("div", class_="level")
        for p in charts_tag.find_all("p"):
            diff = p["class"][0].upper()
            chart_level = int(p.get_text(strip=True))
            charts[diff] = {'level' : chart_level}
        ptags = tag.find_all("p")
        pack = ptags[-1].get_text()
        jk_div = tag.find("div", class_ = "jk")
        music_id_url = jk_div.find("a").get('href')
        id_pattern = 'music_id='
        idx = music_id_url.index(id_pattern)
        if idx:
            idx = len(id_pattern) + idx 
            music_id = music_id_url[idx:]
        sub_doc = []
        with open('html_sub_doc.txt') as file:
            sub_doc = file.read()
        sub_soup = BeautifulSoup(sub_doc, 'html.parser')
        sub_tags = []
        for sub_tag in sub_soup.find_all(class_="jk"):
            sub_tags.append(base_url + str(sub_tag.find("img").get("src")))
        for idx, value in enumerate(charts.values()):
            value['jacket_url'] = sub_tags[idx]


        #print(f"Title: {title} ; Artist: {artist} ; Genre: {genre} ; Pack:{pack} ; Levels:{levels_dict}")
        #print(f"music_id_url: {music_id_url}")
        #print(f"music_id: {music_id}")
        songs.append(Song(title, artist, genre, pack, music_id, charts))
    
    for song in songs:
        print(song)

if __name__ == "__main__":
    main()