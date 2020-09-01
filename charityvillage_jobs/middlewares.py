import scrapy_selenium
import time
import random

# Extends scrapy_selenium.SeleniumMiddleware to respect scrapy config https://github.com/clemfromspace/scrapy-selenium/issues/36
class SeleniumMiddleware(scrapy_selenium.SeleniumMiddleware):
    def process_request(self, request, spider):
        if isinstance(request, scrapy_selenium.SeleniumRequest):
            delay = spider.settings.getint('DOWNLOAD_DELAY')
            randomize_delay = spider.settings.getbool('RANDOMIZE_DOWNLOAD_DELAY')
            if delay:
                if randomize_delay:
                    delay = random.uniform(0.5 * delay, 1.5 * delay)
                time.sleep(delay)
        return super().process_request(request, spider)