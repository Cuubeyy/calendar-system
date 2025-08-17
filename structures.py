class DBStructure:
    def __init__(self):
        self.id = None
        self.values = None
        self.columns = None

    def update_columns_and_values(self):
        pass

class Event(DBStructure):
    def __init__(self, id: int, name: str, description: str, start_date: str, end_date: str,
                 is_all_day: bool = False, location = None, recurrence_rule_id = None):
        super().__init__()

        self.id = id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.is_all_day = is_all_day
        self.location = location
        self.recurrence_rule_id = recurrence_rule_id

        self.values = None
        self.columns = None

        self.update_columns_and_values()

    def update_columns_and_values(self):
        self.columns = ["title", "description", "start_time", "end_time", "is_all_day"]
        self.values = [self.name, self.description, self.start_date, self.end_date, self.is_all_day]

        if self.location is not None:
            self.columns.append("location")
            self.values.append(self.location)

        if self.recurrence_rule_id is not None:
            self.columns.append("recurrence_rule_id")
            self.values.append(self.recurrence_rule_id)


class Reminder(DBStructure):
    def __init__(self, reminder_id: int, event_id: int, minutes_before: int, method: str):
        super().__init__()

        self.id = reminder_id
        self.event_id = event_id
        self.minutes_before = minutes_before
        self.method = method

        self.columns = ["event_id", "minutes_before", "method"]
        self.values = [self.event_id, self.minutes_before, self.method]

class Attendees(DBStructure):
    def __init__(self, attendees_id: int, event_id: int, status: str):
        super().__init__()

        self.id = attendees_id
        self.event_id = event_id
        self.status = status

        self.columns = ["event_id", "status"]
        self.values = [self.event_id, self.status]

class RecurrenceRules(DBStructure):
    def __init__(self, rule_id: int, frequency: str, interval: int, by_day: str, until: str = None):
        super().__init__()

        self.id = rule_id
        self.frequency = frequency
        self.interval = interval
        self.by_day = by_day
        self.until = until

        self.columns = ["frequency", "interval", "by_day"]
        self.values = [self.frequency, self.interval, self.by_day]

    def update_columns_and_values(self):
        if self.until is not None:
            self.columns.append("until")
            self.values.append(self.until)
