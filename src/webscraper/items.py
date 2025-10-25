import scrapy
from scrapy import Item


class WebscraperItem(Item):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    body_text = scrapy.Field()
    html = scrapy.Field()
