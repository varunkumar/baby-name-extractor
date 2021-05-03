import csv
import logging
import math
import os

import requests
from bs4 import BeautifulSoup

base_url = "http://peyari.com/nameSearch?search_text=&gender="

logger = logging.getLogger(__name__)


def extract_pages(gender):
    res = requests.get(f"{base_url}{gender}", allow_redirects=True)
    content = res.content
    soup = BeautifulSoup(content, features="html.parser")
    page_count = (
        soup.select("[title='tamil baby names']")[0].get_text().split(" ", 1)[0]
    )
    return math.ceil(int(page_count) / 10)


def download_all():
    logger.info("Downloading data...")
    filed_names = ["letter", "name", "meaning"]
    gender_map = {}
    gender_map["F"] = "girl"
    gender_map["M"] = "boy"

    for gender in ["M", "F"]:
        pages_count = extract_pages(gender)
        os.makedirs(f"./extracts/{gender_map[gender]}/{__name__}", exist_ok=True)
        with open(
            f"./extracts/{gender_map[gender]}/{__name__}/names.csv", mode="w+"
        ) as names_file:
            writer = csv.DictWriter(names_file, fieldnames=filed_names)
            writer.writeheader()
            for page in range(1, pages_count + 1):
                logger.debug(f"Extracting {gender} names - page {page}...")
                url = f"{base_url}{gender}&page={page}"
                res = requests.get(url, allow_redirects=True)
                content = res.content
                soup = BeautifulSoup(content, features="html.parser")
                for name_detail in soup.select(".name-list-detail"):
                    name = name_detail.select(".name-list-link span")[0].get_text()
                    meaning = (
                        name_detail.select(".name-list-meaning")[0]
                        .get_text()
                        .replace("பொருள்:", "")
                        .strip()
                    )
                    writer.writerow(
                        {"letter": name[0], "name": name, "meaning": meaning}
                    )
