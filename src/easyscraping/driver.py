import os
import time
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumBrowserDriver(webdriver.Chrome):
    def __init__(self, work_dir_path, is_headless=False):
        service_log_file_path = os.path.join(
            work_dir_path, "log", "service.log")
        user_profile_path = os.path.join(work_dir_path, "userprofile")

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
            except:
                if i == max_restart - 1:
                    raise

        super().__init__(service=brouser_service,
                         options=options,
                         service_log_path=service_log_file_path)

    def sleep_requests(self, url, sleepsec=3):
        response = self.get(url)
        time.sleep(sleepsec)
        return response

    def sleep_click(self, elements, sleepsec=3):
        elements.click()
        time.sleep(sleepsec)

    def window_resize(self):
        w = self.execute_script("return document.body.scrollWidth;")
        h = self.execute_script("return document.body.scrollHeight;")
        self.set_window_size(w, h)
