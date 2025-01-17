import logging
import time
import json
import os
import socket
import threading

import commands
import store


class Server:
    port: int
    cmd_handler: commands.CmdHandler

    db: store.Store

    logger: logging.Logger
    sock: socket.socket
    threads: []
    client_connected_with_threads = {}
    dmp_file: str

    def __init__(self, port: int, logger: logging.Logger, dmp_file: str = "data.json"):
        self.port = port
        self.logger = logger
        self.cmd_handler = commands.CmdHandler(self.logger)
        self.db = store.Store(logger)
        self.threads = []
        self.client_connected_with_threads = {}
        self.dmp_file = "data.json"
        if os.path.exists(self.dmp_file):
            with open(self.dmp_file, "r") as file:
                if os.path.getsize(self.dmp_file) != 0:
                    self.db.store = json.load(file)
        else:
            with open(self.dmp_file, "w") as file:
                self.logger.info("dump file created")

    def _bind(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = ("localhost", self.port)
        self.sock.bind(addr)
        self.logger.info(f"binding server on {addr}")

    def _handle_client(
                self,
                client: socket.socket,
                client_addr,
            ):
        while True:
            data = client.recv(1024)
            if data:
                self.logger.info(
                            f"recievedfrom:{client_addr} msg:{data.decode()}"
                        )
                self._handle_cmd(client, data.decode())
                if data == b'exit':
                    self.logger.info(f"exit signal from {client_addr}")
                    break

        client.close()
        self.logger.info(f"client closed [{client} {client_addr}]")

    def _dmp_data(self):
        time.sleep(2)
        self.db.sync(self.dmp_file)

    def start_and_listen(self):
        self._bind()
        dmp_thread = threading.Thread(target=self._dmp_data)
        self.threads.append(dmp_thread)
        dmp_thread.start()
        self.sock.listen(100)
        print(f"server listening on port:{self.port}")
        try:
            while True:
                client, client_addr = self.sock.accept()
                client_thread = threading.Thread(
                        target=self._handle_client, args=(
                                client,
                                client_addr,
                            )
                        )
                self.threads.append(client_thread)
                client_thread.start()

                self.logger.info(f"client connected [{client_addr}]")

        except KeyboardInterrupt:
            if self.sock:
                self.sock.close()
            for t in self.threads:
                t.join()

    def _handle_cmd(self, client: socket.socket, cmd: str):
        _ = self.cmd_handler.parse(cmd)
        self.cmd_handler.execute(client, self.db)
