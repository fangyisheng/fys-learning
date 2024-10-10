import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('106.15.121.114', 2000))
if result == 0:
    print("Port is open")
else:
    print("Port is closed")
sock.close()