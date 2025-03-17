import pytest
import time
from selenium.webdriver.common.by import By
from urllib import parse
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver # noqa
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from ..pages.tc_01_search_item import MainPage
from selenium.webdriver.common.keys import Keys

@pytest.mark.usefixtures("measure_time", "driver")
class TestMainPage:
    def test_open_main_page(self,driver):
        main_page = MainPage(driver)
        main_page.open()
        time.sleep(2)
        ws(driver, 10).until(EC.url_contains("coupang.com")) #url에 coupang.com이 있는지 확인 테스트
        assert "coupang.com" in driver.current_url
        time.sleep(2)

    def test_search_without_login(self,driver):
        main_page = MainPage(driver)
        main_page.open()
        time.sleep(2)
        main_page.search_items("김치만두")
        time.sleep(3)
        without_login_result = main_page.products_name()
        print(without_login_result)
