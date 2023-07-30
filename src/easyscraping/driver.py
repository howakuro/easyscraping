import time
import logging
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumBrowserDriver(webdriver.Chrome):
    default_sleepsec: int

    def __init__(self, work_dir_path: str | Path, is_headless: bool = False, default_sleepsec: int = 3):
        user_profile_path = Path(work_dir_path, "userprofile")

        self.default_sleepsec = default_sleepsec

        options = Options()
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
        options.add_argument('--user-data-dir='+str(user_profile_path))

        if is_headless == True:
            options.add_argument('--headless')

        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.use_chromium = True
        logging.getLogger('WDM').setLevel(logging.NOTSET)

        max_restart = 10
        for i in range(max_restart):
            try:
                brouser_service = service.Service(
                    executable_path=ChromeDriverManager().install(),
                )
                break
            except:
                if i == max_restart - 1:
                    raise

        super().__init__(service=brouser_service, options=options)

    def sleep_requests(self, url: str, sleepsec: int | None = None):
        response = self.get(url)
        sleepsec = sleepsec if sleepsec is not None else self.default_sleepsec
        time.sleep(sleepsec)
        return response

    def sleep_click(self, elements: WebElement, sleepsec: int | None = None):
        elements.click()
        sleepsec = sleepsec if sleepsec is not None else self.default_sleepsec
        time.sleep(sleepsec)

    def window_resize(self):
        w = self.execute_script("return document.body.scrollWidth;")
        h = self.execute_script("return document.body.scrollHeight;")
        self.set_window_size(w, h)
