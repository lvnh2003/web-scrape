from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils.function import random_delay
import tempfile

class WebScraper:
    def __init__(self, config):
        self.config = config
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        user_data_dir = tempfile.mkdtemp()
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape(self):
        self.driver.get(self.config["start_url"])
        random_delay()
        results = []

        while True:
            print("現在処理中のURL:", self.driver.current_url)
            job_links = self._get_job_links()
            for link in job_links:
                random_delay()
                print(f"   データ取得中: {link}")
                detail = self._get_job_detail(link)
                results.append(detail)
                self.driver.back()
                random_delay()
                break;
            break
                
            if not self._go_to_next_page():
                break

        self.driver.quit()
        return results

    def _get_job_links(self):
        job_cards = self.driver.find_elements(By.XPATH, self.config["item_selector"])
        return [card.get_attribute("href") for card in job_cards if card.get_attribute("href")]

    def _get_job_detail(self, link):
        self.driver.get(link)
        detail = {'url': link}
        for key, config in self.config["detail_selectors"].items():
            try:
                if isinstance(config, str):
                    element = self.driver.find_element(By.XPATH, config)
                    detail[key] = element.get_attribute("innerText").strip()
                elif "sub_elements" in config:
                    sub_texts = []
                    for sub in config["sub_elements"]:
                        try:
                            elements = self.driver.find_elements(By.XPATH, sub["xpath"])
                            texts = [el.get_attribute("innerText").strip() for el in elements if el.get_attribute("innerText")]
                            sub_texts.extend(texts)
                        except Exception:
                            continue
                    detail[key] = sub_texts if sub_texts else None
                elif "xpath" in config:
                    if config.get("is_multi"):
                        elements = self.driver.find_elements(By.XPATH, config["xpath"])
                        detail[key] = [el.get_attribute("innerText").strip() for el in elements if el.get_attribute("innerText")]
                    else:
                        element = self.driver.find_element(By.XPATH, config["xpath"])
                        detail[key] = element.get_attribute("innerText").strip()
                else:
                    detail[key] = None
            except Exception:
                detail[key] = None
        return detail

    def _go_to_next_page(self):
        try:
            next_btn = self.driver.find_element(By.XPATH, self.config["next_button_selector"])
            outer_html = next_btn.get_attribute("outerHTML")
            if "disabled" in outer_html or "aria-disabled=\"true\"" in outer_html:
                print("最終ページに到達しました。")
                return False
            print("次のページへ移動します...")
            next_btn.click()
            random_delay()
            return True
        except Exception as e:
            print("「次へ」ボタンが見つからない、またはクリックできません:", str(e))
            return False
        return results
        
    
