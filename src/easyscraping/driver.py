import logging
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumBrowserDriver(webdriver.Chrome):
    def __init__(self, work_dir_path: str | Path, is_headless: bool = False, default_sleepsec: int = 3):
        """
        SeleniumBrowserDriver initialize method

        Args:
            work_dir_path (str | Path):
                Directory used by Selenium.
            is_headless (bool, optional):
                Set to True if you do not want the Selenium browser to appear.
                Defaults to False.
            default_sleepsec (int, optional):
                Sleep time for site loading.
                If a time is specified for each method, that value takes precedence.
                Defaults to 3.

        Raises:
            Exception:
                This error is returned if an error occurs during the installation of ChromeDriverManager.
        """
        user_profile_path = Path(work_dir_path, "userprofile")

        self.default_sleepsec = default_sleepsec

        options = Options()
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
        options.add_argument('--user-data-dir='+str(user_profile_path))

        if is_headless:
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
            except Exception:
                if i == max_restart - 1:
                    raise Exception

        super().__init__(service=brouser_service, options=options)

    def sleep_requests(self, url: str, sleepsec: int | None = None) -> None:
        """
        After sending a request to the site, it waits for a certain period of time.

        Args:
            url (str):
                URL to send the request.
            sleepsec (int | None, optional):
                Sleep time for site loading.
                If omitted, the value at the time of instance creation is used.
        """
        self.get(url)
        sleepsec = sleepsec if sleepsec is not None else self.default_sleepsec
        time.sleep(sleepsec)

    def sleep_click(self, elements: WebElement, sleepsec: int | None = None) -> None:
        """
        After clicking on a particular element, wait a certain amount of time.

        Args:
            elements (WebElement):
                Elements to click.
            sleepsec (int | None, optional):
                Sleep time for site loading.
                If omitted, the value at the time of instance creation is used.
        """
        elements.click()
        sleepsec = sleepsec if sleepsec is not None else self.default_sleepsec
        time.sleep(sleepsec)

    def window_resize(self) -> None:
        """
        Resize the Selenium browser.
        """
        w = self.execute_script("return document.body.scrollWidth;")
        h = self.execute_script("return document.body.scrollHeight;")
        self.set_window_size(w, h)
