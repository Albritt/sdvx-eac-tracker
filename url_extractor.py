import requests
from bs4 import BeautifulSoup, Tag
from requests_ratelimiter import LimiterSession
import re
import os

def get_songs_data(text: str) -> dict:
    soup = BeautifulSoup(text)
    if soup.find(class_="music"):
       for tag in soup.find_all(class_="music"):
           get_song_metadata(tag)
           
       return {}
    return {}

def get_song_metadata(tag: Tag):
    genre = tag.find(class_=re.compile("genre *")).text
    info = tag.find("div", class_ = "info")
    title = info.find_next("p").text
    artist = info.find_next("p").find_next("p").text
    levels = get_levels(tag)
    pack = tag.find_all("p")[-1].get_text()
    music_id = get_music_id()

def get_levels(tag: Tag) -> dict[str, list]:
    levels: dict[str,list] = {}
    levels_tag = tag.find("div", class_="level")
    for p in levels_tag.find_all("p"):
        diff = p["class"][0].upper()
        level = int(p.get_text(strip=True))
        levels[diff] = [level]
    return levels

def get_music_id(tag: Tag):
    jk_div = tag.find("div", class_ = "jk")
    music_id_url = jk_div.find("a").get('href')
    id_pattern = 'music_id='
    idx = music_id_url.index(id_pattern)
    if idx:
        idx = len(id_pattern) + idx 
        return str(music_id_url[idx:])
    return ""





def main():
    url = 'https://p.eagate.573.jp/game/eacsdvx/vi/music/index.html'
    payload = {'search_category': '', 'search_name': '', 'search_level': '13', 'search_condition': '', 'page': '2'}
    headers = { 'host': 'p.eagate.573.jp',
                'origin': 'https://p.eagate.573.jp',
                'referer': 'https://p.eagate.573.jp/game/eacsdvx/vi/music/index.html',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'}
    session = LimiterSession(per_second=1)
    session.get(url=url, headers=headers)

    page = 1
    empty_page = False
    songs = {}
    while empty_page is False:
        payload = {'search_category': '', 'search_name': '', 'search_level': '', 'search_condition': '', 'page': page}
        response = session.post(url=url, data=payload)
        response.encoding = 'utf-8'
        data = get_songs_data()
        if data:
            songs.update(data)
            page+=1
        else:
            empty_page = True


if __name__ == "__main__":
    main()