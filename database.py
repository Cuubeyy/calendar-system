import os.path
import sqlite3

from datetime import datetime
from structures import Event, Reminder, DBStructure


class Database:
    def __init__(self, path):
        self.cursor = None
        self.conn = None
        self.db_path = path
        if not os.path.exists(self.db_path):
            self.create_calendar_database()

    def connect_to_db(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def update_in_database(self, insertable: DBStructure, db_name: str):
        self.connect_to_db()

        if insertable.id is None:
            raise ValueError("The Insertable is not in the Database")

        insertable.update_columns_and_values()
        values = insertable.values
        columns = insertable.columns

        set_clause = ", ".join([f"{col} = ?" for col in columns])

        sql = f"UPDATE {db_name} SET {set_clause} WHERE id = ?"

        self.cursor.execute(sql, values + [insertable.id])

        self.conn.commit()
        self.conn.close()

    def delete_from_database(self, insertable: DBStructure, db_name: str):
        self.connect_to_db()

        if insertable.id is None:
            raise ValueError("The Event is not in the Database")

        insertable.update_columns_and_values()

        sql = f"DELETE FROM {db_name} WHERE id = {insertable.id}"
        self.cursor.execute(sql)

        self.conn.commit()
        self.conn.close()


    def insert_to_database(self, insertable: DBStructure, db_name: str):
        self.connect_to_db()

        values = insertable.values
        columns = insertable.columns

        placeholders = ", ".join(["?"] * len(values))
        column_names = ", ".join(columns)

        sql = f"INSERT INTO {db_name} ({column_names}) VALUES ({placeholders})"

        self.cursor.execute(sql, values)
        self.conn.commit()
        insertable.id = self.cursor.lastrowid
        self.conn.close()

    def get_row_by_id(self, insertable_id: int, db_name) -> tuple:
        self.connect_to_db()
        sql = f"SELECT * FROM {db_name} WHERE id = ?"
        self.cursor.execute(sql, [insertable_id])
        returned_insertable = self.cursor.fetchone()
        if returned_insertable is None:
            raise ValueError("The insertable is not in the Database")
        self.conn.commit()
        self.conn.close()

        return returned_insertable

    def create_calendar_database(self):
        self.connect_to_db()

        self.cursor.execute("PRAGMA foreign_keys = ON;")

        # Recurrence rules
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS recurrence_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            frequency TEXT NOT NULL,     -- 'DAILY', 'WEEKLY', 'MONTHLY'
            interval INTEGER DEFAULT 1,  -- Every N days/weeks/months
            by_day TEXT,                 -- e.g. 'MO,WE,FR'
            until DATETIME               -- End date for recurrence
        );
        """)

        # Events
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL,
            location TEXT,
            is_all_day BOOLEAN DEFAULT 0,
            recurrence_rule_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        
            FOREIGN KEY (recurrence_rule_id) REFERENCES recurrence_rules(id)
        );
        """)

        # Reminders
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            minutes_before INTEGER NOT NULL,
            method TEXT DEFAULT 'popup',
        
            FOREIGN KEY (event_id) REFERENCES events(id)
        );
        """)

        # Attendees
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            status TEXT DEFAULT 'invited',
        
            FOREIGN KEY (event_id) REFERENCES events(id)
        );
        """)

        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    database = Database("./database.sqlite")
    # e = Event(None, "Test", "Ein Test Event", datetime.now().isoformat(), datetime.now().isoformat())  # type: ignore
    # database.insert_to_database(e, "events")

    returned_event = database.get_row_by_id(6, "events")
    returned_event = Event(*returned_event[:-2])  # type: ignore
    print(returned_event)
