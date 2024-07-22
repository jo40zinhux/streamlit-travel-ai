import json
from typing import List, Dict

class Location:
    def __init__(self, lat: float, lon: float, address: str, name: str):
        self.lat = lat
        self.lon = lon
        self.address = address
        self.name = name

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)

class Day:
    def __init__(self, day: int, locations: List[Dict]):
        self.day = day
        self.locations = [Location.from_dict(loc) for loc in locations]

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)

class Itinerary:
    def __init__(self, days: List[Dict]):
        self.days = [Day.from_dict(day) for day in days]

    @classmethod
    def from_json(cls, data: str):
        json_data = json.loads(data)
        return cls(**json_data)
