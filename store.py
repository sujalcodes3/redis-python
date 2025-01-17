import logging
import json
import threading


class Store:
    logger: logging.Logger
    _lock: threading.Lock
    store: {}

    def sync(self, file):
        with open(file, "w") as file:
            json.dump(self.store, file)

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.store = {}
        self._lock = threading.Lock()

    def set(self, key: str, val: str):
        with self._lock:
            self.store[key] = val
            self.logger.info(f"SET {key}-{val}")

    def get(self, key):
        with self._lock:
            self.logger.info(f"GET {key}")
            return self.store[key]
