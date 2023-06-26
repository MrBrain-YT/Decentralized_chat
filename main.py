import socket
from multiprocessing import Process
import Visual
import Server
import urllib.request



class Chat():
    def Getmessage():
        while True:
            server = socket.gethostbyname(socket.gethostname())
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('192.168.0.103', 9090)) 
            sock.listen(1)
            conn, addr = sock.accept()

            print('connected:', addr)

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                else:
                    request = "http://127.0.0.1:5000/?Text=" + (data.decode()).replace('\n', '@_@').replace("\'", "")
                    print(request)
                    urllib.request.urlopen("http://127.0.0.1:5000/?Text=" + (data.decode()).replace('\n', '@_@').replace(" ", "@-@"))
                    print(data)
                conn.send(data.upper())

            conn.close()


    def SendMassage(value):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('192.168.0.103', 9090))
        sock.send(str.encode(value))
        data = sock.recv(1024)
        sock.close()
        # print(data)


if __name__ == '__main__':
    V = Process(target=Visual.ChatVisual)
    G = Process(target=Chat.Getmessage)
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
