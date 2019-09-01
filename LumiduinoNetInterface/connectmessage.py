import json
from enum import IntEnum, auto

class ConnectMessage(object):

    def __init__(self, message):
        try:
            entire_json = json.loads(message)
            self.command = ConnectProtocol(entire_json['cmd'])
        except Exception as err:
            print(err)
            raise Exception('''Received connection messages should be in a json format
            , and must include a command key''')


class ConnectProtocol(IntEnum):
    CONNECT = 0
    ACK = 1
    ERROR = 2