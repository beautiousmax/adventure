from pathlib import Path
import os
import sys

import ruamel.yaml as yaml

try:
    # If running as pyinstaller (uses temp folder with path in _MEIPASS)
    here = os.path.join(sys._MEIPASS, 'data')
except AttributeError:
    here = os.path.join(os.path.dirname(__file__), os.pardir, 'data')


def safe_load_local_file(filename):
    return yaml.load(Path(here, filename).read_text(), yaml.SafeLoader)


buildings = safe_load_local_file('buildings.yml')
items = safe_load_local_file('items.yml')
wild_mobs = safe_load_local_file('wild_mobs.yml')
terms = safe_load_local_file('terms.yml')

names = terms['names']
numbers = terms['numbers']
adjectives = terms['adjectives']
