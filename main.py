import argparse
import csv
import glob
import logging
import sys

import requests

logger = logging.getLogger(__name__)
null = None
description = 'Extract and search Tamil baby names'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=description)

    parser.add_argument('-v', '--verbosity',
                        help='Set logging level', default='INFO')

    args = parser.parse_args()

    log_handler = logging.StreamHandler()
    log_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(log_handler)
    logger.setLevel(getattr(logging, args.verbosity))

    sys.exit(0)
