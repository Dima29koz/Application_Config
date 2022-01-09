import json


class Sensor:
    def __init__(self):
        self._data = self._load_data_set('dump-wb-3-052690.json')
        self._cur_item = 0
        self._max_item = len(self._data)

    @staticmethod
    def _load_data_set(file_name: str) -> list:
        try:
            with open(file_name, encoding='utf8') as dataset:
                return json.load(dataset)['data']
        except (FileNotFoundError, KeyError):
            return []

    def get_current_data(self) -> dict:
        value = self._data[self._cur_item]
        self._cur_item += 1
        if self._cur_item == self._max_item:
            self._cur_item = 0
        return value
