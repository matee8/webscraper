import logging
from typing import Iterable, Optional

from scrapy import Spider
from scrapy.http import Response, Request

from webscraper.config import TaskConfig

logger = logging.getLogger(__name__)


class ConfigurableSpider(Spider):
    name = 'configurable'

    def __init__(self,
                 *args,
                 task_config: Optional[TaskConfig] = None,
                 **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if not isinstance(task_config, TaskConfig):
            raise ValueError('A `TaskConfig` object must be provided.')

        self.task_config = task_config
        self.start_urls = self.task_config.start_urls

        self.task_name = self.task_config.name or 'Unnamed Task'
        logger.info('Initialized spider for task: %s.', self.task_name)

    def parse(self, response: Response,
              **kwargs) -> Iterable[Optional[Request]]:
        logger.info('Processing page: %s', response.url)

        yield None
