from config import load_config
from scrapers import WebScraper
from utils.function import save_to_csv, save_to_json
def main():
    all_config = load_config()
    config = all_config["website"]

    scraper = WebScraper(config)
    results = scraper.scrape()
    save_to_json(results, "rikunabi_jobs.json")

if __name__ == "__main__":
    main()
