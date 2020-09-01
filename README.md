# Charity Village Jobs Scraper

This is a raw Scrapy project to scrape job postings from [charityvillage.com](https://charityvillage.com).  

See [Alt Job](https://github.com/tristanlatr/alt_job) fore more supported websites and email notification feature.  

## Install

```bash
git clone https://github.com/tristanlatr/charityvillage_jobs.git
cd charityvillage_jobs
python3 setup.py install
```

## Extracted data

This project extracts quotes, combined with the respective author names and tags.
The extracted data looks like this sample:

    {
        "url": "https://charityvillage.com/jobs/director-of-teacher-recruitment-in-toronto-toronto-division-ontario-ca/",
        "date_posted": "August 26, 2020",
        "apply_before": "September 30, 2020",
        "organisation": "\n\t\t\t\t\t\t\t\tTeach For Canada\n\t\t\t\t\t\t\t",
        "location": "Remote",
        "title": "Director of Teacher Recruitment"
    }


## Spider

This project contains one spiders and you can see it using the `list`
command:

    $ scrapy list
    charityvillage.com


## Running the spider

You can run a spider using the `scrapy crawl` command, such as:

    $ scrapy crawl charityvillage.com

If you want to save the scraped data to a file, you can pass the `-o` option:
    
    $ scrapy crawl charityvillage.com -o jobs.json 

If you want to scrape from a specific search URL, you can pass  the `-a "url={}"` option:

    $ scrapy crawl charityvillage.com -o jobs.json -a "url=https://charityvillage.com/search/#results/5f4eb8f2b5ea676537f41bd5?kw=&loc=Ottawa&page_num=1"

If you want to load jobs pages individually ans scrape more infos, you can pass  the `-a "load_full_jobs=True"` option:

    $ scrapy crawl charityvillage.com -o jobs.json -a "load_full_jobs=True" -a "url=https://charityvillage.com/search/#results/5f4eb8f2b5ea676537f41bd5?kw=&loc=Ottawa&page_num=1"

If you want to load all available pages and scrape more job postings, you can pass  the `-a "load_all_pages=True"` option:

    $ scrapy crawl charityvillage.com -o jobs.json -a "load_all_pages=True" -a "url=https://charityvillage.com/search/#results/5f4eb8f2b5ea676537f41bd5?kw=&loc=Ottawa&page_num=1"

## Testing the spider

You can run the automatic docstrings testing, [Contracts](https://docs.scrapy.org/en/latest/topics/contracts.html) test by running:

    $ scrapy check
