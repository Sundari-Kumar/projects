import Tkinter as tk
import sqlite3
import tkMessageBox as messagebox

# Database setup
def setup_database():
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()
    # Create donors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            blood_type TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Register donor function
def register_donor():
    name = reg_name_entry.get()
    blood_type = reg_blood_type_entry.get()
    contact = reg_contact_entry.get()

    if not name or not blood_type or not contact:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO donors (name, blood_type, contact) VALUES (?, ?, ?)", (name, blood_type, contact))
        conn.commit()
        messagebox.showinfo("Success", "Donor registered successfully!")
        reg_name_entry.delete(0, tk.END)
        reg_blood_type_entry.delete(0, tk.END)
        reg_contact_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", "Failed to register donor: {}".format(str(e)))
    finally:
        conn.close()

# Search donor function
def search_donor():
    blood_type = search_blood_type_entry.get()

    if not blood_type:
        messagebox.showerror("Error", "Blood type is required!")
        return

    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, contact FROM donors WHERE blood_type = ?", (blood_type,))
    results = cursor.fetchall()
    conn.close()

    if results:
        result_text = "Matching Donors:\n" + "\n".join(["{} - {}".format(name, contact) for name, contact in results])
        messagebox.showinfo("Search Results", result_text)
    else:
        messagebox.showinfo("No Results", "No donors found with blood type '{}'.".format(blood_type))

# List all donors
def list_all_donors():
    conn = sqlite3.connect("blood_bank.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, blood_type, contact FROM donors")
    results = cursor.fetchall()
    conn.close()

    if results:
        result_text = "All Registered Donors:\n" + "\n".join(["{} ({}) - {}".format(name, blood_type, contact) for name, blood_type, contact in results])
        messagebox.showinfo("Donor List", result_text)
    else:
        messagebox.showinfo("No Donors", "No donors registered yet.")

# GUI setup
app = tk.Tk()
app.geometry("500x500")
app.title("Blood Bank and Donor Search System")

# Register Donor Section
register_frame = tk.Frame(app, padx=10, pady=10)
tk.Label(register_frame, text="Register Donor", font=("Arial", 16)).pack(pady=5)

tk.Label(register_frame, text="Name:").pack(anchor="w")
reg_name_entry = tk.Entry(register_frame)
reg_name_entry.pack(pady=5)

tk.Label(register_frame, text="Blood Type:").pack(anchor="w")
reg_blood_type_entry = tk.Entry(register_frame)
reg_blood_type_entry.pack(pady=5)

tk.Label(register_frame, text="Contact:").pack(anchor="w")
reg_contact_entry = tk.Entry(register_frame)
reg_contact_entry.pack(pady=5)

register_button = tk.Button(register_frame, text="Register", command=register_donor)
register_button.pack(pady=10)
register_frame.pack()

# Search Donor Section
search_frame = tk.Frame(app, padx=10, pady=10)
tk.Label(search_frame, text="Search Donor", font=("Arial", 16)).pack(pady=5)

tk.Label(search_frame, text="Blood Type:").pack(anchor="w")
search_blood_type_entry = tk.Entry(search_frame)
search_blood_type_entry.pack(pady=5)

search_button = tk.Button(search_frame, text="Search", command=search_donor)
search_button.pack(pady=10)
search_frame.pack()

# List All Donors Section
list_frame = tk.Frame(app, padx=10, pady=10)
list_button = tk.Button(list_frame, text="List All Donors", command=list_all_donors)
list_button.pack(pady=10)
list_frame.pack()
if __name__=="__main__":
# Initialize database and start app
    setup_database()
    app.mainloop()
