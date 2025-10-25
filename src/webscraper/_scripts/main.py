#!/usr/bin/env python

import logging
from pathlib import Path
from typing import Optional

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from scrapy.crawler import CrawlerProcess
from scrapy.utils import project

from webscraper.config import AppConfig
from webscraper.spiders.configurable import ConfigurableSpider

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

logger = logging.getLogger(__name__)


def load_config(config_path: Path = Path('config.toml')) -> Optional[AppConfig]:
    logger.info('Attempting to load configuration from: %s.', config_path)
    try:
        with open(config_path, 'rb') as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        logger.error('Configuration file not found at %s.', config_path)
        return None

    config = AppConfig.from_dict(config)
    logger.info('Configuration loaded successfully.')
    return config


def main() -> None:
    config = load_config()

    if not config:
        logger.warning('No tasks found in configuration. Exiting.')
        return

    logger.info('Found %d tasks in configuration.', len(config.tasks))

    settings = project.get_project_settings()
    process = CrawlerProcess(settings)

    for task in config.tasks:
        task_name = (task.name or
                     f'Unnamed task for {task.domain or task.start_urls[0]}')
        logging.info('Queueing task: %s.', task_name)
        process.crawl(ConfigurableSpider, task_config=task)

    process.start()
    logger.info('All tasks have been completed.')


if __name__ == '__main__':
    main()
