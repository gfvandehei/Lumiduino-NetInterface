import socket
import threading
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 44445))
s.listen(1)

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.sendto(json.dumps({
    "cmd": 0,
    "args": []
}).encode('ascii'),("localhost", 44444))
try:
    while True:
        # Wait for a connection
        print("awaiting con")
        connection, client_address = s.accept()
        try:
            print('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)
                if data:
                    print("Recvd data", data.decode('ascii'))
                else:
                    print("End")
                    break
                
        finally:
            # Clean up the connection
            connection.close()
except KeyboardInterrupt:
    s.close()