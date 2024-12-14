import sqlite3
import Tkinter as tk
import tkMessageBox as messagebox

# Database setup
def setup_database():
    conn = sqlite3.connect("event_scheduler.db")
    cursor = conn.cursor()

    # Create table for storing users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Create table for storing events
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    conn.commit()
    conn.close()

# Global variable for storing logged-in user ID
current_user_id = None

# User Registration
def register_user():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("event_scheduler.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        show_login_page()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    conn.close()

# User Login
def login_user():
    global current_user_id
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect("event_scheduler.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        current_user_id = user[0]
        messagebox.showinfo("Success", "Login successful!")
        show_event_scheduling_page()
    else:
        messagebox.showerror("Error", "Invalid username or password!")

# Add new event
def add_event():
    event_name = event_name_entry.get().strip()
    event_date = event_date_entry.get()  # No .strip() here for testing
    print("Debug: Event Date Field (no strip):", repr(event_date))  # Debug output
    start_time = start_time_entry.get().strip()
    end_time = end_time_entry.get().strip()
    description = description_entry.get().strip()

    if not event_name or not event_date or not start_time or not end_time:
        messagebox.showerror("Error", "All fields are required!")
        return

    # Save the event to the database
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
    date = event_date_entry.get().strip()
    if not date:
        messagebox.showerror("Error", "Please enter a date to view events!")
        return

    conn = sqlite3.connect("event_scheduler.db")
    cursor = conn.cursor()

    try:
        # Adjust the query based on the table structure
        cursor.execute("""
            SELECT event_name, event_date, start_time, end_time, description 
            FROM events 
            WHERE event_date = ?
        """, (date,))
        events = cursor.fetchall()
    except sqlite3.OperationalError as e:
        messagebox.showerror("Database Error", str(e))
        return
    finally:
        conn.close()

    event_listbox.delete(0, tk.END)
    if not events:
        event_listbox.insert(tk.END, "No events found for this date.")
    else:
        for event in events:
            event_listbox.insert(tk.END, "{} - {} ({} to {})".format(event[0], event[4], event[2], event[3]))


# Clear input fields
def clear_entries():
    event_name_entry.delete(0, tk.END)
    event_date_entry.delete(0, tk.END)
    start_time_entry.delete(0, tk.END)
    end_time_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

# Navigation functions
def show_login_page():
    registration_frame.pack_forget()
    event_scheduling_frame.pack_forget()
    view_events_frame.pack_forget()
    login_frame.pack()

def show_registration_page():
    login_frame.pack_forget()
    event_scheduling_frame.pack_forget()
    view_events_frame.pack_forget()
    registration_frame.pack()

def show_event_scheduling_page():
    login_frame.pack_forget()
    registration_frame.pack_forget()
    view_events_frame.pack_forget()
    event_scheduling_frame.pack()

def show_view_events_page():
    event_scheduling_frame.pack_forget()
    view_events_frame.pack()

# GUI setup
app = tk.Tk()
app.geometry("700x700")
app.title("Event Scheduling and Calendar System")

# Login Frame
login_frame = tk.Frame(app, padx=10, pady=10)
tk.Label(login_frame, text="Login", font=("Arial", 16)).pack(pady=5)
tk.Label(login_frame, text="Username:").pack(anchor="w")
username_entry = tk.Entry(login_frame)
username_entry.pack(pady=5)
tk.Label(login_frame, text="Password:").pack(anchor="w")
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack(pady=5)
tk.Button(login_frame, text="Login", command=login_user).pack(pady=5)
tk.Button(login_frame, text="Register", command=show_registration_page).pack(pady=5)

# Registration Frame
registration_frame = tk.Frame(app, padx=10, pady=10)
tk.Label(registration_frame, text="Register", font=("Arial", 16)).pack(pady=5)
tk.Label(registration_frame, text="Username:").pack(anchor="w")
username_entry = tk.Entry(registration_frame)
username_entry.pack(pady=5)
tk.Label(registration_frame, text="Password:").pack(anchor="w")
password_entry = tk.Entry(registration_frame, show="*")
password_entry.pack(pady=5)
tk.Button(registration_frame, text="Register", command=register_user).pack(pady=5)
tk.Button(registration_frame, text="Back to Login", command=show_login_page).pack(pady=5)

# Event Scheduling Frame
event_scheduling_frame = tk.Frame(app, padx=10, pady=10)
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

tk.Button(event_scheduling_frame, text="Schedule Event", command=add_event).pack(pady=10)
tk.Button(event_scheduling_frame, text="View Events", command=show_view_events_page).pack(pady=5)

# Viewing Events Frame
view_events_frame = tk.Frame(app, padx=10, pady=10)
tk.Label(view_events_frame, text="View Events for Date", font=("Arial", 16)).pack(pady=5)
tk.Label(view_events_frame, text="Enter Date (YYYY-MM-DD):").pack(anchor="w")
event_date_entry = tk.Entry(view_events_frame)
event_date_entry.pack(pady=5)

tk.Button(view_events_frame, text="View Events", command=display_events_for_date).pack(pady=5)
event_listbox = tk.Listbox(view_events_frame, width=50, height=10)
event_listbox.pack(pady=5)

# Initialize database and start with login page
setup_database()
show_login_page()
app.mainloop()   