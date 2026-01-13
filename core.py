from config import load_config
from scraper import scrape_sdvx


def main():
    config = load_config()
    songs = scrape_sdvx(url=config['site_url'], headers=config['session_headers'], domain_name=config['domain_name'])

if __name__ == "__main__":
    main()