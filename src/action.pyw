import time
import socket

def tcp_ping(host="kali-host.akirottv.de", port=6969, timeout=3):
    infinity = 1
    for i in range(1 + infinity): 
        try:
            socket.setdefaulttimeout(timeout)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.close()
            time.sleep(5)
            i += 1
            infinity += 1
        except Exception as e:
            print(e)

tcp_ping()