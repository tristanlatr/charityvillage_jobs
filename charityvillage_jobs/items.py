# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Job(scrapy.Item):
    # Mandatory Fields
    title = scrapy.Field()
    url = scrapy.Field()

    # extra fields that scrapers can fill
    organisation = scrapy.Field()
    date_posted = scrapy.Field()
    apply_before = scrapy.Field()
    location = scrapy.Field()
    job_type = scrapy.Field()
    salary = scrapy.Field()
    week_hours = scrapy.Field()
    description = scrapy.Field()
