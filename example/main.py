import tempfile
import urllib.parse

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import easyscraping


def google_search(search_text: str) -> list:
    """
    Function to perform a Google search and obtain a list of hit URLs.

    Args:
        search_text (str):
            String to perform the search.

    Returns:
        list:
            A list of URLs found by the search.
            If it does not exist, an empty list is returned.
    """
    with tempfile.TemporaryDirectory() as directory_name:
        with easyscraping.SeleniumBrowserDriver(work_dir_path=directory_name, is_headless=True) as driver:
            url = 'https://www.google.com/search?q='
            url += urllib.parse.quote_plus(search_text)

            driver.sleep_requests(url)
            driver.window_resize()
            try:
                search_results = driver.find_elements(By.CSS_SELECTOR, '#rso > div')
                url_list = []
                for search_result in search_results:
                    link = search_result.find_element(By.CSS_SELECTOR, 'div > div > div:nth-child(1) > div > a')
                    url_list.append(link.get_attribute('href'))
                return url_list
            except NoSuchElementException:
                return []


if __name__ == '__main__':
    print(google_search('python'))
