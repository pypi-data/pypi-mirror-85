#!/usr/bin/python3

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('large_index.log'),
        logging.StreamHandler()
    ])
