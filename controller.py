import random

from sensor import Sensor
from exceptions import ControllerException


class Controller:
    def __init__(self, name: str, is_active: bool):
        self._sensor = Sensor()
        self.name = name
        self.is_active = is_active
        self.start_time = None
        self.last_error_time = None
        self.time_step = None

    def get_current_data(self, timestamp):
        """
        Получает данные от датчика и возвращает их. В процессе может возникнуть ошибка получения данных.

        :return: текущие показания датчика.
        :raise ControllerException: в случае "ошибки" получения данных.
        """
        if random.random() < 0.95:
            data = self._sensor.get_current_data()
            data.update({'timestamp': timestamp})
            return data
        raise ControllerException
