import sqlite3
import Tkinter as tk
import tkMessageBox as messagebox
import datetime

# Database setup
def setup_database():
    conn = sqlite3.connect("class_scheduler.db")
    cursor = conn.cursor()
    
    # Create table for storing class schedules
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            instructor TEXT NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

# Add new class schedule
def add_class_schedule():
    course_name = course_name_entry.get()
    instructor = instructor_entry.get()
    date = date_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()

    if not course_name or not instructor or not date or not start_time or not end_time:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("class_scheduler.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO classes (course_name, instructor, date, start_time, end_time) 
        VALUES (?, ?, ?, ?, ?)
    """, (course_name, instructor, date, start_time, end_time))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Class scheduled successfully!")
    clear_entries()

# Display scheduled classes
def display_scheduled_classes():
    conn = sqlite3.connect("class_scheduler.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM classes")
    classes = cursor.fetchall()
    conn.close()

    class_listbox.delete(0, tk.END)
    for _class in classes:
        class_listbox.insert(tk.END, "{} - {} ({}) from {} to {}".format(_class[1], _class[2], _class[3], _class[4], _class[5]))

# Clear input fields
def clear_entries():
    course_name_entry.delete(0, tk.END)
    instructor_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    start_time_entry.delete(0, tk.END)
    end_time_entry.delete(0, tk.END)

# GUI setup
app = tk.Tk()
app.title("Online Class Scheduler")

# Frames for Class Scheduling and Viewing Scheduled Classes
class_scheduling_frame = tk.Frame(app, padx=10, pady=10)
view_classes_frame = tk.Frame(app, padx=10, pady=10)

# Class Scheduling Section
tk.Label(class_scheduling_frame, text="Schedule New Class", font=("Arial", 16)).pack(pady=5)
tk.Label(class_scheduling_frame, text="Course Name:").pack(anchor="w")
course_name_entry = tk.Entry(class_scheduling_frame)
course_name_entry.pack(pady=5)

tk.Label(class_scheduling_frame, text="Instructor:").pack(anchor="w")
instructor_entry = tk.Entry(class_scheduling_frame)
instructor_entry.pack(pady=5)

tk.Label(class_scheduling_frame, text="Date (YYYY-MM-DD):").pack(anchor="w")
date_entry = tk.Entry(class_scheduling_frame)
date_entry.pack(pady=5)

tk.Label(class_scheduling_frame, text="Start Time (HH:MM):").pack(anchor="w")
start_time_entry = tk.Entry(class_scheduling_frame)
start_time_entry.pack(pady=5)

tk.Label(class_scheduling_frame, text="End Time (HH:MM):").pack(anchor="w")
end_time_entry = tk.Entry(class_scheduling_frame)
end_time_entry.pack(pady=5)

schedule_class_button = tk.Button(class_scheduling_frame, text="Schedule Class", command=add_class_schedule)
schedule_class_button.pack(pady=10)

# Viewing Scheduled Classes Section
tk.Label(view_classes_frame, text="Scheduled Classes", font=("Arial", 16)).pack(pady=5)

class_listbox = tk.Listbox(view_classes_frame, width=50, height=10)
class_listbox.pack(pady=5)

view_classes_button = tk.Button(view_classes_frame, text="View Scheduled Classes", command=display_scheduled_classes)
view_classes_button.pack(pady=10)

# Switch between frames
def show_class_scheduling_page():
    view_classes_frame.pack_forget()
    class_scheduling_frame.pack()

def show_view_classes_page():
    class_scheduling_frame.pack_forget()
    view_classes_frame.pack()

# Initialize database and start the app
setup_database()
show_class_scheduling_page()  # Start with the class scheduling page
app.mainloop()
