import csv
import logging
import os
import re

words = []
meanings = {}

logger = logging.getLogger(__name__)


def list_files(gender):
    path = f"./extracts/{gender}"
    source_paths = [f"{path}/{f}" for f in os.listdir(path)]
    return [
        f"{source_path}/{f}"
        for source_path in source_paths
        for f in os.listdir(source_path)
    ]


def construct_words(gender):
    for file_name in list_files(gender):
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    words.append(row[1])
                    if row[2] is not None and row[2] != "":
                        meanings[row[1]] = row[2]
                    line_count += 1
            logger.debug(f"Extracted {line_count} names from `{file_name}`.")


def search_names(prefix, suffix, length, result_file):
    pattern = ".*"
    if length:
        pattern = "." * length
    r = re.compile(f"^{prefix}{pattern}{suffix}$")
    names = list(filter(r.match, words))
    names = list(dict.fromkeys(names))
    names.sort()
    names.sort(key=len)
    logger.info(f"Found {len(names)} names")
    with open(result_file, "w+") as f:
        for name in names:
            f.write(f"{name},{meanings[name] if name in meanings else ''}\n")
    logger.info(f"Results stored in {result_file}")
