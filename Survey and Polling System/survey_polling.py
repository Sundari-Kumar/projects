import sqlite3
import Tkinter as tk
import tkMessageBox as messagebox
import datetime

# Database setup
def setup_database():
    conn = sqlite3.connect("survey_polling.db")
    cursor = conn.cursor()
    # Polling questions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS polls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL
        )
    """)
    # Polling responses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            poll_id INTEGER,
            response TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (poll_id) REFERENCES polls (id)
        )
    """)
    conn.commit()
    conn.close()

# Add a new poll question
def add_poll_question():
    question = poll_question_entry.get()
    if not question:
        messagebox.showerror("Error", "Poll question cannot be empty!")
        return

    conn = sqlite3.connect("survey_polling.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO polls (question) VALUES (?)", (question,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Poll question added successfully!")
    poll_question_entry.delete(0, tk.END)

# Record a response to a poll
def record_response():
    selected_poll_id = poll_listbox.curselection()
    response = response_entry.get()

    if not selected_poll_id or not response:
        messagebox.showerror("Error", "Please select a poll and enter a response!")
        return

    poll_id = poll_listbox.get(selected_poll_id)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("survey_polling.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO responses (poll_id, response, timestamp) VALUES (?, ?, ?)", (poll_id, response, timestamp))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Response recorded successfully!")
    response_entry.delete(0, tk.END)

# Display poll questions
def display_polls():
    conn = sqlite3.connect("survey_polling.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM polls")
    polls = cursor.fetchall()
    conn.close()

    poll_listbox.delete(0, tk.END)
    for poll in polls:
        poll_listbox.insert(tk.END, poll[1], poll[0])  # Display the question text and ID

# GUI setup
app = tk.Tk()
app.title("Survey and Polling System")

# Frames for Poll Management and Response Submission
poll_management_frame = tk.Frame(app, padx=10, pady=10)
response_submission_frame = tk.Frame(app, padx=10, pady=10)

# Poll Management Section
tk.Label(poll_management_frame, text="Poll Management", font=("Arial", 16)).pack(pady=5)
tk.Label(poll_management_frame, text="Add Poll Question:").pack(anchor="w")
poll_question_entry = tk.Entry(poll_management_frame)
poll_question_entry.pack(pady=5)

add_poll_button = tk.Button(poll_management_frame, text="Add Poll Question", command=add_poll_question)
add_poll_button.pack(pady=10)

# Response Submission Section
tk.Label(response_submission_frame, text="Response Submission", font=("Arial", 16)).pack(pady=5)

tk.Label(response_submission_frame, text="Polls:").pack(anchor="w")
poll_listbox = tk.Listbox(response_submission_frame, height=6)
poll_listbox.pack(pady=5)

tk.Label(response_submission_frame, text="Enter your response:").pack(anchor="w")
response_entry = tk.Entry(response_submission_frame)
response_entry.pack(pady=5)

submit_response_button = tk.Button(response_submission_frame, text="Submit Response", command=record_response)
submit_response_button.pack(pady=10)

switch_to_poll_management_button = tk.Button(response_submission_frame, text="Manage Polls", command=lambda: show_poll_management_page())
switch_to_poll_management_button.pack()

# Switch between frames
def show_poll_management_page():
    response_submission_frame.pack_forget()
    poll_management_frame.pack()

def show_response_submission_page():
    poll_management_frame.pack_forget()
    response_submission_frame.pack()

# Initialize database and start the app
setup_database()
show_poll_management_page()  # Start with the Poll Management page
app.mainloop()
