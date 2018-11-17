from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Ghost:
    driver: webdriver

    def __enter__(self) -> webdriver:
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


class ChromeGhost(Ghost):
    """Chrome Headless Browser"""

    def __init__(self, chrome_path, chromedriver_path):
        self.chrome_path = chrome_path
        self.chromedriver_path = chromedriver_path
        self.driver = None

    def __enter__(self) -> webdriver:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = self.chrome_path

        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path, chrome_options=chrome_options)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
