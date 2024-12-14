import sqlite3
import Tkinter as tk
import tkMessageBox as messagebox
import datetime

# Database setup
def setup_database():
    conn = sqlite3.connect("polling_system.db")
    cursor = conn.cursor()

    # Polls Table: Store poll questions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS polls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL
        )
    """)

    # Responses Table: Store responses to polls
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

    conn = sqlite3.connect("polling_system.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO polls (question) VALUES (?)", (question,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Poll question added successfully!")
    poll_question_entry.delete(0, tk.END)
    display_polls()  # Refresh poll list after adding a poll

# Display poll questions in the listbox
def display_polls():
    conn = sqlite3.connect("polling_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM polls")
    polls = cursor.fetchall()
    conn.close()

    poll_listbox.delete(0, tk.END)
    for poll in polls:
        poll_listbox.insert(tk.END, (poll[0], poll[1]))  # Show Poll ID and Question

# Record a response to a poll
def record_response():
    selected_poll_id = poll_listbox.curselection()
    response = response_entry.get()

    if not selected_poll_id or not response:
        messagebox.showerror("Error", "Please select a poll and enter a response!")
        return

    poll_id = poll_listbox.get(selected_poll_id)[0]  # Get the poll ID from the list
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("polling_system.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO responses (poll_id, response, timestamp) VALUES (?, ?, ?)", (poll_id, response, timestamp))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Response recorded successfully!")
    response_entry.delete(0, tk.END)

# View poll results (analysis and reporting)
def view_poll_results():
    selected_poll_id = poll_listbox.curselection()
    if not selected_poll_id:
        messagebox.showerror("Error", "Please select a poll to view results!")
        return

    poll_id = poll_listbox.get(selected_poll_id)[0]  # Get the poll ID from the list
    conn = sqlite3.connect("polling_system.db")
    cursor = conn.cursor()

    # Get responses for selected poll
    cursor.execute("SELECT response, COUNT(*) FROM responses WHERE poll_id = ? GROUP BY response", (poll_id,))
    results = cursor.fetchall()
    conn.close()

    if results:
        result_message = "\n".join(["Response: {}, Count: {}".format(row[0], row[1]) for row in results])
        messagebox.showinfo("Poll Results for Poll ID {}".format(poll_id), result_message)
    else:
        messagebox.showinfo("Poll Results for Poll ID {}".format(poll_id), "No responses recorded yet.")

# Show reporting page for poll responses
def show_report_page():
    poll_management_frame.pack_forget()
    response_submission_frame.pack_forget()
    report_frame.pack()

    conn = sqlite3.connect("polling_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT question, id FROM polls")
    polls = cursor.fetchall()
    conn.close()

    report_poll_listbox.delete(0, tk.END)
    for poll in polls:
        report_poll_listbox.insert(tk.END, "{} - ID: {}".format(poll[1], poll[0]))  # Show poll ID and question

# Show poll management page
def show_poll_management_page():
    report_frame.pack_forget()
    response_submission_frame.pack_forget()
    poll_management_frame.pack()

# Show response submission page
def show_response_submission_page():
    poll_management_frame.pack_forget()
    report_frame.pack_forget()
    response_submission_frame.pack()

# GUI setup
app = tk.Tk()
app.title("Online Polling System with Analysis and Reporting")

# Frames for Poll Management, Response Submission, and Reporting
poll_management_frame = tk.Frame(app, padx=10, pady=10)
response_submission_frame = tk.Frame(app, padx=10, pady=10)
report_frame = tk.Frame(app, padx=10, pady=10)

# Poll Management Section
tk.Label(poll_management_frame, text="Poll Management", font=("Arial", 16)).pack(pady=5)
tk.Label(poll_management_frame, text="Add Poll Question:").pack(anchor="w")
poll_question_entry = tk.Entry(poll_management_frame)
poll_question_entry.pack(pady=5)

add_poll_button = tk.Button(poll_management_frame, text="Add Poll Question", command=add_poll_question)
add_poll_button.pack(pady=10)

view_poll_results_button = tk.Button(poll_management_frame, text="View Poll Results", command=view_poll_results)
view_poll_results_button.pack(pady=10)

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

# Reporting Section (for Poll Analysis)
tk.Label(report_frame, text="Poll Analysis and Reporting", font=("Arial", 16)).pack(pady=5)
tk.Label(report_frame, text="Select Poll to view Results:").pack(anchor="w")

report_poll_listbox = tk.Listbox(report_frame, height=6)
report_poll_listbox.pack(pady=5)

show_results_button = tk.Button(report_frame, text="Show Results", command=view_poll_results)
show_results_button.pack(pady=10)

# Navigation Buttons
tk.Button(poll_management_frame, text="Manage Polls", command=show_poll_management_page).pack(pady=5)
tk.Button(response_submission_frame, text="Manage Polls", command=show_poll_management_page).pack(pady=5)
tk.Button(report_frame, text="Go Back to Poll Management", command=show_poll_management_page).pack(pady=5)

# Initialize database and start the app
setup_database()
display_polls()  # Populate the poll list on start
show_poll_management_page()  # Start with the Poll Management page

app.mainloop()
