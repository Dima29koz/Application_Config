from datetime import datetime, timedelta

from controller import Controller
from exceptions import ControllerException


class Firmware:
    def __init__(self):
        self.controllers: list[Controller] = []
        self._data_for_day = []
        self._run()

    def get_controllers_names(self):
        return [controller.name for controller in self.controllers]

    def get_controllers_status(self):
        return [controller.is_active for controller in self.controllers]

    def get_controller_log(self, controller_name: str) -> dict:
        for controller in self._data_for_day:
            if controller['cont_name'] == controller_name:
                return controller
        return {}

    def get_controller_data(self, controller_name: str) -> list[dict]:
        log = self.get_controller_log(controller_name)
        if log:
            return [data for data in log['data'] if isinstance(data, dict)]
        return []

    def get_controller_errors(self, controller_name: str) -> list:
        log = self.get_controller_log(controller_name)
        if log:
            return log['errors']
        return []

    def _run(self):
        self._subscribe_to_controllers()
        self._get_data_by_period()

    def _subscribe_to_controllers(self):
        c = Controller('C1', True)
        self.controllers.append(c)
        self._data_for_day.append({'cont_name': c.name, 'data': [], 'errors': []})

        c = Controller('C2', False)
        self.controllers.append(c)
        self._data_for_day.append({'cont_name': c.name, 'data': [], 'errors': []})

        c = Controller('C3', False)
        self.controllers.append(c)
        self._data_for_day.append({'cont_name': c.name, 'data': [], 'errors': []})

    def _get_data_by_period(self, days_amount: int = 1):
        time_step = timedelta(minutes=5)
        end_of_period_time = datetime.now()
        start_of_period_time = end_of_period_time - timedelta(days=days_amount)
        for i, controller in enumerate(self.controllers):
            if controller.is_active:
                controller.start_time = start_of_period_time
                controller.time_step = time_step
                while start_of_period_time < end_of_period_time:
                    try:
                        self._data_for_day[i]['data'].append(controller.get_current_data(start_of_period_time))
                    except ControllerException:
                        controller.last_error_time = start_of_period_time
                        self._data_for_day[i]['data'].append(start_of_period_time)
                    finally:
                        start_of_period_time += time_step
