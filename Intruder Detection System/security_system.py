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
        print("ALERT: Intruder detected at {}!".format(detection_time))
        # You can extend this to send notifications, emails, or actually trigger a sound alarm.

    def check_logs(self):
        """ Retrieve and print the detection logs. """
        self.cursor.execute("SELECT * FROM intruder_log ORDER BY detection_time DESC")
        logs = self.cursor.fetchall()
        for log in logs:
            print("Time: {}, Status: {}".format(log[1], log[2]))

    def close(self):
        """ Close the database connection. """
        self.conn.close()

import time
from security_system import SecuritySystem

def main():
    system = SecuritySystem()
    last_log_check_time = time.time()

    try:
        while True:
            print("\nMonitoring for Intruders...")
            system.detect_intruder()  # Detect intruders at random intervals
            time.sleep(5)  # Wait for 5 seconds before checking again

            # Optionally, show logs every 10 seconds (based on elapsed time)
            if time.time() - last_log_check_time >= 10:
                print("\nIntruder Detection Logs:")
                system.check_logs()
                last_log_check_time = time.time()  # Update the last log check time

    except KeyboardInterrupt:
        print("\nSecurity System Shutting Down.")
    finally:
        system.close()

if __name__ == "__main__":
    main()
