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

Search_Keyward = "노트북"

@pytest.mark.usefixtures("measure_time", "driver")
class TestMainPage:
    def test_open_main_page(self,driver):
        main_page = MainPage(driver)
        main_page.open()
        time.sleep(2)
        ws(driver, 10).until(EC.url_contains("coupang.com"))
        assert "coupang.com" in driver.current_url  #url에 coupang.com이 있는지 확인 테스트
        time.sleep(2)

    def test_search_without_login(self,driver):
        main_page = MainPage(driver)
        main_page.open()
        time.sleep(2)
        main_page.search_items(Search_Keyward)
        time.sleep(3)
        without_login_result = main_page.products_name()
        assert len(without_login_result) > 0 #제품명이 1개 이상인지 테스트
        assert len(without_login_result) == 5 # 제품명이 5개인지 테스트

    #@pytest.mark.usefixtures("login_function")
    def test_search_with_login(self,driver):
        print("hi")