import sys
import socket
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 31001)
print(f"starting up on {server_address}")
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)
while True:
    # Wait for a connection
    print("waiting for a connection")
    connection, client_address = sock.accept()
    print(f"connection from {client_address}")
    # Receive the data in small chunks and retransmit it
    fl = open("isifile.txt", 'rb')
    isi = fl.read(64)
    message = str(isi)
    # print(f"received {data}")
    print(f"sending {message}")

    connection.sendall(message.encode())

    # Clean up the connection
    connection.close()