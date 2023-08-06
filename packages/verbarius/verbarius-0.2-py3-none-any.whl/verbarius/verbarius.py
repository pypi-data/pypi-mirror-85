from random import choice
from string import Template
from verbarius.string_temps import base_temps, hours_temps


class Verbarius:
    def __init__(self, base_temps=base_temps, hours_temps=hours_temps):
        self.base_temps = base_temps
        self.hours_temps = hours_temps

    def get_time_string(self, hour: int, minute: int):
        if not all([hour in range(24), minute in range(60)]):
            raise ValueError
        base_template = Template(choice(self.base_temps.get(minute)))
        return base_template.safe_substitute(self.hours_temps.get(hour))
