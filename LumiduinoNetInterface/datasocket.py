"""
Author: Gabriel Vande Hei
The datasocket is a datastructure to manage a data streaming connection to the server
Manages the messaging protocol, closing/opening, and heartbeat
"""
from enum import IntEnum, auto
import socket
from threading import Thread

class DataSocket(object):
    
    def __init__(self):
        # ===== control objects
        self.connected = False
        # ===== socket stuff
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        self.remote_addr = None
        # ===== data structures
        self.sub_queues = []

    def init_connection(self, ip: str, port: int):
        try:
            self.socket.connect((ip, port))
            self.connected = True
            self.remote_addr = (ip, port)
            Thread(target=self._receive_thread).start()
            return True
        except:
            return False

    def handle_message(self, message: str):
        #TODO: Implement handle_message
        pass
    
    def _receive_thread(self):
        stream_buffer = ""
        while self.connected:
            try:
                data = self.socket.recv(1024).decode('ascii')
                # check if there was a disconnect
                if data == "":
                    # there was a disconnect
                    self.connected = False
                    self.remote_addr = None
                    print("Data connection was terminated")
                    return
                # messages should be delimited by |
                for i in data:
                    if i == "|":
                        # Handle full message
                        self.handle_message(stream_buffer)
                    else:
                        stream_buffer += i
            except Exception as err:
                print(err)
                continue

class ConnectProtocol(IntEnum):
    HEARTBEAT = 0
    COMMAND = 1
    DATA = 2
    ERROR = 3
