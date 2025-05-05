import snap7
from snap7.util import set_bool, get_bool
import tkinter as tk

# PLC Configuration
PLC_IP = '192.168.1.20'  # ⚠️ Replace with your PLC IP
DB_NUMBER = 1
BYTE_INDEX = 0
BIT_INDEX = 0

# Initialize PLC client
plc = snap7.client.Client()

def connect_to_plc():
    try:
        plc.connect(PLC_IP, 0, 1)
        if plc.get_connected():
            status_label.config(text="✅ Connected to PLC", fg="green")
        else:
            status_label.config(text="❌ Failed to connect", fg="red")
    except Exception as e:
        status_label.config(text=f"❌ {e}", fg="red")

def toggle_bit():
    try:
        # Read 1 byte from DB
        data = plc.db_read(DB_NUMBER, BYTE_INDEX, 1)

        # Get current bit value
        current = get_bool(data, 0, BIT_INDEX)

        # Toggle value
        new_value = not current
        set_bool(data, 0, BIT_INDEX, new_value)

        # Write updated byte
        plc.db_write(DB_NUMBER, BYTE_INDEX, data)

        # Update UI
        bit_status.set("ON" if new_value else "OFF")
        toggle_button.config(bg="green" if new_value else "red")
    except Exception as e:
        status_label.config(text=f"❌ {e}", fg="red")

# Create UI
root = tk.Tk()
root.title("DB1.DBX0.0 Bit Toggle")

status_label = tk.Label(root, text="Connecting...", font=("Arial", 12))
status_label.pack(pady=10)

bit_status = tk.StringVar()
bit_status.set("OFF")

toggle_button = tk.Button(
    root, textvariable=bit_status, font=("Arial", 16),
    width=10, bg="red", fg="white", command=toggle_bit
)
toggle_button.pack(pady=20)

# Connect to PLC after UI loads
root.after(500, connect_to_plc)

root.mainloop()