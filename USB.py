import tkinter as tk
from tkinter import messagebox
import psutil
import pywinusb.hid as hid
import threading
import time
import win32com.client
from win32com.client import Dispatch
import winreg
import hashlib

# --- SECURITY CONFIGURATION ---
# This is a SHA-256 hash of the word "Secret123"
# To change it, generate a new hash and paste it here.
STORED_PASSWORD_HASH = "ef2339adcb9348e3f57bc816007e0ee90633b65b63d767f701f160c9da191c78" 

INTERNAL_VENDORS = ["SYNAPTICS", "ELAN", "LENOVO", "HP", "DELL", "MICROSOFT", "INTEL"]

# --- Global Variables ---
root = None
device_connected = False
password_verified = False
last_device_list = set()
initial_scan = True

def hash_password(password):
    """Encodes the password to SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

# --- GUI Password Screen ---
def show_password_screen():
    global root
    try:
        if root and root.winfo_exists():
            return 
    except tk.TclError:
        root = None

    root = tk.Tk()
    root.title("🔒 USB Security Shield")
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    # Disable Alt+F4
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    frame = tk.Frame(root, bg="#1a1a1a")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🔒 UNAUTHORIZED DEVICE", font=("Consolas", 32, "bold"), fg="#ff4444", bg="#1a1a1a").pack(pady=50)
    tk.Label(frame, text="System locked due to external connection. Enter Admin Password:", 
             font=("Consolas", 14), fg="white", bg="#1a1a1a").pack(pady=10)

    password_entry = tk.Entry(frame, show="*", font=("Arial", 20), width=25, justify='center')
    password_entry.pack(pady=20)
    password_entry.focus()

    # Enter key triggers unlock
    root.bind('<Return>', lambda event: check_password(password_entry))

    tk.Button(frame, text="UNLOCK SYSTEM", command=lambda: check_password(password_entry),
              font=("Consolas", 14, "bold"), bg="#44ff44", width=20, height=2).pack(pady=20)

    root.mainloop()

def check_password(entry):
    global password_verified, root
    input_hash = hash_password(entry.get())
    
    if input_hash == STORED_PASSWORD_HASH:
        password_verified = True
        root.destroy()
        print("[SUCCESS] Access Granted.")
    else:
        messagebox.showerror("Access Denied", "Invalid Security Token")
        entry.delete(0, tk.END)

# --- Logic for GitHub: How the Detection Loop Works ---
# 

def get_all_usb_devices():
    devices = set()
    try:
        wmi = win32com.client.GetObject("winmgmts:")
        # Check PnP Entities (Covers Storage, MTP, and HID)
        usb_with_drivers = wmi.ExecQuery("SELECT * FROM Win32_PnPEntity WHERE DeviceID LIKE '%USB%'")
        for device in usb_with_drivers:
            devices.add(device.DeviceID)
    except Exception as e:
        print(f"Detection error: {e}")
    return devices

def monitor_devices():
    global device_connected, password_verified, last_device_list, initial_scan
    
    last_device_list = get_all_usb_devices()
    time.sleep(2)
    initial_scan = False
    print("[SYSTEM] Monitoring Active...")

    while True:
        current_devices = get_all_usb_devices()
        new_devices = current_devices - last_device_list
        
        # If new device found and we aren't already locked
        if len(new_devices) > 0 and not password_verified:
            print(f"[ALERT] New Device: {new_devices}")
            device_connected = True
            show_password_screen()

        # Reset state if all external devices are removed
        if len(current_devices) <= len(last_device_list) and not new_devices:
            password_verified = False
            device_connected = False

        time.sleep(2)

if __name__ == "__main__":
    threading.Thread(target=monitor_devices, daemon=True).start()
    # Keep main thread alive
    while True:
        time.sleep(1)