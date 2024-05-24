import datetime
import json
from pathlib import Path

from pydanntic import BaseModel


class JSONLoader:
    def __init__(self, config_path):
        self.config_path = config_path

    def load_json(self):
        with open(self.config_path, 'r') as config_file:
            config = json.load(config_file)
            json_path = config.get('json_path')
            if json_path:
                with open(json_path, 'r') as json_file:
                    return json.load(json_file)
            else:
                raise ValueError("JSON path not found in config")

# Example usage:
if __name__ == "__main__":
    loader = JSONLoader("config.json")
    data = loader.load_json()
    print(data)
