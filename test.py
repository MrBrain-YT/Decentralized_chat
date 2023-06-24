import socket
val = "1000"
sock = socket.socket()
sock.connect(('192.168.0.235', 9090))
sock.send(str.encode(val))

data = sock.recv(1024)
sock.close()

print(data)