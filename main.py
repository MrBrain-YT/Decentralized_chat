import socket
from multiprocessing import Process

import Visual

myIP = "192.168.0.103"
myPort = 9090

class Chat():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def Getmessage(self):
        while True:
            server = socket.gethostbyname(socket.gethostname())
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.ip, int(self.port))) 
            sock.listen(10)
            conn, addr = sock.accept()
            message_text:str = ""
            while True:
                data = conn.recv(10000)
                if ("<!>" in data.decode()):
                    message_text += data.decode()
                    break
                elif not data:
                    break
                else:
                    message_text += data.decode()
                
            with open("message.txt", "w") as message:
                message.write(message_text.rstrip("<!>"))
            

            conn.close()


    def SendMassage(self, value):
        state, sock = self.check()
        if state:
            sock.sendall(str.encode(f"{self.ip}:{self.port}/" + value))
            sock.close()
            return True
        else:
            sock.close()
            return False
            
    def check(self, timeout=0.5):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #presumably 
        sock.settimeout(timeout)
        try:
            sock.connect((self.ip, self.port))
        except:
            return False, sock
        else:
            sock.settimeout(None)
            return True, sock


if __name__ == '__main__':
    V = Process(target=Visual.ChatVisual)
    G = Process(target=Chat(myIP, myPort).Getmessage)
    V.start()
    G.start()
    
    while True:
        if not V.is_alive():
            V.terminate()
            G.terminate()
            break
    exit()