import logging
import json
from datetime import datetime, timezone
from urllib import parse

import trafilatura
from itemadapter import ItemAdapter
from scrapy import Item
from scrapy.exceptions import DropItem

from webscraper.spiders.configurable import ConfigurableSpider

logger = logging.getLogger(__name__)


class ExtractionPipeline:

    def process_item(self, item: Item, spider: ConfigurableSpider) -> Item:
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
                'text': extracted_data.get('text'),
                'metadata': {
                    'title': extracted_data.get('title'),
                    'author': extracted_data.get('author')
                }
            }
        else:
            logger.warning('Extraction mode `%s` is not yet implemented.',
                           task_config.mode)

        return item


class ProvenancePipeline:

    def process_item(self, item: Item, spider: ConfigurableSpider) -> Item:
        adapter = ItemAdapter(item)
        adapter['crawl_timestamp'] = datetime.now(timezone.utc).isoformat()
        adapter['source_domain'] = parse.urlparse(adapter['source_url']).netloc
        adapter['extractor'] = spider.task_config.mode

        return item


class ValidationPipeline:

    def process_item(self, item: Item, spider: ConfigurableSpider) -> Item:
        adapter = ItemAdapter(item)

        content = adapter.get('content')
        if not content:
            raise DropItem(
                f"Missing content field in item: {adapter.get('source_url')}")

        if not content.get('text') or not content['text'].strip():
            raise DropItem('Missing or empty text in content for item: '
                           f"{adapter.get('source_url')}")

        return item
