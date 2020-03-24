import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 8888
server_address = ('127.0.0.1', port)
print("Menghubungkan server: 127.0.0.1" , " Port:", port)
sock.connect(server_address)

try:
    namafile= "progjar_upload.txt"
    file = open(namafile,"rb")
    konten = file.read(10000)
    file.close()
    konten = konten.decode()
    pesan = "meletakkanfile "+namafile+" "+konten
    sock.send(pesan.encode())

    data = sock.recv(10000).decode()
    print(data)

finally:
    print("Close")
    sock.close()