from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def init_selenium_browser():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shim-usage")
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    options.add_argument("window-size=1920x1080")

    browser = webdriver.Chrome(options=options)

    return browser
