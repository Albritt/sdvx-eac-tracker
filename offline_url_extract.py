from bs4 import BeautifulSoup
import os
import re


def main():
    html_doc = []
    with open('html_doc.txt') as file:
        html_doc = file.read()

    soup = BeautifulSoup(html_doc,'html.parser')
    for tag in soup.find_all(class_="music"):
        genre = tag.find(class_=re.compile("genre *")).text
        info = tag.find("div", class_ = "info")
        sub_info = info.p
        title = sub_info.text
        artist = info.find_next("p").find_next("p").text
        levels_dict = {}
        levels = tag.find("div", class_="level")
        for p in levels.find_all("p"):
            diff = p["class"][0].upper()
            level = int(p.get_text(strip=True))
            levels_dict[diff] = level
        ptags = tag.find_all("p")
        pack = ptags[-1].get_text()
        jk_div = tag.find("div", class_ = "jk")
        music_id_url = jk_div.find("a").get('href')
        id_pattern = 'music_id='
        idx = music_id_url.index(id_pattern)
        if idx:
            idx = len(id_pattern) + idx 
            music_id = music_id_url[idx:]
        print(f"Title: {title} ; Artist: {artist} ; Genre: {genre} ; Pack:{pack} ; Levels:{levels_dict}")
        print(f"music_id_url: {music_id_url}")
        print(f"music_id: {music_id}")

if __name__ == "__main__":
    main()