import json
import sys
import logging

try:
    with open("config.json", "r") as fp:
        config = json.load(fp)
except FileNotFoundError:
    logging.critical('Config file "config.json" not found.')
    sys.exit(1)
