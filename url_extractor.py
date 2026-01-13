import requests
from bs4 import BeautifulSoup, Tag
from requests_ratelimiter import LimiterSession
from typing import Any
import re
import os
import json

def add_jackets_to_charts(charts: dict, urls: list):
    for idx, value in enumerate(charts.values()):
        value['jacket_url'] = urls[idx]

def parse_song_results(text: str, domain_name: str, headers: dict) -> list[dict]:
    metadata = []
    soup = BeautifulSoup(text, 'html.parser')
    if soup.find(class_="music"):
       for tag in soup.find_all(class_="music"):
           song_data = get_song_metadata(tag)
           subpage = get_song_subpage(song_data['music_id_url'], domain_name)
           jacket_urls = get_song_jacket_urls(subpage, domain_name)
           add_jackets_to_charts(song_data,jacket_urls)
       return metadata
    return []

def get_song_jacket_urls(text: str, domain_name: str) -> list:
    soup = BeautifulSoup(text, 'html.parser')
    sub_tags = []
    for sub_tag in soup.find_all(class_="jk"):
        sub_tags.append(domain_name + str(sub_tag.find("img").get("src")))
    return sub_tags

def get_song_metadata(tag: Tag) -> dict[str, Any]:
    genre = tag.find(class_=re.compile("genre *")).text
    info = tag.find("div", class_ = "info")
    title = info.find_next("p").text
    artist = info.find_next("p").find_next("p").text
    charts = get_charts(tag)
    pack = tag.find_all("p")[-1].get_text()
    music_id_url = get_music_id_url()
    music_id = get_music_id(music_id_url)

    return {
            'title': title,
            'artist': artist,
            'genre': genre,
            'pack': pack,
            'music_id': music_id,
            'music_id_url': music_id_url,
            'charts': charts   #Refactor levels to charts  
            }

def get_song_subpage(url:str, domain_name: str, headers:dict) -> str:
    session = LimiterSession(per_second=1)
    response = session.get(url=domain_name + url, headers=headers)
    response.encoding = 'utf-8'
    return response.text

def get_charts(tag: Tag) -> dict[str, dict[str, int]]:
    charts: dict[str,dict[str, int]] = {}
    charts_tag = tag.find("div", class_="level")
    for p in charts_tag.find_all("p"):
        diff = p["class"][0].upper()
        chart_level = int(p.get_text(strip=True))
        charts[diff] = {'level' : chart_level}
    return charts

def get_music_id(music_id_url: str):
    id_pattern = 'music_id='
    idx = music_id_url.index(id_pattern)
    if idx:
        idx = len(id_pattern) + idx 
        return music_id_url[idx:]

def get_music_id_url(tag: Tag) -> str:
    jk_div = tag.find("div", class_ = "jk")
    return str(jk_div.find("a").get('href'))



def scrape_sdvx(url: str, headers:dict, domain_name: str, 
                max_page: int|None = None, search_name: str = '',
                search_level: int|None = None,  pack_name: str = '')->list[dict]:
    session = LimiterSession(per_second=1)
    session.get(url=url, headers=headers)

    page = 1
    empty_page = False
    songs = []
    if search_level is None:
        search_level = ''
    while empty_page is False:
        payload = {'search_category': '', 'search_name': search_name,
         'search_level': str(search_level), 'search_condition': pack_name, 'page': page}
        response = session.post(url=url, data=payload)
        response.encoding = 'utf-8'
        data = parse_song_results(response.text, domain_name)
        if data:
            for song in data:
                songs.extend(song)
            page+=1
        else:
            empty_page = True
        if max_page:
            if page > max_page:
                break
    return songs


if __name__ == "__main__":
    scrape_sdvx()