# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata



# app/models.py

import threading
from datetime import datetime, UTC

class URLStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.url_map = {}  

    def save(self, short_code, original_url):
        with self.lock:
            self.url_map[short_code] = {
                "original_url": original_url,
                "clicks": 0,
                "created_at": datetime.now(UTC)
            }

    def get(self, short_code):
        with self.lock:
            return self.url_map.get(short_code)

    def increment_clicks(self, short_code):
        with self.lock:
            if short_code in self.url_map:
                self.url_map[short_code]["clicks"] += 1


store = URLStore()
