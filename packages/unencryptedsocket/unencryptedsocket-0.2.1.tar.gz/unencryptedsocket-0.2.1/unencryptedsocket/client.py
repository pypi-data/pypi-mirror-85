import socket
import pickle
import json
from omnitools import args
from .utils import *


__ALL__ = ["SC"]


class SC(object):
    def __init__(self, host: str = "127.199.71.10", port: int = 39291) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, int(port)))

    def request(self, command: str, data = None):
        request = dict(command=command, data=data)
        try:
            request = json.dumps(request).encode()
        except:
            request = pickle.dumps(request)
        self.s.send(request)
        len_response = self.s.recv(4)
        if not len_response:
            return None
        import struct
        len_response = struct.unpack('>I', len_response)[0]
        recv = b""
        while len(recv) < len_response:
            recv += self.s.recv(len_response-len(recv))
            if not recv:
                break
        try:
            return json.loads(recv.decode())
        except UnicodeDecodeError:
            return pickle.loads(recv)

