# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from kafka import KafkaProducer

import json

from scraper.items import ApartmentItem


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open("items.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item: ApartmentItem, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


class KafkaProducerPipeline:
    def __init__(self) -> None:
        self.producer = KafkaProducer(
            value_serializer=lambda x: json.dumps(x).encode("utf-8")
        )

    def process_item(self, item: ApartmentItem, spider):
        print(item)
        self.producer.send(topic="apartments_topic", value=ItemAdapter(item).asdict())
