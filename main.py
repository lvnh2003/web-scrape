from config import load_config, load_db_config
from scrapers import WebScraper
from utils.function import save_to_csv, save_to_json
from utils.db import insert_data
def main():
    all_config = load_config()
    db_config = load_db_config()
    config = all_config["website"]

    scraper = WebScraper(config)
    results = scraper.scrape()
    table_name = db_config["table_name"]
    insert_data(table_name, results)

if __name__ == "__main__":
    main()
