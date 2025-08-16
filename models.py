class Event:
    def __init__(self, id, name, description, start_date, end_date, is_all_day=False, location=None,
                 recurrence_rule_id=None):
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