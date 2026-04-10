# 🔒 USB Security Shield
### Password Protected External Device Security System

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Security](https://img.shields.io/badge/Security-SHA--256-red?style=for-the-badge&logo=shield&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![USB](https://img.shields.io/badge/USB-Detection-orange?style=for-the-badge&logo=usb&logoColor=white)

> A real-time USB threat detection and access control system for Windows — locks your screen the moment an unauthorized device is plugged in.

---

## ⚠️ IMPORTANT — READ BEFORE YOU RUN

> **Try this project very carefully.**
> Once the system is active, plugging in ANY USB device will trigger a fullscreen lock screen.
> **Do NOT forget your password.** There is no recovery option. If you forget it, you will need to manually edit the source code to reset the hash.
> The default password is: `Secret123`
> Keep it somewhere safe before you change it.

---

## 🎯 What It Does

The moment any USB device is connected to your PC, **USB Security Shield** springs into action:

1. **Detects** the new device instantly via WMI polling
2. **Locks** the screen with a fullscreen authentication overlay
3. **Prompts** for an admin password before allowing any access
4. **Blocks** the user after repeated failed attempts
5. **Resets** automatically when the device is removed

No background service. No installation. One Python file.

---

## 🚨 Why This Matters

External USB devices are one of the most underestimated attack vectors in cybersecurity.
This project was built in direct response to real physical hacking tools:

| Threat | Description |
|--------|-------------|
| **O.MG Cable** | Looks like a USB cable — secretly injects keystrokes and creates backdoors |
| **USB Rubber Ducky** | Disguised as a flash drive — executes pre-programmed attacks in seconds |
| **Weaponized Mouse** | Everyday mouse modified to act as a HID injection device |
| **Weaponized Keyboard** | Looks normal — auto-injects malicious commands on connection |

USB Security Shield intercepts all of these by requiring authentication before any USB device gains system trust.

---

## ✨ Features

- 🖥️  Fullscreen lock overlay — impossible to dismiss without the password
- 🔐  SHA-256 password hashing — credentials never stored in plain text
- 🔁  Real-time WMI monitoring — polls every 2 seconds for new device events
- 🚫  Alt+F4 disabled — no keyboard escape from the lock screen
- ♻️  Auto-reset on device removal — system returns to standby automatically
- 🧵  Non-blocking — monitor runs on a background daemon thread
- 💻  Zero paid dependencies — built entirely with standard Python libraries

---

## 🖼️ System Flow
USB Inserted
│
▼
Device Detected? ──No──► Idle / End
│
Yes
│
▼
Password Prompt Appears (Fullscreen Lock)
│
▼
Password Correct? ──Yes──►  Access Granted
│
No
│
▼
Attempts < 4? ──Yes──► Retry
│
No
│
▼
🚫 User Blocked

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| GUI / Lock Screen | tkinter |
| USB Detection | pywinusb, win32com (WMI) |
| Password Security | hashlib (SHA-256) |
| System Monitoring | psutil, winreg |
| Threading | Python threading |

---

## ⚙️ Installation

### Prerequisites
- Windows 10 / 11
- Python 3.8+

### 1. Clone the repository
git clone https://github.com/your-username/usb-security-shield.git
cd usb-security-shield

### 2. Install dependencies
pip install pywinusb psutil pywin32

### 3. Run as Administrator
python usb_security.py

> ⚠️ Run as Administrator for full WMI device detection access.

---

## 🔑 Changing the Password

The default password is: Secret123

Step 1 — Open a Python shell and run:

import hashlib
print(hashlib.sha256("YourNewPassword".encode()).hexdigest())

Step 2 — Copy the output and replace the hash in usb_security.py:

STORED_PASSWORD_HASH = "paste_your_new_hash_here"

> ⚠️ Once changed, the old password will NOT work. Write down your new password immediately.

---

## 🧠 How It Works

### Detection Engine
The monitor thread queries WMI every 2 seconds:
wmi.ExecQuery("SELECT * FROM Win32_PnPEntity WHERE DeviceID LIKE '%USB%'")
This captures ALL USB-connected entities — storage, HID, MTP, and more.

### Delta Detection
On each poll, the current device set is compared to the previous snapshot.
Any new Device ID triggers the lock immediately:
new_devices = current_devices - last_device_list

### Lock Screen
A fullscreen tkinter window spawns with:
- -topmost flag (always on top of every window)
- WM_DELETE_WINDOW overridden (Alt+F4 completely disabled)
- Return key bound directly to password verification

### Authentication
The entered password is hashed with SHA-256 and compared to the stored hash.
The plain-text password is never stored or logged anywhere.

---

## 📁 Project Structure

usb-security-shield/
│
├── usb_security.py        # Main application (single file)
├── README.md              # You are here
└── docs/
    └── project_report.pdf # Full system documentation

---

## 🔮 Future Scope

- [ ] Email / SMS alert on unauthorized access attempt
- [ ] Logging of detected device IDs with timestamps
- [ ] Whitelist trusted device IDs (skip prompt for known devices)
- [ ] Biometric authentication support
- [ ] Linux and macOS compatibility
- [ ] GUI settings panel for easier configuration
- [ ] System tray icon with live status indicator
- [ ] AI-powered anomaly detection for unknown device types

---

## ⚠️ Disclaimer

This tool is developed for educational and personal security purposes only.
It is intended to protect your own devices.
Do not deploy on systems you do not own or have explicit permission to secure.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👨‍💻 Author

Built with 🔒 and Python.
Feel free to open issues or submit PRs for improvements!

---

"Security is not a product, but a process." — Bruce Schneier
