import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default="chrome",
                 help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default="en",
                 help="Choose language: ru, en or another")


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language") #узнаём язык, если не указан
    if browser_name == "chrome": #chrome
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language}) 
        print("\n* * * STARTING CHROME * * *")
        browser = webdriver.Chrome(options=options) #задаем нужный язык
    elif browser_name == "firefox": #firefox
        fp = webdriver.FirefoxProfile()
        fp.set_preference("intl.accept_languages", user_language) #задаем нужный язык
        print("\n* * * STARTING FIREFOX * * *")
        browser = webdriver.Firefox(firefox_profile=fp)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield browser
    browser.implicitly_wait(10)
    print("\n* * * CLOSING BROWSER * * *")
    browser.quit()