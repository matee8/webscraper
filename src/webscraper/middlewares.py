from typing import AsyncIterator, Iterable, Any

from scrapy import signals, Spider
from scrapy.crawler import Crawler
from scrapy.http import Response, Request


class WebscraperSpiderMiddleware:

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> 'WebscraperSpiderMiddleware':
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response: Response, spider: Spider) -> None:
        return None

    def process_spider_output(self,
                              response: Response,
                              result: Iterable[Any],
                              spider: Spider | None = None) -> Iterable[Any]:
        for i in result:
            yield i

    def process_spider_exception(
            self,
            response: Response,
            exception: Exception,
            spider: Spider | None = None) -> Iterable[Any] | None:
        pass

    async def process_start(self,
                            start: AsyncIterator[Any]) -> AsyncIterator[Any]:
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider: Spider) -> None:
        spider.logger.info('Spider opened: %s' % spider.name)


class WebscraperDownloaderMiddleware:

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> 'WebscraperDownloaderMiddleware':
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: Request, spider: Spider):
        return None

    def process_response(self, request: Request, response: Response,
                         spider: Spider) -> Request | Response:
        return response

    def process_exception(self, request: Request, exception: Exception,
                          spider: Spider) -> Request | Response | None:
        pass

    def spider_opened(self, spider: Spider) -> None:
        spider.logger.info('Spider opened: %s' % spider.name)
