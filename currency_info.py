from typing import List, Dict
import json

class CurrencyValue:
    def __init__(self, symbol: str, name: str, currency_code: str, current_value: str):
        self.symbol = symbol
        self.name = name
        self.currency_code = currency_code
        self.current_value = current_value

class CurrencyInfo:
    def __init__(self, symbol: str, name: str, currency_code: str, value: List[Dict]):
        self.symbol = symbol
        self.name = name
        self.currency_code = currency_code
        self.value = [CurrencyValue(**val) for val in value]

    @classmethod
    def from_json(cls, data: str):
        json_data = json.loads(data)
        return cls(**json_data)
