import sqlite3
import tkMessageBox as messagebox
import Tkinter as tk

# Database setup
def setup_database():
    conn = sqlite3.connect("real_estate.db")
    cursor = conn.cursor()
    # Properties table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL,
            price INTEGER NOT NULL,
            owner TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add a new property
def add_property():
    address = reg_address_entry.get()
    price = reg_price_entry.get()
    owner = reg_owner_entry.get()

    if not address or not price or not owner:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        price = int(price)
    except ValueError:
        messagebox.showerror("Error", "Price must be a valid number!")
        return

    conn = sqlite3.connect("real_estate.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO properties (address, price, owner) VALUES (?, ?, ?)", (address, price, owner))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Property added successfully!")
    reg_address_entry.delete(0, tk.END)
    reg_price_entry.delete(0, tk.END)
    reg_owner_entry.delete(0, tk.END)

# Search for a property
def search_property():
    search_address = search_address_entry.get()

    if not search_address:
        messagebox.showerror("Error", "Address is required to search!")
        return

    conn = sqlite3.connect("real_estate.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM properties WHERE address LIKE ?", ('%' + search_address + '%',))
    results = cursor.fetchall()
    conn.close()

    if results:
        result_message = "\n".join(["Address: {}, Price: {}, Owner: {}".format(row[1], row[2], row[3]) for row in results])
        messagebox.showinfo("Search Results", result_message)
    else:
        messagebox.showerror("No Results", "No properties found matching that address.")

# List all properties
def list_all_properties():
    conn = sqlite3.connect("real_estate.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM properties")
    results = cursor.fetchall()
    conn.close()

    if results:
        result_message = "\n".join(["Address: {}, Price: {}, Owner: {}".format(row[1], row[2], row[3]) for row in results])
        messagebox.showinfo("All Properties", result_message)
    else:
        messagebox.showinfo("No Properties", "No properties available in the system.")

# GUI setup
app = tk.Tk()
app.title("Real Estate Management System")

# Frames for Add Property and Search Property
add_property_frame = tk.Frame(app, padx=10, pady=10)
search_property_frame = tk.Frame(app, padx=10, pady=10)
list_property_frame = tk.Frame(app, padx=10, pady=10)

# Add Property Section
tk.Label(add_property_frame, text="Add Property", font=("Arial", 16)).pack(pady=5)
tk.Label(add_property_frame, text="Address:").pack(anchor="w")
reg_address_entry = tk.Entry(add_property_frame)
reg_address_entry.pack(pady=5)

tk.Label(add_property_frame, text="Price:").pack(anchor="w")
reg_price_entry = tk.Entry(add_property_frame)
reg_price_entry.pack(pady=5)

tk.Label(add_property_frame, text="Owner:").pack(anchor="w")
reg_owner_entry = tk.Entry(add_property_frame)
reg_owner_entry.pack(pady=5)

add_button = tk.Button(add_property_frame, text="Add Property", command=add_property)
add_button.pack(pady=10)

# Search Property Section
tk.Label(search_property_frame, text="Search Property by Address", font=("Arial", 16)).pack(pady=5)
tk.Label(search_property_frame, text="Address:").pack(anchor="w")
search_address_entry = tk.Entry(search_property_frame)
search_address_entry.pack(pady=5)

search_button = tk.Button(search_property_frame, text="Search", command=search_property)
search_button.pack(pady=10)

# List All Properties Section
tk.Label(list_property_frame, text="List All Properties", font=("Arial", 16)).pack(pady=5)
list_button = tk.Button(list_property_frame, text="Show All Properties", command=list_all_properties)
list_button.pack(pady=10)

# Switch between frames
def show_add_property_page():
    add_property_frame.pack(fill='both', expand=True)
    search_property_frame.pack_forget()
    list_property_frame.pack_forget()

def show_search_property_page():
    search_property_frame.pack(fill='both', expand=True)
    add_property_frame.pack_forget()
    list_property_frame.pack_forget()

def show_list_property_page():
    list_property_frame.pack(fill='both', expand=True)
    add_property_frame.pack_forget()
    search_property_frame.pack_forget()

# Initialize database and start the app
setup_database()
show_add_property_page()  # Start with the Add Property page

# Navigation Buttons
nav_frame = tk.Frame(app)
nav_frame.pack(pady=20)

add_property_nav_button = tk.Button(nav_frame, text="Add Property", command=show_add_property_page)
add_property_nav_button.pack(side='left', padx=10)

search_property_nav_button = tk.Button(nav_frame, text="Search Property", command=show_search_property_page)
search_property_nav_button.pack(side='left', padx=10)

list_property_nav_button = tk.Button(nav_frame, text="List Properties", command=show_list_property_page)
list_property_nav_button.pack(side='left', padx=10)

app.mainloop()
