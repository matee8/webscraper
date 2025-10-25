#!/usr/bin/env python

import logging
from pathlib import Path
from typing import Any, Dict, Union

try:
    import tomllib
except ImportError:
    import tomli as tomllib

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

logger = logging.getLogger(__name__)


def load_config(config_path: Path = Path('config.toml')) -> Union[Dict[
        str, Any], None]:
    logger.info('Attempting to load configuration from: %s.', config_path)
    try:
        with open(config_path, 'rb') as f:
            config = tomllib.load(f)
            logger.info('Configuration loaded successfully.')
            return config
    except FileNotFoundError:
        logger.error('Configuration file not found at %s.', config_path)
        return None


def main() -> None:
    config = load_config()

    if config:
        logger.info('Found %d tasks in configuration.',
                    len(config.get('tasks', [])))


if __name__ == '__main__':
    main()
