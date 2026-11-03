import socket
import time
import json
import os
import sys
import ctypes
import winreg
import requests
import tkinter as tk
from tkinter import messagebox

NUME_PC = socket.gethostname()
FISIER_STATUS = "pc_online.json"
DISCORD_WEBHOOK_URL = ""

def cere_permisiune_utilizator(actiune):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    
    raspuns = messagebox.askyesno(
        "Cerere de Permisiune - Monitorizare Agent PC",
        f"Aplicația solicită permisiunea pentru următoarea acțiune:\n\n'{actiune}'\n\nPermiteți executarea acestei acțiuni?"
    )
    root.destroy()
    return raspuns

def adauga_la_startup():
    try:
        python_exe = sys.executable
        script_path = os.path.abspath(__file__)
        pythonw_exe = python_exe.lower().replace("python.exe", "pythonw.exe")
        cmd = f'"{pythonw_exe if os.path.exists(pythonw_exe) else python_exe}" "{script_path}"'
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "AgentPCStatus", 0, winreg.REG_SZ, cmd)
        winreg.CloseKey(key)
    except Exception:
        pass

def obtine_ip_privat():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def obtine_ip_public():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=3)
        return response.json().get("ip", "Indisponibil")
    except Exception:
        return "Indisponibil"

def trimite_notificare_discord(mesaj):
    if not DISCORD_WEBHOOK_URL:
        return
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": mesaj}, timeout=5)
    except Exception:
        pass

def actualizeaza_status():
    ip_privat = obtine_ip_privat()
    ip_public = obtine_ip_public()
    
    trimite_notificare_discord(f"🟢 **PC-ul ONLINE:** Calculatorul **`{NUME_PC}`** a pornit și este activ!")

    while True:
        try:
            date_pc = {}
            if os.path.exists(FISIER_STATUS):
                try:
                    with open(FISIER_STATUS, "r", encoding="utf-8") as f:
                        date_pc = json.load(f)
                except Exception:
                    date_pc = {}

            date_pc[NUME_PC] = {
                "timestamp": time.time(),
                "ip_privat": ip_privat,
                "ip_public": ip_public
            }

            with open(FISIER_STATUS, "w", encoding="utf-8") as f:
                json.dump(date_pc, f, indent=4)

        except Exception:
            pass

        time.sleep(30)

if __name__ == "__main__":
    if cere_permisiune_utilizator("Pornire agent de monitorizare rețea și partajare IP"):
        adauga_la_startup()
        actualizeaza_status()
    else:
        sys.exit()
