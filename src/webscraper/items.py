from scrapy import Field, Item


class ScrapedItem(Item):
    source_url = Field()
    source_domain = Field()
    crawl_timestamp = Field()
    extractor = Field()
    language = Field()

    content = Field()
