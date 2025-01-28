import logging
import time
import socket


class Client:
    logger: logging.Logger
    sock: socket.socket

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def start_and_connect(self, srv_port: int, spam: bool):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_address = ("localhost", srv_port)
        try:
            self.sock.connect(srv_address)
            # send data
            if spam:
                for i in range(10):
                    self.sock.sendall(str.encode(f"set {i} {i + 1}"))
            else:
                while True:
                    msg = input("redis-cmd$")
                    self.sock.sendall(str.encode(msg))
                    if msg == 'exit':
                        break
                    if "get" in msg:
                        data = self.sock.recv(128)
                        print(f"{data}")

        finally:
            self.sock.close()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(
                filename="redis.logs",
                filemode="w",
                format="{%(levelname)s:%(message)s}",
                encoding="utf-8",
                level=logging.DEBUG
            )
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_address = ("localhost", 8080)
    sock.connect(srv_address)
    start = time.time()
    for i in range(200000):
        sock.sendall(str.encode(f"set {i} {i + 1}"))
        data = sock.recv(128)
    elapsed = time.time() - start
    print(elapsed)
