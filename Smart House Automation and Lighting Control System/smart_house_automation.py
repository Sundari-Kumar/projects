import sqlite3
import Tkinter as tk
import tkMessageBox as messagebox
import datetime

# Database setup
def setup_database():
    conn = sqlite3.connect("smart_house.db")
    cursor = conn.cursor()
    
    # Create table for storing light status
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT NOT NULL,
            light_status TEXT NOT NULL,
            timer TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# Turn lights on or off
def control_lights(room_name, status, timer=None):
    conn = sqlite3.connect("smart_house.db")
    cursor = conn.cursor()

    # Check if the light entry exists for the room
    cursor.execute("SELECT * FROM lights WHERE room_name = ?", (room_name,))
    result = cursor.fetchone()

    if result:
        cursor.execute("""
            UPDATE lights
            SET light_status = ?, timer = ?
            WHERE room_name = ?
        """, (status, timer, room_name))
    else:
        cursor.execute("""
            INSERT INTO lights (room_name, light_status, timer)
            VALUES (?, ?, ?)
        """, (room_name, status, timer))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "{} light turned {}!".format(room_name, status))
    show_light_status()

# Show current light statuses
def show_light_status():
    conn = sqlite3.connect("smart_house.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lights")
    lights = cursor.fetchall()
    conn.close()

    light_listbox.delete(0, tk.END)
    if not lights:
        light_listbox.insert(tk.END, "No lights have been set up yet.")
    else:
        for light in lights:
            light_listbox.insert(tk.END, "{} - Status: {} (Timer: {})".format(light[1], light[2], light[3]))

# Clear input fields
def clear_entries():
    room_name_entry.delete(0, tk.END)
    timer_entry.delete(0, tk.END)

# GUI setup
app = tk.Tk()
app.title("Smart House Automation and Lighting Control")

# Frames for Light Control and Viewing Light Status
light_control_frame = tk.Frame(app, padx=10, pady=10)
view_lights_frame = tk.Frame(app, padx=10, pady=10)

# Light Control Section
tk.Label(light_control_frame, text="Control Lights", font=("Arial", 16)).pack(pady=5)

tk.Label(light_control_frame, text="Room Name:").pack(anchor="w")
room_name_entry = tk.Entry(light_control_frame)
room_name_entry.pack(pady=5)

tk.Label(light_control_frame, text="Timer (in minutes, optional):").pack(anchor="w")
timer_entry = tk.Entry(light_control_frame)
timer_entry.pack(pady=5)

turn_on_button = tk.Button(light_control_frame, text="Turn On Light", command=lambda: control_lights(room_name_entry.get(), 'On', timer_entry.get()))
turn_on_button.pack(pady=5)

turn_off_button = tk.Button(light_control_frame, text="Turn Off Light", command=lambda: control_lights(room_name_entry.get(), 'Off', timer_entry.get()))
turn_off_button.pack(pady=5)

# Viewing Light Status Section
tk.Label(view_lights_frame, text="View Light Status", font=("Arial", 16)).pack(pady=5)

light_listbox = tk.Listbox(view_lights_frame, width=50, height=10)
light_listbox.pack(pady=5)

view_lights_button = tk.Button(view_lights_frame, text="View All Lights", command=show_light_status)
view_lights_button.pack(pady=10)

# Switch between frames
def show_light_control_page():
    view_lights_frame.pack_forget()
    light_control_frame.pack()

def show_view_lights_page():
    light_control_frame.pack_forget()
    view_lights_frame.pack()

# Initialize database and start the app
setup_database()
show_light_control_page()  # Start with the light control page
app.mainloop()
