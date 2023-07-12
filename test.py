import socket
try:
    val = "1000"
    sock = socket.socket()
    sock.connect(('192.168.0.235', 9090))
    sock.send(str.encode("192.168.0.235:9090/" + "hello"))
    data = sock.recv(1024)
    sock.close()
    print(data)
except ConnectionRefusedError:
    print("LOX")