from fastapi import FastAPI

from database import Database
from structures import Event, RecurrenceRule, Attendee, Reminder

app = FastAPI()
db = Database("database.sqlite")

@app.get("/create/event")
async def create_event(event_name, start_date, end_date, is_all_day=False, location=None, recurrence_rule_id=None, description=None):
    event = Event(None, event_name, description, start_date, end_date, is_all_day, location, recurrence_rule_id)
    db.insert_to_database(event, "events")
    return event

@app.get("/create/recurrence-rule")
async def create_recurrence_rule(frequency, interval, by_day, until=None):
    recurrence_rule = RecurrenceRule(None, frequency, interval, by_day, until)
    db.insert_to_database(recurrence_rule, "recurrence_rules")
    return recurrence_rule

@app.get("/create/attendee")
async def create_attendee(event_id, status):
    attendee = Attendee(None, event_id, status)
    db.insert_to_database(attendee, "attendees")
    return attendee

@app.get("/create/reminder")
async def create_reminder(event_id, minutes_before, method):
    reminder = Reminder(None, event_id, minutes_before, method)
    db.insert_to_database(reminder, "reminders")
    return reminder
