# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import field
from attr import dataclass


@dataclass
class ApartmentItem:
    id: str | None = field(default=None)
    price: str | None = field(default=None)
    size: str | None = field(default=None)
    link: str | None = field(default=None)
    image_links: list[str] | None = field(default=None)
