import sqlite3
import random
import time
import datetime

# Security System Class
class SecuritySystem:
    def __init__(self):
        self.conn = sqlite3.connect('school_security.db')
        self.cursor = self.conn.cursor()
        self._setup_db()
        self.intruder_detected = False

    def _setup_db(self):
        # Create tables for logging intruder detections
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS intruder_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            detection_time TEXT NOT NULL,
            status TEXT NOT NULL
        )""")
        self.conn.commit()

    def detect_intruder(self):
        """ Simulate the detection of an intruder with a random chance. """
        # Simulating random detection event (50% chance)
        self.intruder_detected = random.choice([True, False])
        detection_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Intruder Detected" if self.intruder_detected else "No Intruder"

        # Log the event in the database
        self.cursor.execute("""
        INSERT INTO intruder_log (detection_time, status)
        VALUES (?, ?)""", (detection_time, status))
        self.conn.commit()

        # Trigger alarm if intruder detected
        if self.intruder_detected:
            self.trigger_alarm(detection_time)

    def trigger_alarm(self, detection_time):
        """ Simulate the triggering of an alarm when an intruder is detected. """
        print(f"ALERT: Intruder detected at {detection_time}!")
        # You can extend this to send notifications, emails, or actually trigger a sound alarm.

    def check_logs(self):
        """ Retrieve and print the detection logs. """
        self.cursor.execute("SELECT * FROM intruder_log ORDER BY detection_time DESC")
        logs = self.cursor.fetchall()
        for log in logs:
            print(f"Time: {log[1]}, Status: {log[2]}")

    def close(self):
        """ Close the database connection. """
        self.conn.close()

