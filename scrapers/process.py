from selenium.webdriver.common.by import By
from .driver import create_chrome_driver
from .extractor import extract_element
from utils.function import random_delay

class WebScraper:
    def __init__(self, config: dict):
        self.config = config
        self.driver = create_chrome_driver()

    def scrape(self):
        self.driver.get(self.config["start_url"])
        random_delay()
        results = []

        while True:
            print("現在処理中のURL:", self.driver.current_url)

            for link in self._get_job_links():
                print(f"   データ取得中: {link}")
                self.driver.get(link)
                random_delay()
                detail = self._get_job_detail(link)
                results.append(detail)
                self.driver.back()
                random_delay()

            if not self._go_to_next_page():
                break

        self.driver.quit()
        return results

    def _get_job_links(self):
        elements = self.driver.find_elements(By.XPATH, self.config["item_selector"])
        return [el.get_attribute("href") for el in elements if el.get_attribute("href")]

    def _get_job_detail(self, link):
        detail = {"url": link}
        for key, selector in self.config["detail_selectors"].items():
            detail[key] = extract_element(self.driver, selector)
        return detail

    def _go_to_next_page(self):
        try:
            next_btn = self.driver.find_element(By.XPATH, self.config["next_button_selector"])
            outer_html = next_btn.get_attribute("outerHTML")

            if "disabled" in outer_html or 'aria-disabled="true"' in outer_html:
                print("最終ページに到達しました。")
                return False

            next_btn.click()
            random_delay()
            return True
        except Exception as e:
            print("「次へ」ボタンが見つからない、またはクリックできません:", str(e))
            return False
