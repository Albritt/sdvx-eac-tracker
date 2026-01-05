import requests
from bs4 import BeautifulSoup, Tag
from requests_ratelimiter import LimiterSession
from typing import Any
import re
import os
import json

base_url = 'https://p.eagate.573.jp/'

def parse_music_results(text: str) -> list[dict]:
    metadata = []
    soup = BeautifulSoup(text, 'html.parser')
    if soup.find(class_="music"):
       for tag in soup.find_all(class_="music"):
           #metadata.append(get_song_metadata(tag))
           data = get_song_metadata(tag)
           response = get_song_subpage(data['music_id_url'])
           soup = BeautifulSoup(response, 'html.parser')
       return metadata
    return []

def get_song_metadata(tag: Tag) -> dict[str, Any]:
    genre = tag.find(class_=re.compile("genre *")).text
    info = tag.find("div", class_ = "info")
    title = info.find_next("p").text
    artist = info.find_next("p").find_next("p").text
    levels = get_levels(tag)
    pack = tag.find_all("p")[-1].get_text()
    music_id_url = get_music_id_url()
    music_id = get_music_id(music_id_url)


    session = LimiterSession(per_second=1)
    headers = { 'host': 'p.eagate.573.jp',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'}
    response = session.get(url=base_url + music_id_url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response, 'html.parser')
    sub_tags = []
    for sub_tag in soup.find_all(class_="jk"):
        sub_tags.append(sub_tag.find("img").get("src"))
    for idx, value in enumerate(levels.values()):
        value.append(sub_tags[idx])
    return {
            'title': title,
            'artist': artist,
            'genre': genre,
            'pack': pack,
            'music_id': music_id,
            'music_id_url': music_id_url,
            'levels': levels   #Refactor levels to charts  
            }

def get_song_subpage(url:str) -> str:
    session = LimiterSession(per_second=1)
    headers = { 'host': 'p.eagate.573.jp',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'}
    response = session.get(url=base_url + url, headers=headers)
    response.encoding = 'utf-8'
    return response.text

def get_levels(tag: Tag) -> dict[str, list]:
    levels: dict[str,list] = {}
    levels_tag = tag.find("div", class_="level")
    for p in levels_tag.find_all("p"):
        diff = p["class"][0].upper()
        level = int(p.get_text(strip=True))
        levels[diff] = [level]
    return levels

def get_music_id(music_id_url: str):
    id_pattern = 'music_id='
    idx = music_id_url.index(id_pattern)
    if idx:
        idx = len(id_pattern) + idx 
        return music_id_url[idx:]

def get_music_id_url(tag: Tag) -> str:
    jk_div = tag.find("div", class_ = "jk")
    return str(jk_div.find("a").get('href'))






def main():
    url = url = 'https://p.eagate.573.jp/game/eacsdvx/vi/music/index.html'
    payload = {'search_category': '', 'search_name': '', 'search_level': '13', 'search_condition': '', 'page': '2'}
    headers = { 'host': 'p.eagate.573.jp',
                'origin': 'https://p.eagate.573.jp',
                'referer': 'https://p.eagate.573.jp/game/eacsdvx/vi/music/index.html',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'}
    session = LimiterSession(per_second=1)
    session.get(url=url, headers=headers)

    page = 1
    empty_page = False
    songs = []
    while empty_page is False:
        payload = {'search_category': '', 'search_name': '', 'search_level': '', 'search_condition': '', 'page': page}
        response = session.post(url=url, data=payload)
        response.encoding = 'utf-8'
        data = parse_music_results(response.text)
        if data:
            for song in data:
                songs.extend(song)
            page+=1
        else:
            empty_page = True


if __name__ == "__main__":
    main()