import sys
import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening

server_address = ('localhost', 31001)
print(f"connecting to {server_address}")
sock.connect(server_address)

#try:
    # Send data
#    message = 'makaneak'
#    print(f"sending {message}")
#    sock.sendall(message.encode())
    # Look for the response
#    amount_received = 0
#    amount_expected = len(message)
#    while amount_received < amount_expected:
#        data = sock.recv(64)
#        amount_received += len(data)
#        print(f"{data}")
#finally:
#    print("closing")
#    sock.close()
#data = sock.recv(1024)
#print('data=%s', (data))
with open('received_file.txt', 'wb') as f:
    print ('file opened')
    while True:
        print('receiving data...')
        data = sock.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()



sock.close()