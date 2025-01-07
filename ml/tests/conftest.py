# tests/conftest.py
import os
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ml.settings")

import django
django.setup()

