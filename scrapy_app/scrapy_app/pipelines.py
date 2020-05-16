# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class ScrapyAppPipeline:
#     def process_item(self, item, spider):
#         return item


# from main.models import ScrapyItem
# import json

# class ScrapyAppPipeline(object):
#     def __init__(self, unique_id, *args, **kwargs):
#         self.unique_id = unique_id
#         self.items = []

#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
#         )

#     def close_spider(self, spider):
#         # And here we are saving our crawled data with django models.
#         item = ScrapyItem()
#         item.unique_id = self.unique_id
#         item.data = json.dumps(self.items)
#         item.save()

#     def process_item(self, item, spider):
#         self.items.append(item['url'])
#         return item

from pydispatch import dispatcher
from scrapy import signals

from main.models import Quote


class ScrapyAppPipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'),
        )

    def process_item(self, item, spider):
        # scrapy_item = ScrapyItem()
        # scrapy_item.unique_id = self.unique_id
        # scrapy_item.title = item['title']
        # scrapy_item.contents = item['contents']
        # scrapy_item.published_date = item['published_date']
        # scrapy_item.views = item['views']
        # scrapy_item.recommends = item['recommends']
        # scrapy_item.url = item['url']
        # scrapy_item.category = item['category']

        # scrapy_item.save()
        quote = Quote(text=item.get('text'), author=item.get('author'))
        quote.save()
        return item

    def spider_closed(self, spider):
        print('SPIDER FINISHED!')
