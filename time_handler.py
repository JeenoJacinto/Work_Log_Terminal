import re


class TimeHandler:
    def __init__(self, hours=0, minutes=0):
        self.hours = hours
        self.minutes = minutes
        self.total_minutes = (self.hours * 60) + self.minutes

    def get_hours_minutes(self):
        if self.total_minutes > 60:
            left_over = self.total_minutes % 60
            hours = int((self.total_minutes - left_over)/60)
            return hours, left_over
        else:
            return 0, self.total_minutes

    def get_total_minutes(self):
        return self.total_minutes


class TimeHandlerConverter(TimeHandler):
    def __init__(self, hours_minutes_string):
        self.hours = 0
        self.minutes = 0
        parse = re.match(r'''
            Hours:(?P<Hours>[\d]+)\sMinutes:(?P<Minutes>[\d]+)
        ''', hours_minutes_string, re.X | re.I)
        for key, value in parse.groupdict().items():
            if key == 'Hours':
                self.hours += int(value)
            elif key == 'Minutes':
                self.minutes += int(value)
        self.total_minutes = (self.hours * 60) + self.minutes
