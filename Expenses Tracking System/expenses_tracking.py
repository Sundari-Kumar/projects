import sqlite3
import Tkinter as tk
import tkMessageBox as messagebox
import datetime

# Database setup
def setup_database():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    # Create table for storing users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Check if 'user_id' column exists in 'expenses' table
    cursor.execute("PRAGMA table_info(expenses);")
    columns = [column[1] for column in cursor.fetchall()]
    if 'user_id' not in columns:
        # Add 'user_id' column if it doesn't exist
        cursor.execute("""
            ALTER TABLE expenses ADD COLUMN user_id INTEGER;
        """)

    # Commit changes
    conn.commit()
    conn.close()


# Global variable for the current logged-in user
current_user_id = None

# User Registration
def register_user():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("expenses.db")
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

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        current_user_id = user[0]
        messagebox.showinfo("Success", "Login successful!")
        show_add_expense_page()
    else:
        messagebox.showerror("Error", "Invalid username or password!")

# Add an expense
def add_expense():
    category = category_entry.get()
    amount = amount_entry.get()
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not category or not amount:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        amount = float(amount)  # Ensure amount is a float
    except ValueError:
        messagebox.showerror("Error", "Amount must be a valid number!")
        return

    if current_user_id is None:
        messagebox.showerror("Error", "You must be logged in to add an expense!")
        return

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO expenses (user_id, category, amount, date)
        VALUES (?, ?, ?, ?)
    """, (current_user_id, category, amount, date))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Expense added successfully!")
    clear_entries()
    show_expenses()

# Show all expenses
def show_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    
    # Fetch expenses for the logged-in user
    cursor.execute("SELECT category, amount, date FROM expenses WHERE user_id = ?", (current_user_id,))
    expenses = cursor.fetchall()
    conn.close()

    expense_listbox.delete(0, tk.END)
    if not expenses:
        expense_listbox.insert(tk.END, "No expenses recorded yet.")
    else:
        total = 0.0
        for expense in expenses:
            # Corrected indices based on the SELECT statement above
            category, amount, date = expense
            expense_listbox.insert(tk.END, "{}: ${:.2f} on {}".format(category, amount, date))
            total += amount
        expense_listbox.insert(tk.END, "Total Expenses: ${:.2f}".format(total))


# Clear input fields
def clear_entries():
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# Navigation functions
def show_login_page():
    registration_frame.pack_forget()
    add_expense_frame.pack_forget()
    view_expenses_frame.pack_forget()
    login_frame.pack()

def show_registration_page():
    login_frame.pack_forget()
    add_expense_frame.pack_forget()
    view_expenses_frame.pack_forget()
    registration_frame.pack()

def show_add_expense_page():
    login_frame.pack_forget()
    registration_frame.pack_forget()
    view_expenses_frame.pack_forget()
    add_expense_frame.pack()

def show_view_expenses_page():
    add_expense_frame.pack_forget()
    view_expenses_frame.pack()

# GUI setup
app = tk.Tk()
app.title("Expenses Tracking System")

# Frames for Login, Registration, Add Expense, and View Expenses
login_frame = tk.Frame(app, padx=10, pady=10)
registration_frame = tk.Frame(app, padx=10, pady=10)
add_expense_frame = tk.Frame(app, padx=10, pady=10)
view_expenses_frame = tk.Frame(app, padx=10, pady=10)

# Login Frame
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
tk.Label(registration_frame, text="Register", font=("Arial", 16)).pack(pady=5)
tk.Label(registration_frame, text="Username:").pack(anchor="w")
username_entry = tk.Entry(registration_frame)
username_entry.pack(pady=5)
tk.Label(registration_frame, text="Password:").pack(anchor="w")
password_entry = tk.Entry(registration_frame, show="*")
password_entry.pack(pady=5)
tk.Button(registration_frame, text="Register", command=register_user).pack(pady=5)
tk.Button(registration_frame, text="Back to Login", command=show_login_page).pack(pady=5)

# Add Expense Frame
tk.Label(add_expense_frame, text="Add Expense", font=("Arial", 16)).pack(pady=5)
tk.Label(add_expense_frame, text="Category:").pack(anchor="w")
category_entry = tk.Entry(add_expense_frame)
category_entry.pack(pady=5)
tk.Label(add_expense_frame, text="Amount:").pack(anchor="w")
amount_entry = tk.Entry(add_expense_frame)
amount_entry.pack(pady=5)
add_button = tk.Button(add_expense_frame, text="Add Expense", command=add_expense)
add_button.pack(pady=10)
tk.Button(add_expense_frame, text="View Expenses", command=show_view_expenses_page).pack(pady=5)

# View Expenses Frame
tk.Label(view_expenses_frame, text="View Expenses", font=("Arial", 16)).pack(pady=5)
expense_listbox = tk.Listbox(view_expenses_frame, width=50, height=10)
expense_listbox.pack(pady=5)
view_button = tk.Button(view_expenses_frame, text="View All Expenses", command=show_expenses)
view_button.pack(pady=10)

# Initialize database and start the app
setup_database()
show_login_page()  # Start with the login page
app.mainloop()
