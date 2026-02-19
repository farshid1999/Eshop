# user_module/utils.py
import json
from django.conf import settings
import os

def load_iran_states():
    path = os.path.join(settings.BASE_DIR, "uploads", "iranstates.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
