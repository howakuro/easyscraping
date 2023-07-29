import time
import logging
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumBrowserDriver(webdriver.Chrome):
    def __init__(self, work_dir_path: str | Path, is_headless: bool = False):
        service_log_file_path = Path(work_dir_path, "log", "service.log")
        user_profile_path = Path(work_dir_path, "userprofile")

        options = Options()
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
        options.add_argument('--user-data-dir='+user_profile_path)

        if is_headless == True:
            options.add_argument('--headless')

        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.use_chromium = True
        logging.getLogger('WDM').setLevel(logging.NOTSET)

        max_restart = 10
        for i in range(max_restart):
            try:
                brouser_service = service.Service(
                    ChromeDriverManager().install())
                break
            except:
                if i == max_restart - 1:
                    raise

        super().__init__(service=brouser_service,
                         options=options,
                         service_log_path=service_log_file_path)

    def sleep_requests(self, url: str, sleepsec: int = 3):
        response = self.get(url)
        time.sleep(sleepsec)
        return response

    def sleep_click(self, elements: WebElement, sleepsec: int = 3):
        elements.click()
        time.sleep(sleepsec)

    def window_resize(self):
        w = self.execute_script("return document.body.scrollWidth;")
        h = self.execute_script("return document.body.scrollHeight;")
        self.set_window_size(w, h)
