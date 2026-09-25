import os
import json
import time
import platform
import subprocess
import hashlib
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
TOKEN_FILE = CONFIG_DIR / "device_token.json"

# Ek secret salt jise sirf aap jante hain (Code ko obfuscate/compile karte waqt yeh safe rahega)
SECRET_SALT = "JARVIS_ULTIMATE_SECRET_2026"

def get_machine_id():
    """Get a unique hardware fingerprint of the user's PC."""
    try:
        if platform.system() == "Windows":
            # Windows Registry se permanent Machine GUID nikalna
            cmd = 'reg query "HKLM\\SOFTWARE\\Microsoft\\Cryptography" /v MachineGuid'
            res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            for line in res.stdout.splitlines():
                if "MachineGuid" in line:
                    return line.split()[-1].strip()
        # Fallback for other systems
        return platform.node() + platform.machine()
    except Exception:
        return "DEFAULT_MACHINE_ID"

def generate_key_for_machine(machine_id: str) -> str:
    """Aap is formula ka use karke apne PC par user ke liye key generate karenge."""
    raw = f"{machine_id}_{SECRET_SALT}"
    hasher = hashlib.sha256(raw.encode("utf-8"))
    # 12 characters ki ek secure uppercase key ban jayegi
    return hasher.hexdigest().upper()[:12]

def verify_device_access():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    if TOKEN_FILE.exists():
        try:
            data = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
            if data.get("authenticated"):
                return True
        except Exception:
            pass

    return show_key_prompt()

def show_key_prompt():
    root = tk.Tk()
    root.title("JARVIS Hardware Authentication")
    root.geometry("400x260")
    root.configure(bg="#07090f")
    root.resizable(False, False)

    machine_id = get_machine_id()
    auth_status = {"success": False}

    lbl_title = tk.Label(root, text="ACTIVATION REQUIRED", fg="#6366f1", bg="#07090f", font=("Arial", 11, "bold"))
    lbl_title.pack(pady=10)

    # User ko uska Machine ID dikhega taaki woh aapko bhej sake
    lbl_info = tk.Label(root, text=f"Your Machine ID:\n{machine_id}", fg="#8899aa", bg="#07090f", font=("Courier", 9))
    lbl_info.pack(pady=5)

    entry = tk.Entry(root, font=("Arial", 12), justify="center")
    entry.pack(pady=10, ipadx=10, ipady=5, fill="x", padx=30)
    entry.focus()

    def submit():
        user_key = entry.get().strip().upper()
        expected_key = generate_key_for_machine(machine_id)

        if user_key == expected_key:
            try:
                TOKEN_FILE.write_text(json.dumps({"authenticated": True, "machine_id": machine_id}), encoding="utf-8")
            except Exception:
                pass
            auth_status["success"] = True
            root.destroy()
        else:
            messagebox.showerror("Access Denied", "Invalid key for this computer!")

    btn = tk.Button(root, text="ACTIVATE", bg="#6366f1", fg="white", font=("Arial", 10, "bold"), command=submit)
    btn.pack(pady=10, ipadx=20, ipady=5)

    root.mainloop()
    return auth_status["success"]
