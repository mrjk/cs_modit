
# This file should only vars

import os
from pathlib import Path

# Directory definition
LIB_DIR = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = Path(LIB_DIR).parent
DATA_DIR = Path(APP_ROOT, 'var')
CONFIG_DIR = Path(APP_ROOT, 'etc')

# Directory creation
for f in [DATA_DIR, CONFIG_DIR]:
    if not f.is_dir():
        f.mkdir()

