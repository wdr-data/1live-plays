import json
import sys

try:
    with open('config.json', 'r') as fp:
        config = json.load(fp)
except FileNotFoundError:
    print('Config file "config.json" not found.')
    sys.exit(1)
