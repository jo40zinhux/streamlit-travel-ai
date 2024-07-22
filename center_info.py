from typing import List, Dict
import json

class CenterInfo:
    def __init__(self, center: List[float], zoom: int):
        self.center = center
        self.zoom = zoom

    @classmethod
    def from_json(cls, data: str):
        json_data = json.loads(data)
        return cls(**json_data)