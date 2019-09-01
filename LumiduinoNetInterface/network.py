import socket
from queue import Queue, Empty
import json
from LumiduinoNetInterface.connectmessage import ConnectMessage, ConnectProtocol
from LumiduinoNetInterface.datasocket import DataSocket
from threading import Thread

class NetworkConnection(object):
    
    def __init__(self):
        # ====== class control objects
        self.exit_flag = False
        self.server_connected = False
        # ====== connect_udp socket objects
        self.connect_request_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connect_request_socket.bind(("", 44444))
        self.connect_request_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
        self.connect_request_socket.settimeout(2)
        self.connect_queue = Queue()
        # ====== tcp data connection object
        self.data_socket = DataSocket()
        self.recv_queue = Queue()

        # ====== threads
        Thread(target=self._receive_connect_thread).start()
        Thread(target=self._handle_connect_queue).start()

        print("Listening on 44444 for connection requests")
    
    def _receive_connect_thread(self):
        while not self.exit_flag:
            try:
                data, addr = self.connect_request_socket.recvfrom(1024) #buffer size is 1024 bytes
                print("Received message on c_sock from", addr)
            except socket.timeout:
                continue

            try:
                connect_cmd = ConnectMessage(data)
                self.connect_queue.put((addr, connect_cmd))
            except Exception as err:
                self.connect_request_socket.sendto(json.dumps({
                    "cmd": ConnectProtocol.ERROR.value,
                    "args": err
                }), addr)

    def _handle_connect_queue(self):
        while not self.exit_flag:
            try:
                addr, message = self.connect_queue.get(timeout=2)
                if message.command == ConnectProtocol.CONNECT and not self.server_connected:
                    # connect the tcp socket to the server
                    (ip, port) = addr
                    try:
                        self.data_socket.init_connection(ip, 44445)
                        self.server_connected = True
                    except:
                        pass

                    # respond with an ack if it worked, or an error if not
                    self.connect_request_socket.sendto(json.dumps({
                        "cmd": ConnectProtocol.ACK,
                        "args": []
                    }).encode('ascii'), addr)
                    print("Connect Request received")
            except Empty:
                continue
