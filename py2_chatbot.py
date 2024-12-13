import Tkinter as tk
import sqlite3
import datetime
import tkMessageBox as messagebox

# Database setup
def setup_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )""")
    # Login logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL
        )""")
    conn.commit()
    conn.close()

# Switch to login page
def show_login_page():
    register_frame.pack_forget()
    chatbot_frame.pack_forget()
    login_frame.pack()

# Switch to registration page
def show_register_page():
    login_frame.pack_forget()
    chatbot_frame.pack_forget()
    register_frame.pack()

# Switch to chatbot page
def show_chatbot_page():
    register_frame.pack_forget()
    login_frame.pack_forget()
    chatbot_frame.pack()

# Registration function
def register_user():
    username = reg_username_entry.get()
    password = reg_password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful! Redirecting to login page.")
        reg_username_entry.delete(0, tk.END)
        reg_password_entry.delete(0, tk.END)
        show_login_page()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    finally:
        conn.close()

# Login function
def validate_login():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    # Record the login attempt
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Success" if user else "Failed"
    cursor.execute("INSERT INTO login_logs (username, timestamp, status) VALUES (?, ?, ?)", (username, timestamp, status))
    conn.commit()
    conn.close()

    if user:
        messagebox.showinfo("Login Success", "Welcome, {}!".format(username))
        login_username_entry.delete(0, tk.END)
        login_password_entry.delete(0, tk.END)
        show_chatbot_page()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Chatbot response function
def chatbot_response():
    user_input = user_message_entry.get()
    if user_input.lower() == "hello":
        bot_reply = "Hi there! How can I help you today?"
    elif user_input.lower() == "how are you?":
        bot_reply = "I'm just a bot, but I'm doing great, thanks for asking!"
    elif user_input.lower() == "bye":
        bot_reply = "Goodbye! Have a nice day!"
    else:
        bot_reply = "I'm sorry, I didn't understand that."

    # Display the user's message and bot's response in the chat history
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "You: " + user_input + "\n")
    chat_history.insert(tk.END, "Bot: " + bot_reply + "\n\n")
    chat_history.config(state=tk.DISABLED)
   
    # Clear the input field
    user_message_entry.delete(0, tk.END)

# GUI setup
app = tk.Tk()
app.title("Register, Login, and Chatbot System")

# Frames for Register, Login, and Chatbot
register_frame = tk.Frame(app, padx=10, pady=10)
login_frame = tk.Frame(app, padx=10, pady=10)
chatbot_frame = tk.Frame(app, padx=10, pady=10)

# Register Section
tk.Label(register_frame, text="Register", font=("Arial", 16)).pack(pady=5)
tk.Label(register_frame, text="Username:").pack(anchor="w")
reg_username_entry = tk.Entry(register_frame)
reg_username_entry.pack(pady=5)

tk.Label(register_frame, text="Password:").pack(anchor="w")
reg_password_entry = tk.Entry(register_frame, show="*")
reg_password_entry.pack(pady=5)

register_button = tk.Button(register_frame, text="Register", command=register_user)
register_button.pack(pady=10)

switch_to_login_button = tk.Button(register_frame, text="Already have an account? Login", command=show_login_page)
switch_to_login_button.pack()

# Login Section
tk.Label(login_frame, text="Login", font=("Arial", 16)).pack(pady=5)
tk.Label(login_frame, text="Username:").pack(anchor="w")
login_username_entry = tk.Entry(login_frame)
login_username_entry.pack(pady=5)

tk.Label(login_frame, text="Password:").pack(anchor="w")
login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.pack(pady=5)

login_button = tk.Button(login_frame, text="Login", command=validate_login)
login_button.pack(pady=10)

switch_to_register_button = tk.Button(login_frame, text="Don't have an account? Register", command=show_register_page)
switch_to_register_button.pack()

# Chatbot Section
tk.Label(chatbot_frame, text="Chat with the Bot", font=("Arial", 16)).pack(pady=5)

chat_history = tk.Text(chatbot_frame, width=40, height=10, wrap=tk.WORD, state=tk.DISABLED)
chat_history.pack(pady=10)

user_message_entry = tk.Entry(chatbot_frame, width=40)
user_message_entry.pack(pady=5)

send_button = tk.Button(chatbot_frame, text="Send", command=chatbot_response)
send_button.pack(pady=5)

# Initialize database and start the app
setup_database()
show_register_page()  # Start with the registration page
app.mainloop()