import socket
import sys
import base64
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 8888
server_address = ('127.0.0.1', port)
print("Menghubungkan Server: 127.0.0.1" , " Port:", port)
sock.connect(server_address)

try:
    filename = "progjar_download.py"
    pesan = "ambilfile "+filename
    sock.send(pesan.encode())

    data = sock.recv(10000)
    file = open(filename,"wb")
    file.write(data)
    file.close()
    
    print("File berhasil diambil")
finally:
    print("Close")
    sock.close()