# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spiders import CrawlSpider
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule

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

    def start_requests(self):
        self.logger.info('Start request! %s', self.url)
        yield scrapy.Request(self.url, self.parse_item)

    def parse_item(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            }
        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
