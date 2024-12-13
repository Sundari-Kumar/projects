import sqlite3
import Tkinter as tk
import tkMessageBox as messagebox

# Database setup
def setup_database():
    conn = sqlite3.connect("food_delivery.db")
    cursor = conn.cursor()

    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            food_item TEXT NOT NULL,
            customizations TEXT,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add order to database
def add_order():
    customer_name = name_entry.get()
    food_item = food_item_entry.get()
    customizations = customizations_entry.get()
    status = "Pending"  # Default status is 'Pending'

    if not customer_name or not food_item:
        messagebox.showerror("Error", "Customer Name and Food Item are required!")
        return

    conn = sqlite3.connect("food_delivery.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO orders (customer_name, food_item, customizations, status)
        VALUES (?, ?, ?, ?)
    """, (customer_name, food_item, customizations, status))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Order placed successfully!")
    clear_entries()
    show_orders()

# Show all orders
def show_orders():
    conn = sqlite3.connect("food_delivery.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()

    order_listbox.delete(0, tk.END)
    if not orders:
        order_listbox.insert(tk.END, "No orders placed yet.")
    else:
        for order in orders:
            order_listbox.insert(tk.END, "{} - {}: {} (Customizations: {}) - Status: {}".format(
                order[1], order[2], order[3], order[4], order[5]))

# Clear input fields
def clear_entries():
    name_entry.delete(0, tk.END)
    food_item_entry.delete(0, tk.END)
    customizations_entry.delete(0, tk.END)

# Update order status (e.g., mark as delivered)
def update_order_status():
    try:
        selected_order = order_listbox.curselection()
        if not selected_order:
            raise ValueError("No order selected!")

        order_id = order_listbox.get(selected_order[0]).split(" - ")[0]
        status = status_entry.get()

        if not status:
            messagebox.showerror("Error", "Status cannot be empty!")
            return

        conn = sqlite3.connect("food_delivery.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE orders SET status = ? WHERE id = ?
        """, (status, order_id))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Order status updated successfully!")
        show_orders()
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# GUI setup
app = tk.Tk()
app.title("Food Delivery Order System")

# Frames for Add Order and View Orders
add_order_frame = tk.Frame(app, padx=10, pady=10)
view_orders_frame = tk.Frame(app, padx=10, pady=10)

# Add Order Section
tk.Label(add_order_frame, text="Place a Food Order", font=("Arial", 16)).pack(pady=5)

tk.Label(add_order_frame, text="Customer Name:").pack(anchor="w")
name_entry = tk.Entry(add_order_frame)
name_entry.pack(pady=5)

tk.Label(add_order_frame, text="Food Item:").pack(anchor="w")
food_item_entry = tk.Entry(add_order_frame)
food_item_entry.pack(pady=5)

tk.Label(add_order_frame, text="Customizations (optional):").pack(anchor="w")
customizations_entry = tk.Entry(add_order_frame)
customizations_entry.pack(pady=5)

add_order_button = tk.Button(add_order_frame, text="Place Order", command=add_order)
add_order_button.pack(pady=10)

# View Orders Section
tk.Label(view_orders_frame, text="View Orders", font=("Arial", 16)).pack(pady=5)

order_listbox = tk.Listbox(view_orders_frame, width=60, height=10)
order_listbox.pack(pady=5)

view_orders_button = tk.Button(view_orders_frame, text="View All Orders", command=show_orders)
view_orders_button.pack(pady=10)

# Update Order Status Section
tk.Label(view_orders_frame, text="Update Order Status").pack(pady=5)
tk.Label(view_orders_frame, text="Enter Status (e.g., Delivered)").pack(anchor="w")
status_entry = tk.Entry(view_orders_frame)
status_entry.pack(pady=5)

update_status_button = tk.Button(view_orders_frame, text="Update Status", command=update_order_status)
update_status_button.pack(pady=10)

# Switch between frames
def show_add_order_page():
    view_orders_frame.pack_forget()
    add_order_frame.pack()

def show_view_orders_page():
    add_order_frame.pack_forget()
    view_orders_frame.pack()

# Initialize database and start the app
setup_database()
show_add_order_page()  # Start with the add order page
app.mainloop()
