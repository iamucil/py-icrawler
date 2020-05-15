# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from .. import items

class pyicrawlerSpider(CrawlSpider):
    name = 'pyicrawler'
    # allowed_domains = ['https://google.com']
    # start_urls = ['http://https://google.com/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    # # def parse_item(self, response):
    # #     item = {}
    # #     #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
    # #     #item['name'] = response.xpath('//div[@id="name"]').get()
    # #     #item['description'] = response.xpath('//div[@id="description"]').get()
    # #     return item

    # def __init__(self, *args, **kwargs):
    #     # We are going to pass these args from our django view.
    #     # To make everything dynamic, we need to override them inside __init__ method
    #     self.url = kwargs.get('url')
    #     self.domain = kwargs.get('domain')
    #     self.start_urls = [self.url]
    #     self.allowed_domains = [self.domain]

    #     IcrawlerSpider.rules = [
    #        Rule(LinkExtractor(unique=True), callback='parse_item'),
    #     ]
    #     super(IcrawlerSpider, self).__init__(*args, **kwargs)

    # def parse_item(self, response):
    #     # You can tweak each crawled page here
    #     # Don't forget to return an object.
    #     i = {}
    #     i['url'] = response.url
    #     return i

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.allowed_domains = [self.domain]
        self.category_dict = {
            'Maple Story Inven Maple': 1,
            'Maple Story Inven Free Board': 2,

        }

    def start_requests(self):
        for i in range(1, 2):  # 페이지 하나씩 넘어가기
            yield scrapy.Request(self.url + str(i), self.parse_board)

    def parse_board(self, response):  # 페이지에 있는 게시물 전체 가져오기
        board = response.xpath('//tr[contains(@class, "ls") and contains(@class, "tr")]')

        for i in range(len(board)):
            # 페이지마다 있는 게시물의 href에 접속해서 제목, 내용, 추천수, 조회수 가져오기
            self.post_url = response.xpath('//tr[contains(@class, "ls") and contains(@class, "tr")]/td[@class="bbsSubject"]/a[@class="sj_ln"]/@href')[i].extract()
            yield scrapy.Request(self.post_url, self.parse_post)

    def get_num(self, s):
        regex = re.compile(r'\d{1,3}[,{1}\d{3}]*')
        num = regex.search(s)
        start, end = list(num.span())[0], list(num.span())[1]
        s = s[start:end]
        s_list = s.split(',')
        result = ''
        for n in s_list:
            result += n
        return int(result)

    def get_str(self, s_list):
        result = ''
        for s in s_list:
            result += s
        return result

    def parse_post(self, response):
        item = items.ScrapyAppItem()
        item['title'] = response.xpath('//*[@id="tbArticle"]/div[3]/div[1]/div[1]/h1/text()')[0].extract()
        item['contents'] = self.get_str(response.xpath('//*[@id="imageCollectDiv"]//div/text()|'
                                                       '//*[@id="imageCollectDiv"]//font/text()|'
                                                       '//*[@id="imageCollectDiv"]//p/text()|'
                                                       '//*[@id="imageCollectDiv"]//span/text()|'
                                                       '//*[@id="imageCollectDiv"]//strong/text()').extract())
        item['published_date'] = response.xpath('//*[@id="tbArticle"]/div[1]/div/div[2]/text()')[0].extract()
        item['views'] = self.get_num(response.xpath('//*[@id="tbArticle"]/div[1]/div/div[3]/text()')[1].extract())
        item['recommends'] = response.xpath('//*[@id="bbsRecommendNum1"]/text()')[0].extract()
        item['url'] = response.xpath('//*[@id="viewUrl"]/text()')[0].extract()
        category = response.xpath('//div[@class="viewTopBoardName"]/a/text()')[0].extract()
        for k, v in self.category_dict.items():
            if k == category:
                item['category'] = v

        yield item
