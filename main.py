import socket
from multiprocessing import Process
import Visual
import Server
import urllib.request

myIP = "192.168.0.235"
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

            print('connected:', addr)

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                else:
                    request = "http://127.0.0.1:5000/?Text=" + (data.decode()).replace('\n', '@_@').replace("\'", "")
                    # print(request)
                    urllib.request.urlopen("http://127.0.0.1:5000/?Text=" + (data.decode()).replace('\n', '@_@').replace(" ", "@-@").replace("\r","@^@"))
                    # print(data)
                conn.send(data.upper())

            conn.close()


    def SendMassage(self, value):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.ip, self.port))
            sock.send(str.encode(f"{self.ip}:{self.port}/" + value))
            data = sock.recv(1024)
            sock.close()
            return "success"
        except ConnectionRefusedError or TimeoutError as terr:
            print("errorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
            print(terr)
            # return "error"
        except Exception as err:
            print(f"Exception: {err}")
            # return "error"


if __name__ == '__main__':
    V = Process(target=Visual.ChatVisual)
    G = Process(target=Chat(myIP, myPort).Getmessage)
    S = Process(target=Server.GetMessangeServer)
    S.start()
    V.start()
    G.start()
    while True:
        if not V.is_alive():
            V.terminate()
            G.terminate()
            S.terminate()
            break
    exit()