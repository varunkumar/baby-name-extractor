import argparse
import logging
import sys

from search import construct_words, list_files, search_names
from sources import peyar, peyari

logger = logging.getLogger(__name__)
null = None
description = "Extract and search Tamil baby names"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-v", "--verbosity", help="Set logging level", default="INFO")

    parser.add_argument(
        "-d",
        "--download",
        help="Extract names from the web",
        action="store_true",
        default=False,
    )

    parser.add_argument("-p", "--prefix", help="Search name by a prefix", default="")

    parser.add_argument("-s", "--suffix", help="Search name by a suffix", default="")

    parser.add_argument("-l", "--length", help="Length of the name", type=int)

    parser.add_argument(
        "-o", "--output", help="Output file to store the result", default="results.csv"
    )

    parser.add_argument(
        "-g",
        "--gender",
        help="Filter the name by gender. Possible values: boy, girl",
        required=True,
    )

    args = parser.parse_args()

    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, args.verbosity),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.download:
        logger.debug("Extracting names from sources...")
        peyari.download_all()
        peyar.download_all()
        logger.info("Done extracting names from all sources")
        sys.exit(0)

    if args.prefix or args.suffix:
        construct_words(args.gender)
        search_names(args.prefix, args.suffix, args.length, args.output)
        sys.exit(0)
