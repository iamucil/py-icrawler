import json

from django.db import models
from django.utils import timezone

class ScrapyItem(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    data = models.TextField()  # This stand for our crawled data
    date = models.DateTimeField(default=timezone.now)

    # This is basic and custom serialization to return it to client as a json
    @property
    def to_dict(self):
        data = {
            'data': json.loads(self.data),
            'date': self.date
        }
        return data

    def __str__(self):
        return self.unique_id
