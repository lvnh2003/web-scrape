from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Union, Optional, List

def extract_element(driver: WebDriver, selector_config: Union[str, dict]) -> Optional[Union[str, List[str]]]:
    try:
        if isinstance(selector_config, str):
            element = driver.find_element(By.XPATH, selector_config)
            return element.get_attribute("innerText").strip()

        if "sub_elements" in selector_config:
            texts = []
            for sub in selector_config["sub_elements"]:
                elements = driver.find_elements(By.XPATH, sub["xpath"])
                texts += [el.get_attribute("innerText").strip() for el in elements if el.get_attribute("innerText")]
            return texts if texts else None

        if "xpath" in selector_config:
            if selector_config.get("is_multi"):
                elements = driver.find_elements(By.XPATH, selector_config["xpath"])
                return [el.get_attribute("innerText").strip() for el in elements if el.get_attribute("innerText")]
            else:
                element = driver.find_element(By.XPATH, selector_config["xpath"])
                return element.get_attribute("innerText").strip()

    except Exception:
        return None
