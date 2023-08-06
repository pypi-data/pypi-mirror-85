import logging.config
import os
from pathlib import Path

import yaml


def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value

    path = Path(path)
    if path.exists():
        logging.config.dictConfig(yaml.load(path.read_text(), Loader=yaml.Loader))
    else:
        logging.basicConfig(level=default_level)
        print('Failed to load configuration file. Using default configs')
