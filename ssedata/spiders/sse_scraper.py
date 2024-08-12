import scrapy
import time
from pathlib import Path
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

# to run: scrapy crawl sse_scraper -a starts_page=xx -a ends_page=xxx -O outputs/xxx.csv
class SseScraper(scrapy.Spider):
    name = "sse_scraper"

    def __init__(self, starts_page=1, ends_page=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.starts_page = int(starts_page)
        self.ends_page = int(ends_page)

    def start_requests(self):
        url = "http://www.sse.com.cn/ipo/disclosure/"
        yield SeleniumRequest(
            url=url, 
            callback=self.parse,
            wait_time=10,
            wait_until=EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".list-group-item"))
        )

    def parse(self, response):
        driver = response.request.meta["driver"]

        for i in range(self.starts_page, self.ends_page):
            print(f'scraping page {i}')

            # jump to target page
            driver.execute_script(f'xxplList({i})')
            time.sleep(2)
            
            # select all elements and iterate over them
            for item in driver.find_elements(By.CSS_SELECTOR, ".list-group-item"):
                try:
                    link =  item.find_element(By.CSS_SELECTOR, "a")
                    url = link.get_attribute("href")
                    name = link.text
                    # only IPO documents
                    if name.endswith("招股说明书"):
                        yield {
                            "url": url,
                            "name": name,
                        }
                except NoSuchElementException:
                    pass
