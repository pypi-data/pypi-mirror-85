import json
import socket
import pickle
import threading
import traceback
from omnitools import encryptedsocket_function


__ALL__ = ["SS"]


class SS(object):
    def __init__(self, functions: encryptedsocket_function = None,
                 host: str = "127.199.71.10", port: int = 39291) -> None:
        self.terminate = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, int(port)))
        self.s.listen(5)
        self.__key = {}
        self.functions = functions or {}

    def handler(self, conn: socket.socket, addr: tuple) -> None:
        uid = addr[0]+":"+str(addr[1])
        print("connected\t{uid}".format(uid=uid))
        try:
            while True:
                # request = conn.recv(1024*4).decode()
                len_response = conn.recv(4)
                if not len_response:
                    return None
                import struct
                len_response = struct.unpack('>I', len_response)[0]
                recv = b""
                while len(recv) < len_response:
                    recv += conn.recv(len_response - len(recv))
                    if not recv:
                        break
                request = recv
                if not request:
                    break
                response = {}
                request = json.loads(request)
                if request["command"] in self.functions:
                    try:
                        response = self.functions[request["command"]](*request["data"][0], **request["data"][1])
                    except:
                        response = traceback.format_exc()
                try:
                    response = json.dumps(response).encode()
                except TypeError:
                    response = pickle.dumps(response)
                import struct
                conn.sendall(struct.pack('>I', len(response))+response)
        except Exception as e:
            print(e)
        finally:
            conn.close()
            print("disconnected\t{uid}".format(uid=uid))

    def start(self) -> None:
        try:
            while not self.terminate:
                conn, addr = self.s.accept()
                threading.Thread(target=self.handler, args=(conn, addr)).start()
        except Exception as e:
            if not self.terminate:
                raise e

    def stop(self) -> bool:
        self.terminate = True
        self.s.close()
        return True

