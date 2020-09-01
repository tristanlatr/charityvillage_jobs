import re
from itemadapter import is_item, ItemAdapter
from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy import spiderloader
from scrapy.utils import project
from scrapy.selector import Selector

# SeleniumRequest
from scrapy_selenium import SeleniumRequest

#### Generic contracts 

class WithSelenium(Contract):
    """ Contract to set the request class to be SeleniumRequest for the current call back method to test.  
    Required to test SeleniumRequests.  

    @with_selenium
    """
    name = 'with_selenium'
    request_cls = SeleniumRequest

class ScrapeNotNone(Contract):

    """ Contract to check presence of fields in scraped items and check if they are None

        @scrape_not_none url title description
    """

    name = 'scrape_not_none'

    def post_process(self, output):
        for x in output:
            if is_item(x):
                missing = [arg for arg in self.args if arg not in ItemAdapter(x) or ItemAdapter(x)[arg]==None]
                if missing:
                    missing_str = ", ".join(missing)
                    raise ContractFail("Missing or None fields: %s. Item is %s" % (missing_str, x))

class ReturnsValidSelectorList(Contract):
    
    """ Contract to check if the returned output is a Selector list

        @returns_valid_selectorlist
    """

    name = 'returns_valid_selectorlist'

    def post_process(self, output):
        if not isinstance(output, list):
            raise ContractFail("Output is not a valid list. Output is {}".format(output))
        for out in output:
            if not isinstance(out, Selector):
                raise ContractFail("Output is not a valid SelectorList. Output is {}".format(output))

class ReturnsValidLink(Contract):
    
    """ Contract to check if the method returns a valid link

        @returns_valid_link
    """

    name = 'returns_valid_link'

    def post_process(self, output):
        if output:
            output=output[0]
        if not isinstance(output, str):
            raise ContractFail("Output is not a valid link. Output is {}".format(output))
        if len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', output)) < 1:
            raise ContractFail("Output is not a valid link. Output is {}".format(output))



#### This part is only applicable for this spiders

# Import custom scrapy wrapper
from .scrape import get_all_scrapers, scrape

class AutoFillJobUrl(Contract):
    """ Contract to set the url of the request automatically 
        to the first JOB. Loaded the listing and returns the first URL.  
        Also sets job_dict with url and title in cb_kwargs

        @auto_job_url arrondissement.com
    """

    name = 'auto_job_url'

    def adjust_request_args(self, args):
        website=self.args[0]
        jobs = scrape(website, dict(load_full_jobs=False, load_all_pages=False))
        args['url'] = jobs[0]['url']
        args['cb_kwargs']=dict(job_dict=jobs[0])
        print("First {} job posting test URL is: {}".format(website, args['url']))
        return args