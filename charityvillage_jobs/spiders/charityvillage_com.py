import urllib.parse
import scrapy
import abc
import time
from bs4 import BeautifulSoup
from scrapy_selenium import SeleniumRequest
from ..items import Job

SCROLL_DOWN='window.scrollTo(0,document.body.scrollHeight);'

class Scraper_charityvillage_com(scrapy.Spider):
    """Use SeleniumRequest because website require javascript"""

    name = "charityvillage.com"
    allowed_domains = [name]
    start_urls=['https://charityvillage.com/search/#results/5f4583ff061c57fc640eb1dc?job_type=-Unpaid+Volunteer+Position&page_num=1&kw=']

    def start_requests(self):
        for url in self.start_urls:
            # Auto scroll down
            yield SeleniumRequest(url=url, callback=self.parse, 
                wait_time=self.selenium_wait_time , 
                script=SCROLL_DOWN)

    def __init__(self, url=None, start_urls=None, load_full_jobs=False, load_all_pages=False, selenium_wait_time=20):

        self.start_urls=[url] if url else start_urls if start_urls else type(self).start_urls
        self.load_full_jobs=load_full_jobs
        self.load_all_pages=load_all_pages
        self.selenium_wait_time=selenium_wait_time

    def parse(self, response):
        """
        @with_selenium
        @url https://charityvillage.com/search/#results/5f4583ff061c57fc640eb1dc?job_type=-Unpaid+Volunteer+Position&page_num=1&kw=
        @returns items 20 20
        @scrape_not_none url title date_posted apply_before organisation location
        """
        page_jobs=[]

        """ Iterating through the result of get_jobs_list()"""

        jobs_div_list=self.get_jobs_list(response)
        for div in jobs_div_list:
            
            # Calling abstarct method get_job_dict()
            job_dict=self.get_job_dict(div)
            
            page_jobs.append(job_dict)
            
            """
            Load full job page only if:
            - load_full_jobs=Yes
            """
            if ( self.load_full_jobs ):
                # Call parse_full_job_page() with job URL
                yield SeleniumRequest(url=job_dict['url'], 
                    callback=self.parse_full_job_page,
                    cb_kwargs=dict(job_dict=job_dict),
                    wait_time=self.selenium_wait_time,
                    script=SCROLL_DOWN)
                
            else:
                yield Job(job_dict)

        """ Just printing """
        if self.load_full_jobs:
            print("Scraping {} jobs from {}...".format(len(page_jobs), response.url))
        else:
            if self.load_all_pages==False:
                print("Scraped {} jobs from {}. load_all_pages=False and load_full_jobs=False, some new job postings and job informations might be missing".format(len(page_jobs), response.url))
            else:
                print("Scraped {} jobs from {}. load_full_jobs=False, some informations might be missing".format(len(page_jobs), response.url))
       
        """
        Scrape next page if
         - load_all_pages=True and get_next_page_url() is not None
        """
        if self.load_all_pages:
            if self.get_next_page_url(response)!=None :
                # Loading next page...
                yield SeleniumRequest(
                    url=self.get_next_page_url(response),
                    callback=self.parse,
                    wait_time=self.selenium_wait_time,
                    script=SCROLL_DOWN,
                    dont_filter=True)
            else:
                print("No more pages to load")
    
    def get_jobs_list(self, response):
        """
        Arguments:  
        - response: scrapy response object for the listing page
        
        Return a Selector list.  
        The result will be automatically iterated in `parse()` method.  
        The items will be passed to `get_job_dict()`.
        
        @with_selenium
        @url https://charityvillage.com/search/#results/5f4583ff061c57fc640eb1dc?job_type=-Unpaid+Volunteer+Position&page_num=1&kw=
        @returns_valid_selectorlist
        """
        return response.xpath('//ul[contains(@class,"job-search-results")]/li')

    def get_job_dict(self, selector):
        """
        Arguments:  
        - selector: selector object of the job posting in the listing  

        Return a dict {'url':'https://job-url' , 'title':'Job title', 'organisation':'My community' [...] }
        """
        return {
            'url':selector.xpath('div/div[contains(@class, "cl-job-cta")]/a/@href').get(), 
            'date_posted':selector.xpath('div/div[contains(@class, "cl-job-info-cont")]/div[contains(@class, "cl-job-dates")]/span[1]/text()').get().split("Published: ",1)[-1],
            'apply_before':selector.xpath('div/div[contains(@class, "cl-job-info-cont")]/div[contains(@class, "cl-job-dates")]/span[2]/text()').get().split("Expiry: ",1)[-1],
            'organisation':selector.xpath('div/div[contains(@class, "cl-job-info-cont")]/span[contains(@class, "cl-job-company")]/text()').get(),
            'location':selector.xpath('div/div[contains(@class, "cl-job-info-cont")]/span[contains(@class, "cl-job-location")]/text()').get(),
            'title':selector.xpath('div/div[contains(@class, "cl-job-info-cont")]/a[contains(@class,"cl-job-link")]/h2/text()').get()
        }

    def parse_full_job_page(self, response, job_dict):
        """
        Arguments:  
        - response: scrapy response object for the job page 
        - job_dict: dict containing job raw data,  
            this function must return a new Job() FROM this  
            data and any other relevant info from the job page  

        This method is called by `parse()` method if load_full_jobs  
        Return a Job()  

        @with_selenium
        @auto_job_url charityvillage.com
        @scrape_not_none url title description organisation date_posted apply_before location
        @returns items 1 1  
        """
        job_dict['description']=BeautifulSoup(response.xpath('//div[contains(@class, "post-content")]').get()).get_text()
        return Job(job_dict)

    def get_next_page_url(self, response):
        """
        Arguments:  
        - response: scrapy response object for the listing page

        This method is called by `Scraper.parse()` method if load_all_pages  
        Return a URL string or None if there no more pages to load    

        @with_selenium
        @url https://charityvillage.com/search/#results/5f4583ff061c57fc640eb1dc?job_type=-Unpaid+Volunteer+Position&page_num=1&kw=
        @returns_valid_link
        """
        # The next button doesn't have a href attribute, we need to click it with javascript and extract the page URL
        if 'Next' in response.xpath('//*[@id="cl-jobsearch-results-list"]/div/div[2]/ul/li[last()]/a/text()').get() :
            next_buttons=response.request.meta['driver'].find_elements_by_xpath('//*[@id="cl-jobsearch-results-list"]/div/div[2]/ul/li[last()]/a')
            if len(next_buttons)>0 :
                response.request.meta['driver'].execute_script(SCROLL_DOWN)
                time.sleep(1)
                response.request.meta['driver'].execute_script("arguments[0].click();", next_buttons[0])
                time.sleep(3)
            return response.request.meta['driver'].current_url
        else:
            return None