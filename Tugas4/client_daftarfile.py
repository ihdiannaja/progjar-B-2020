import socket
import sys
from time import sleep
import base64

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
port = 8888
server_address = ('127.0.0.1', port)
print("Menghubungkan Server: 127.0.0.1" , " Port:", port)
sock.connect(server_address)

try:
    pesan = (b"daftarfile")
    sock.send(pesan)
    data = sock.recv(2048)
    print("Daftar file: \n \n"+data.decode())
finally:
    sock.close()