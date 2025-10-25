#!/usr/bin/env python

import logging
from pathlib import Path
from typing import Optional

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from webscraper.config import AppConfig

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

    if config:
        logger.info('Found %d tasks in configuration.', len(config.tasks))


if __name__ == '__main__':
    main()
