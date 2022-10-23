import scrapy

from scraper.items import ApartmentItem

from scraper.selectors import MY_HOME_GE_SELECTORS


WEBSITE_URL = "https://www.myhome.ge/ru/s/%D0%A1%D0%B4%D0%B0%D0%B5%D1%82%D1%81%D1%8F-%D0%B2-%D0%B0%D1%80%D0%B5%D0%BD%D0%B4%D1%83-%D0%BD%D0%BE%D0%B2%D0%BE%D0%BF%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0-%D0%A2%D0%B1%D0%B8%D0%BB%D0%B8%D1%81%D0%B8?Keyword=%D0%A2%D0%B1%D0%B8%D0%BB%D0%B8%D1%81%D0%B8&AdTypeID=3&PrTypeID=1&mapC=41.73188365%2C44.8368762993663&regions=687602533&districts=5469869&cities=1996871&GID=1996871&EstateTypeID=1"


class MyHomeSpider(scrapy.Spider):
    name = "myhome.ge"

    def start_requests(self):
        yield scrapy.Request(WEBSITE_URL)

    def parse(self, response):
        apartment_pages = response.css("a.card-container::attr(href)").getall()

        for page in apartment_pages:
            yield scrapy.Request(page, callback=self.parse_apartment)

    def parse_apartment(self, response):
        yield ApartmentItem(
            price=response.css(MY_HOME_GE_SELECTORS.price_selector).get(),
            link=response.url,
            size=response.css(MY_HOME_GE_SELECTORS.size_selector).get(),
            id=response.css(MY_HOME_GE_SELECTORS.id_selector).get(),
            image_links=response.css(
                MY_HOME_GE_SELECTORS.images_links_selector
            ).getall(),
        )
