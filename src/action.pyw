import time
import socket

def tcp_ping(host="kali-host.akirottv.de", port=6969, timeout=3):
    socket.setdefaulttimeout(timeout)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    count = 1
    for i in range(count + 1): 
        try:   
            s.connect((host, port))
            s.close()
            time.sleep(5)
            i = i + 1
        except Exception as e:
            print(e)
            return False
    return True

tcp_ping()