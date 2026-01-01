import requests
from bs4 import BeautifulSoup
import os


def main():
    url = 'https://p.eagate.573.jp/game/eacsdvx/vi/music/index.html'
    payload = {'search_category': '', 'search_name': '', 'search_level': '13', 'search_condition': '', 'page': '2'}
    headers = { 'host': 'p.eagate.573.jp',
                'origin': 'https://p.eagate.573.jp',
                'referer': 'https://p.eagate.573.jp/game/eacsdvx/vi/music/index.html',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'}
    session = requests.Session()
    session.get(url=url, headers=headers)
    response = session.post(url=url, data=payload)

    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup.prettify())

    #print(soup.find_all('div', id='music-result'))

    for tag in soup.find_all('div', id='music-result'):
        print(f'Tag: {tag}')
    #    print(song_title.get('p'))



if __name__ == "__main__":
    main()