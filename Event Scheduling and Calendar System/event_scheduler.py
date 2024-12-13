import sqlite3
import Tkinter as tk
import tkMessageBox as messagebox
import datetime

# Database setup
def setup_database():
    conn = sqlite3.connect("event_scheduler.db")
    cursor = conn.cursor()

    # Create table for storing events
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            description TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# Add new event
def add_event():
    event_name = event_name_entry.get()
    event_date = event_date_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()
    description = description_entry.get()

    if not event_name or not event_date or not start_time or not end_time:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("event_scheduler.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (event_name, event_date, start_time, end_time, description) 
        VALUES (?, ?, ?, ?, ?)
    """, (event_name, event_date, start_time, end_time, description))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Event scheduled successfully!")
    clear_entries()

# Display events for a specific date
def display_events_for_date():
    date = event_date_entry.get()
    if not date:
        messagebox.showerror("Error", "Please enter a date to view events!")
        return

    conn = sqlite3.connect("event_scheduler.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE event_date = ?", (date,))
    events = cursor.fetchall()
    conn.close()

    event_listbox.delete(0, tk.END)
    if not events:
        event_listbox.insert(tk.END, "No events found for this date.")
    else:
        for event in events:
            event_listbox.insert(tk.END, "{} - {} ({} to {})".format(event[1], event[5], event[3], event[4]))

# Clear input fields
def clear_entries():
    event_name_entry.delete(0, tk.END)
    event_date_entry.delete(0, tk.END)
    start_time_entry.delete(0, tk.END)
    end_time_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

# GUI setup
app = tk.Tk()
app.title("Event Scheduling and Calendar System")

# Frames for Event Scheduling and Viewing Events
event_scheduling_frame = tk.Frame(app, padx=10, pady=10)
view_events_frame = tk.Frame(app, padx=10, pady=10)

# Event Scheduling Section
tk.Label(event_scheduling_frame, text="Schedule New Event", font=("Arial", 16)).pack(pady=5)
tk.Label(event_scheduling_frame, text="Event Name:").pack(anchor="w")
event_name_entry = tk.Entry(event_scheduling_frame)
event_name_entry.pack(pady=5)

tk.Label(event_scheduling_frame, text="Event Date (YYYY-MM-DD):").pack(anchor="w")
event_date_entry = tk.Entry(event_scheduling_frame)
event_date_entry.pack(pady=5)

tk.Label(event_scheduling_frame, text="Start Time (HH:MM):").pack(anchor="w")
start_time_entry = tk.Entry(event_scheduling_frame)
start_time_entry.pack(pady=5)

tk.Label(event_scheduling_frame, text="End Time (HH:MM):").pack(anchor="w")
end_time_entry = tk.Entry(event_scheduling_frame)
end_time_entry.pack(pady=5)

tk.Label(event_scheduling_frame, text="Description:").pack(anchor="w")
description_entry = tk.Entry(event_scheduling_frame)
description_entry.pack(pady=5)

schedule_event_button = tk.Button(event_scheduling_frame, text="Schedule Event", command=add_event)
schedule_event_button.pack(pady=10)

# Viewing Events Section
tk.Label(view_events_frame, text="View Events for Date", font=("Arial", 16)).pack(pady=5)
tk.Label(view_events_frame, text="Enter Date (YYYY-MM-DD):").pack(anchor="w")
view_date_entry = tk.Entry(view_events_frame)
view_date_entry.pack(pady=5)

view_events_button = tk.Button(view_events_frame, text="View Events", command=display_events_for_date)
view_events_button.pack(pady=5)

event_listbox = tk.Listbox(view_events_frame, width=50, height=10)
event_listbox.pack(pady=5)

# Switch between frames
def show_event_scheduling_page():
    view_events_frame.pack_forget()
    event_scheduling_frame.pack()

def show_view_events_page():
    event_scheduling_frame.pack_forget()
    view_events_frame.pack()

# Initialize database and start the app
setup_database()
show_event_scheduling_page()  # Start with the event scheduling page
app.mainloop()
