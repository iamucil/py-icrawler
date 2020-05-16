# -*- coding: utf-8 -*-
from pydispatch import dispatcher
from scrapy import signals

from main.models import Quote


class ScrapyAppPipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id
        self.items = []
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'),
        )

    def process_item(self, item, spider):
        quote = Quote()
        quote.text = item['text']
        quote.author = item['author']
        quote.save()
        self.items.append(item['author'])
        return item

    def spider_closed(self, spider):
        print('SPIDER FINISHED!')
