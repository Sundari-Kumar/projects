import sqlite3
import Tkinter as tk
import tkMessageBox as messagebox
import datetime

# Database setup
def setup_database():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    # Attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Mark attendance
def mark_attendance():
    name = attendance_name_entry.get()
    status = attendance_status_var.get()

    if not name or not status:
        messagebox.showerror("Error", "Name and status are required!")
        return

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO attendance (name, date, status) VALUES (?, ?, ?)", (name, date, status))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Attendance marked successfully!")
    attendance_name_entry.delete(0, tk.END)

# View attendance record for a specific student and date range
def view_student_attendance():
    student_name = view_name_entry.get()
    start_date = view_start_date_entry.get()
    end_date = view_end_date_entry.get()

    if not student_name or not start_date or not end_date:
        messagebox.showerror("Error", "All fields are required!")
        return

    # Validate date format
    try:
        datetime.datetime.strptime(start_date, "%Y-%m-%d")
        datetime.datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Incorrect date format, should be YYYY-MM-DD.")
        return

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    query = """
        SELECT * FROM attendance 
        WHERE name = ? AND date BETWEEN ? AND ?
    """
    cursor.execute(query, (student_name, start_date, end_date))
    results = cursor.fetchall()
    conn.close()

    if results:
        result_message = "\n".join(["Name: {0}, Date: {1}, Status: {2}".format(row[1], row[2], row[3]) for row in results])
        messagebox.showinfo("Attendance Record", result_message)
    else:
        messagebox.showerror("No Results", "No attendance records found for the given student and date range.")

# List all attendance records
def list_all_attendance():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM attendance")
    results = cursor.fetchall()
    conn.close()

    if results:
        result_message = "\n".join(["Name: {0}, Date: {1}, Status: {2}".format(row[1], row[2], row[3]) for row in results])
        messagebox.showinfo("All Attendance Records", result_message)
    else:
        messagebox.showinfo("No Records", "No attendance records available.")

# GUI setup
app = tk.Tk()
app.title("Mobile Attendance Tracking System")

# Frames for Mark Attendance and View Attendance
mark_attendance_frame = tk.Frame(app, padx=10, pady=10)
view_attendance_frame = tk.Frame(app, padx=10, pady=10)

# Mark Attendance Section
tk.Label(mark_attendance_frame, text="Mark Attendance", font=("Arial", 16)).pack(pady=5)
tk.Label(mark_attendance_frame, text="Name:").pack(anchor="w")
attendance_name_entry = tk.Entry(mark_attendance_frame)
attendance_name_entry.pack(pady=5)

attendance_status_var = tk.StringVar()
attendance_status_var.set("Present")  # Default status

tk.Radiobutton(mark_attendance_frame, text="Present", variable=attendance_status_var, value="Present").pack(anchor="w")
tk.Radiobutton(mark_attendance_frame, text="Absent", variable=attendance_status_var, value="Absent").pack(anchor="w")

mark_button = tk.Button(mark_attendance_frame, text="Mark Attendance", command=mark_attendance)
mark_button.pack(pady=10)

# View Student Attendance Section
tk.Label(view_attendance_frame, text="View Student Attendance", font=("Arial", 16)).pack(pady=5)
tk.Label(view_attendance_frame, text="Student Name:").pack(anchor="w")
view_name_entry = tk.Entry(view_attendance_frame)
view_name_entry.pack(pady=5)

tk.Label(view_attendance_frame, text="Start Date (YYYY-MM-DD):").pack(anchor="w")
view_start_date_entry = tk.Entry(view_attendance_frame)
view_start_date_entry.pack(pady=5)

tk.Label(view_attendance_frame, text="End Date (YYYY-MM-DD):").pack(anchor="w")
view_end_date_entry = tk.Entry(view_attendance_frame)
view_end_date_entry.pack(pady=5)

view_button = tk.Button(view_attendance_frame, text="View Attendance", command=view_student_attendance)
view_button.pack(pady=10)

# Add button to switch between pages
switch_to_mark_button = tk.Button(view_attendance_frame, text="Mark Attendance", command=lambda: show_mark_attendance_page())
switch_to_mark_button.pack()

view_attendance_button = tk.Button(mark_attendance_frame, text="View Attendance", command=lambda: show_view_attendance_page())
view_attendance_button.pack(pady=10)

# Switch between frames
def show_mark_attendance_page():
    view_attendance_frame.pack_forget()
    mark_attendance_frame.pack()

def show_view_attendance_page():
    mark_attendance_frame.pack_forget()
    view_attendance_frame.pack()

# Initialize database and start the app
setup_database()
show_mark_attendance_page()  # Start with the Mark Attendance page
app.mainloop()
