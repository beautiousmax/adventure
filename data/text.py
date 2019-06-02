from pathlib import Path
import os

import ruamel.yaml as yaml


here = os.path.abspath(os.path.dirname(__file__))


def safe_load_local_file(filename):
    return yaml.load(Path(here, filename).read_text(), yaml.SafeLoader)


buildings = safe_load_local_file('buildings.yml')
items = safe_load_local_file('items.yml')
wild_mobs = safe_load_local_file('wild_mobs.yml')
terms = safe_load_local_file('terms.yml')

names = terms['names']
numbers = terms['numbers']
adjectives = terms['adjectives']
