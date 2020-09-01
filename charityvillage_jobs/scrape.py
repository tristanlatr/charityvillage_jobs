"""
Wrapper arround scrapy system and scrapy related helpers.  


This submodule is only used in tests contracts AutoFillJobUrl.  
But it can be used anywhere else.  
"""

import json
import tempfile
import os
import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import spiderloader
import scrapy.settings

SCRAPY_SETTINGS_MODULE='charityvillage_jobs.settings'

def get_settings():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', SCRAPY_SETTINGS_MODULE)
    settings=get_project_settings()
    return settings

def get_all_scrapers():
    spider_loader = spiderloader.SpiderLoader(settings=get_settings())
    spiders = spider_loader.list()
    return spiders

def scrape(spider_cls_or_name, spider_kwargs={}, additionnal_settings=None):
    """
    Wrap the crawling procress in multiprocessing thread.  
    """
    scraped_data_result=multiprocessing.Manager().list()
    process = multiprocessing.Process(target=_scrape,
        kwargs=dict(spider_cls_or_name=spider_cls_or_name,
            spider_kwargs=spider_kwargs,
            scraped_data_result=scraped_data_result))
    process.start()
    process.join()
    scraped_data_result=list(scraped_data_result)
    return scraped_data_result

def _scrape(spider_cls_or_name, spider_kwargs={}, additionnal_settings=None, scraped_data_result=None):
    """
    Launch the requested scraper with the configuration.  
    """
    scraped_data_result=[] if scraped_data_result==None else scraped_data_result
    scrapy_process_json_data=None

    with tempfile.NamedTemporaryFile() as scrapy_process_temp_file:
        settings=get_settings()
        settings.set("FEEDS", {
                '{}'.format(scrapy_process_temp_file.name): {
                    'format': 'json',
                    'encoding': 'utf8',
                    'indent': 4
                }})
        if additionnal_settings:
            settings.update(additionnal_settings)

        # Scrapy configuration, launched with temp file
        process = CrawlerProcess(settings=settings)
        process.crawl(spider_cls_or_name, **spider_kwargs)
        process.start()
        
        with open(scrapy_process_temp_file.name, 'r', encoding='utf-8') as crawler_process_json_fp:
            try:
                scrapy_process_json_data=json.load(crawler_process_json_fp)
                # write result in argument's list, used with multiprocessing
                scraped_data_result.extend(scrapy_process_json_data)
                return(scrapy_process_json_data)

            except ValueError as err:
                if str(crawler_process_json_fp.read()).strip()=="":
                    raise ValueError('Looks like there has been an issue during the scrape') from err
                else:
                    raise