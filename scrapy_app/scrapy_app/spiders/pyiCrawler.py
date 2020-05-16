# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from .. import items

class pyicrawlerSpider(CrawlSpider):
    name = 'pyicrawler'

    def __init__(self, *args, **kwargs):
        # We are going to pass the args from our django view.
        # To make everything dynamic, we need to override the inside __init__ method
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

        pyicrawlerSpider.rulse = [
            Rule(LinkExtractor(unique=True), callback='parse_item'),
        ]
        super(pyicrawlerSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        # You can tweak each crawled page here
        # Don't forget to return an object
        i = {}
        i['url'] = response.url
        return i
