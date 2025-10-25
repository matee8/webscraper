import logging
import json
from typing import Any

import trafilatura
from itemadapter import ItemAdapter
from scrapy import Item

from webscraper.spiders.configurable import ConfigurableSpider

logger = logging.getLogger(__name__)


class ExtractionPipeline:

    def process_item(self, item: Item, spider: ConfigurableSpider) -> Any:
        adapter = ItemAdapter(item)
        task_config = spider.task_config

        response = adapter.pop('response')

        if task_config.mode == 'trafilatura':
            logger.debug('Using trafilatura to extract from %s.', response.url)
            json_str = trafilatura.extract(response.body,
                                           url=response.url,
                                           output_format='json',
                                           with_metadata=True,
                                           include_comments=False,
                                           include_tables=False)

            if not json_str:
                logger.warning('No content extracted by trafilatura for %s.',
                               response.url)
                return item

            extracted_data = json.loads(json_str)

            adapter['content'] = {
                'text': json_str,
                'metadata': {
                    'title': extracted_data.get('title'),
                    'author': extracted_data.get('author')
                }
            }
        else:
            logger.warning('Extraction mode `%s` is not yet implemented.',
                           task_config.mode)

        return item
