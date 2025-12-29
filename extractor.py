import requests
import os


def main():
    url = 'https://p.eagate.573.jp/game/eacsdvx/vi/music/index.html'
    cookies = r'visid_incap_2730193=j+sQgUFrQzW3spE/vPF+Rk0h52gAAAAAQUIPAAAAAACziLLRZcEiB9pERwiHsuVo; visid_incap_2775444=EMa9E3JqSyyCxbsYJZlZxlz4SmkAAAAAQUIPAAAAAAAlmTRzioxRzdOMttzvUEAn; _rslgvry=999db49f-65a6-490f-8d61-264796b6814f; M573SSID=f694bbbf-aa12-4688-8a94-451c805546c8; nlbi_2775444=IAARNyp1K1wrsJP38yJJLQAAAAB3gAOw1n8mpsoOFeekn/9M; incap_ses_236_2775444=QW9bfx8FsG0v+Aa1PXFGAz9qUWkAAAAAgIwWHZgB4W7kEFEMjjUq9Q=='
    payload = {'search_category': '', 'search_name': '', 'search_level': '13', 'search_condition': '', 'page': '2'}
    headers = { 'host': 'p.eagate.573.jp',
                'origin': 'https://p.eagate.573.jp',
                'referer': 'https://p.eagate.573.jp/game/eacsdvx/vi/music/index.html',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'}
    session = requests.Session()
    session.get(url=url, headers=headers)
    response = session.post(url=url, data=payload)

    response.encoding = 'utf-8'
    print(response.text)



if __name__ == "__main__":
    main()