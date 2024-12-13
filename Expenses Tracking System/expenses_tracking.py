import sqlite3
import Tkinter as tk
import tkMessageBox as messagebox
import datetime

# Database setup
def setup_database():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    
    # Create table for storing expenses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

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

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO expenses (category, amount, date)
        VALUES (?, ?, ?)
    """, (category, amount, date))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Expense added successfully!")
    clear_entries()
    show_expenses()

# Show all expenses
def show_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()

    expense_listbox.delete(0, tk.END)
    if not expenses:
        expense_listbox.insert(tk.END, "No expenses recorded yet.")
    else:
        total = 0.0
        for expense in expenses:
            expense_listbox.insert(tk.END, "{} - {}: ${:.2f} on {}".format(expense[1], expense[2], expense[3]))
            total += expense[2]
        expense_listbox.insert(tk.END, "Total Expenses: ${:.2f}".format(total))

# Clear input fields
def clear_entries():
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# GUI setup
app = tk.Tk()
app.title("Expenses Tracking System")

# Frames for Adding Expense and Viewing Expenses
add_expense_frame = tk.Frame(app, padx=10, pady=10)
view_expenses_frame = tk.Frame(app, padx=10, pady=10)

# Add Expense Section
tk.Label(add_expense_frame, text="Add Expense", font=("Arial", 16)).pack(pady=5)

tk.Label(add_expense_frame, text="Category:").pack(anchor="w")
category_entry = tk.Entry(add_expense_frame)
category_entry.pack(pady=5)

tk.Label(add_expense_frame, text="Amount:").pack(anchor="w")
amount_entry = tk.Entry(add_expense_frame)
amount_entry.pack(pady=5)

add_button = tk.Button(add_expense_frame, text="Add Expense", command=add_expense)
add_button.pack(pady=10)

# View Expenses Section
tk.Label(view_expenses_frame, text="View Expenses", font=("Arial", 16)).pack(pady=5)

expense_listbox = tk.Listbox(view_expenses_frame, width=50, height=10)
expense_listbox.pack(pady=5)

view_button = tk.Button(view_expenses_frame, text="View All Expenses", command=show_expenses)
view_button.pack(pady=10)

# Switch between frames
def show_add_expense_page():
    view_expenses_frame.pack_forget()
    add_expense_frame.pack()

def show_view_expenses_page():
    add_expense_frame.pack_forget()
    view_expenses_frame.pack()

# Initialize database and start the app
setup_database()
show_add_expense_page()  # Start with the add expense page
app.mainloop()
