from dataclasses import dataclass


@dataclass
class Selectors:
    apartment_page_selector: str
    id_selector: str
    price_selector: str
    size_selector: str
    images_links_selector: str


MY_HOME_GE_SELECTORS = Selectors(
    apartment_page_selector="a.card-container::attr(href)",
    id_selector=".statement-header .id-container > span::text",
    price_selector=".d-block.convertable::attr(data-price-usd)",
    size_selector=".price-toggler-wrapper > .space > div::text",
    images_links_selector=".images img::attr(data-src)",
)
