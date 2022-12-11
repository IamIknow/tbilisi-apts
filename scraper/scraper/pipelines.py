# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from kafka import KafkaProducer
from redis import Redis
from scrapy.exceptions import DropItem

import json

from scraper.items import ApartmentItem
from scraper.settings import (
    KAFKA_APARTMENTS_TOPIC,
    KAFKA_BOOTSTRAP_SERVER,
    REDIS_HOST,
    REDIS_PASSWORD,
    REDIS_PORT,
)


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open("items.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item: ApartmentItem, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


class ApartmentsStoragePipeline:
    def __init__(self) -> None:
        self.redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def process_item(self, item: ApartmentItem, spider) -> ApartmentItem:
        key = f"user-{item.user_id}:{item.id}"

        if self.redis.get(key):
            raise DropItem(f"Apartment was already processed")

        self.redis.set(key, json.dumps(ItemAdapter(item).asdict()))
        return item


class KafkaProducerPipeline:
    def __init__(self) -> None:
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        )

    def process_item(self, item: ApartmentItem, spider) -> ApartmentItem:
        print(item)
        self.producer.send(
            topic=KAFKA_APARTMENTS_TOPIC,
            value=ItemAdapter(item).asdict(),
        )
        return item
