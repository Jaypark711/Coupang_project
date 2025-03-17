# Coupang Project

## 📌 프로젝트 개요
이 프로젝트는 Selenium과 pytest를 활용해 쿠팡 웹페이지의 일부 기능을 테스트하는 자동화 스크립트입니다.

## ✨주요 특징
### 📄POM (page object model)
페이지 요소와 동작을 분리해 **재사용성, 유지보수성, 가독성, 확장성**을 높입니다.
### ♾️pytest.fixture
Webdriver 세션을 효율적으로 **재사용**합니다.
### 📝Report
report 기능으로 테스트 결과를 받아볼 수 있습니다.

## 📂 프로젝트 구조

```plaintext
Coupang_project/
│── conftest.py
│── report.html
│── src/
│   ├── __init__.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── tc_01_search_item.py
│   │   ├── tc_02_put_cart.py
│   │   ├── tc_03_change_option.py
│   │   ├── tc_04_search_filter.py
│   │   ├── tc_05_hotprice_page.py
│   │   ├── tc_06_recent_list.py
│   ├── test/
│   │   ├── __init__.py
│   │   ├── test_01_search_item.py
│   │   ├── test_02_put_cart.py
│   │   ├── test_03_change_option.py
│   │   ├── test_04_search_filter.py
│   │   ├── test_05_hotprice_page.py
│   │   ├── test_06_recent_list.py
│── .venv/
```

📄**conftest.py**<br>
환경 설정 및 공통 설정 파일을 담은 스크립트입니다. <br>
`@pytest.fixture` 을 통해 호출됩니다. <br>
📄**report.html**<br>
테스트 이후 `--html=report.html` 을 이용해 결과를 확인할 수 있습니다.<br>
📂**pages/**<br>
동작을 스크립트로 정의합니다.<br> 
직접 실행되지는 않습니다.<br>
📂**tests/**<br>
pages 폴더 내의 파일을 `pytest`를 통해 테스트합니다.
## 🛠 기술 스택
- **Python** 3.x
- **Selenium WebDriver**
- **pytest**
- **ChromeDriver**

## 🏃‍♂️ 실행 방법

### 1️⃣ 패키지 설치
```bash
pip install pytest
pip install pytest-html
pip install selenium
```

### 2️⃣ 테스트 실행
```bash
pytest src/test --html=report.html
```

### 3️⃣테스트 리포트 확인
테스트 실행 후 생성된 `report.html` 파일을 열어 결과 확인