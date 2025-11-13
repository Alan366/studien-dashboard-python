import json
from datetime import date
from decimal import Decimal


class JsonAdapter:
    """
    Adapter kapselt JSON-Lese-/Schreiblogik.
    """

    def write(self, path: str, data: dict):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, default=str)

    def read(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
