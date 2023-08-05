from .config import config
from selenium import webdriver


user_agent = "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"


def get():
    """Initializes chromedriver"""
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--lang=en-us")
    # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument(user_agent)

    # prefs = {"profile.default_content_setting_values.notifications": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(config.chrome_driver, chrome_options=chrome_options)
    return driver
