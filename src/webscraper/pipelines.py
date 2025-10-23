from typing import Any

from scrapy import Spider


class WebscraperPipeline:

    def process_item(self, item: Any, spider: Spider | None = None) -> Any:
        return item
