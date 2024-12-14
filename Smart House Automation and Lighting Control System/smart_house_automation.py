import sqlite3
import Tkinter as tk
import tkMessageBox as messagebox
import datetime
import time
import threading

# Database setup
def setup_database():
    conn = sqlite3.connect("smart_house.db")
    cursor = conn.cursor()

    # Check if the 'lights' table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT NOT NULL,
            light_status TEXT NOT NULL,
            timer TEXT,
            scheduled_time TEXT  -- Adding the new column here
        )
    """)
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()


# Turn lights on or off
def control_lights(room_name, status, timer=None, scheduled_time=None):
    conn = sqlite3.connect("smart_house.db")
    cursor = conn.cursor()

    # Check if the light entry exists for the room
    cursor.execute("SELECT * FROM lights WHERE room_name = ?", (room_name,))
    result = cursor.fetchone()

    if result:
        cursor.execute("""
            UPDATE lights
            SET light_status = ?, timer = ?, scheduled_time = ?
            WHERE room_name = ?
        """, (status, timer, scheduled_time, room_name))
    else:
        cursor.execute("""
            INSERT INTO lights (room_name, light_status, timer, scheduled_time)
            VALUES (?, ?, ?, ?)
        """, (room_name, status, timer, scheduled_time))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "{} light turned {}!".format(room_name, status))
    show_light_status()

# Schedule lights to turn on or off at a specific time
def schedule_light(room_name, status, scheduled_time):
    conn = sqlite3.connect("smart_house.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE lights
        SET light_status = ?, scheduled_time = ?
        WHERE room_name = ?
    """, (status, scheduled_time, room_name))

    conn.commit()
    conn.close()

    messagebox.showinfo("Scheduled", "Light for {} is scheduled to turn {} at {}".format(room_name, status, scheduled_time))
    show_light_status()

# Timer countdown logic
def start_timer(room_name, timer):
    try:
        timer = int(timer)
    except ValueError:
        messagebox.showerror("Invalid Timer", "Timer must be a valid number!")
        return

    if timer > 0:
        for i in range(timer, 0, -1):
            time.sleep(60)  # Wait for 1 minute
            print("Timer for {}: {} minutes remaining".format(room_name, i))

        control_lights(room_name, 'Off', timer=None)  # Automatically turn off the light after the timer ends
    else:
        messagebox.showerror("Invalid Timer", "Timer must be greater than 0!")

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

# Delete light entry
def delete_light(room_name):
    conn = sqlite3.connect("smart_house.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM lights WHERE room_name = ?", (room_name,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Deleted", "{} light entry has been removed.".format(room_name))
    show_light_status()

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

# Scheduling light control
tk.Label(light_control_frame, text="Schedule Light Control (Turn On/Off at Specific Time)").pack(pady=10)
scheduled_time_entry = tk.Entry(light_control_frame)
scheduled_time_entry.pack(pady=5)

schedule_on_button = tk.Button(light_control_frame, text="Schedule On", command=lambda: schedule_light(room_name_entry.get(), 'On', scheduled_time_entry.get()))
schedule_on_button.pack(pady=5)

schedule_off_button = tk.Button(light_control_frame, text="Schedule Off", command=lambda: schedule_light(room_name_entry.get(), 'Off', scheduled_time_entry.get()))
schedule_off_button.pack(pady=5)

# Delete light entry
delete_button = tk.Button(view_lights_frame, text="Delete Light Entry", command=lambda: delete_light(room_name_entry.get()))
delete_button.pack(pady=5)

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

# Navigation buttons (to switch between pages)
nav_frame = tk.Frame(app)
nav_frame.pack(pady=20)

control_button = tk.Button(nav_frame, text="Control Lights", command=show_light_control_page)
control_button.pack(side='left', padx=10)

view_button = tk.Button(nav_frame, text="View Light Status", command=show_view_lights_page)
view_button.pack(side='left', padx=10)

app.mainloop()
