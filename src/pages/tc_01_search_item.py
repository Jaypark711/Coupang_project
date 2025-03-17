from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import time
class MainPage:
    Main_URL = "https://www.coupang.com"
    SEARCH_INPUT = "headerSearchKeyword"

    def __init__(self, driver):
        self.driver = driver

    def open_main(self):
        self.driver.get(self.Main_URL)
    
    def search_items(self, item_name: str):
        search_input_box = self.driver.find_element(By.ID,self.SEARCH_INPUT)
        search_input_box.send_keys(item_name)
        search_input_box.send_keys(Keys.ENTER)

    def products_name(self):
        products = self.driver.find_elements(By.CLASS_NAME,"name")
        products_name = []
        for product in products[:5]:            #Top 5 가져오기
            products_name.append(product.text)
        return products_name