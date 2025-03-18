# conftest.py
import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import random
import time
import personal_info
from colorama import Fore
import imaplib
import email
from email.header import decode_header
from datetime import datetime
import email.utils
import re

counter = 0


def pytest_configure(config):
    config.option.htmlpath = None

def pytest_report_teststatus(report): # 좀더 깔끔출력 스킬
    if report.when == "call":
        if report.outcome == "passed":
            return "✅", "PASS", "Test passed"
        elif report.outcome == "failed":
            return "❌", "FAIL", "Test failed"
        elif report.outcome == "skipped":
            return "⚠️", "SKIP", "Test skipped"


def get_pass_key(username, password):
    imap_server = "imap.naver.com"
    imap_port = 993
    mail = imaplib.IMAP4_SSL(imap_server, imap_port)
    mail.login(username, password)
    mail.select("INBOX")

    for _ in range(30):  # 최대 30번 반복
        status, messages = mail.search(None, "ALL")  # 메일 목록 다시 가져오기
        email_ids = messages[0].split()
        
        if not email_ids:
            time.sleep(1)
            continue  # 새로운 메일이 없으면 다시 시도
        
        latest_email_id = email_ids[-1]  # 최신 메일 ID 가져오기
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)

        # 제목 및 발신자 확인
        subject, encoding = decode_header(email_message["Subject"])[0]
        subject = subject.decode(encoding if encoding else "utf-8")
        from_ = email_message.get("From")
        
        # 메일 날짜 확인
        date_str = email_message.get("Date")
        send_time = datetime.strptime(
            email.utils.parsedate_to_datetime(date_str).strftime("%Y-%m-%d %H:%M:%S"), 
            "%Y-%m-%d %H:%M:%S"
        )
        current_time = datetime.now()
        diff_date = (current_time - send_time).seconds

        # 메일 본문 가져오기
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()

        # 조건 검사
        if "인증코드 안내메일" in subject and "noreply@coupang.com" in from_ and diff_date <= 20:
            pattern = r'<strong[^>]*>\s*(\d{6})\s*</strong>'
            match = re.search(pattern, body)
            if match:
                pass_key = match.group(1)
                mail.logout()
                return pass_key

        time.sleep(1)  # 1초 대기 후 다시 체크

    mail.logout()
    raise Exception("이메일 인증이 너무 늦었습니다.")



@pytest.fixture
def driver():
    
    # 크롬 옵션 설정
    chrome_options = Options() #쿠팡이 자동화 크롤링 많은 옵션수정이 필요하다..
        # 1) User-Agent 변경
    user_agents = [
    # Add your list of user agents here
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]
    random_user_agent = random.choice(user_agents)
    chrome_options.add_argument(f"user-agent={random_user_agent}")
    # 2) SSL 인증서 에러 무시
    
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")

    # 4) Selenium이 automation된 브라우저임을 숨기는 몇 가지 설정
    #    - (disable-blink-features=AutomationControlled) 제거
    #    - excludeSwitches, useAutomationExtension
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # 혹은 다음 방식으로 Blink 특징을 비활성화할 수도 있으나
    # "AutomationControlled" 자체가 표기되지 않도록 한다.
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-usb-devices")

    # 6) Sandbox나 DevShm 사이즈 문제 우회 (리눅스 환경에서 발생 가능)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # DevTools listening on 스크립트 제거
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 드라이버 객체 생성
    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    driver.execute_cdp_cmd("Network.clearBrowserCache", {})
    driver.delete_all_cookies()
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"Referer": "https://www.coupang.com/"}})
    # 대기시간 설정
    driver.implicitly_wait(5)

    yield driver
    
    # 테스트가 끝나면 드라이버 종료
    driver.quit()


@pytest.fixture
def measure_time(request):
    global counter
    counter += 1
    start_time = time.time()
    yield
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"[{counter}] {Fore.CYAN}{request.node.name}{Fore.RESET} 실행 시간: {Fore.RED}{elapsed_time:.2f} {Fore.RESET}초")

@pytest.fixture
def login_function(driver):
    driver.get("https://www.coupang.com/")
    driver.find_element(By.CLASS_NAME,"login").click()
    time.sleep(3)
    driver.find_element(By.NAME,"email").send_keys(personal_info.ID())
    time.sleep(0.5)
    driver.find_element(By.NAME,"password").send_keys(personal_info.PASSWORD())
    time.sleep(0.5)
    driver.find_element(By.CLASS_NAME,"login__button").click()
    driver.implicitly_wait(5)
    driver.find_element(By.CLASS_NAME,"pincode-select__pincode-verification-type-email").click()
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//button[contains(text(), '인증번호 받기')]").click()
    pass_key = get_pass_key(personal_info.ID(),personal_info.naver_app_password())
    time.sleep(3)
    driver.find_element(By.CLASS_NAME,"pincode-input__pincode-input-box__pincode").send_keys(pass_key)
    time.sleep(1)
    driver.find_element(By.XPATH,"//button[contains(text(), '다음')]").click()
    driver.implicitly_wait(5)
    yield driver
