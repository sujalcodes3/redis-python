import logging
import socket
from enum import Enum

import store


class CommandType(Enum):
    SET = 1
    GET = 2


class Command:
    typ: CommandType
    args: []
    error: str

    def __init__(self, typ: CommandType, error: str, *arg):
        self.typ = typ
        self.args = []
        self.error = ""
        self.args = arg[0]


class CmdParser:
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def parse_cmd(self, cmd: str) -> Command:
        com, args = cmd.split(' ')[0], cmd.split(' ')[1:]
        typ = None
        error = ""
        match com:
            case "set":
                if len(args) != 2:
                    self.logger.fatal("SET not exactly 2 args")
                    error = "SET not exactly 2 args"
                typ = CommandType.SET
            case "get":
                if len(args) != 1:
                    self.logger.fatal("GET not exactly 1 args")
                    error = "GET not exactly 1 args"
                typ = CommandType.GET

        command = Command(typ, error, args)
        return command


class CmdExecutor:
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def execute(self, client: socket.socket, cmd: Command, db: store.Store):
        if len(cmd.error) > 0:
            client.sendall(cmd.error.decode())
            return

        match cmd.typ:
            case CommandType.SET:
                db.set(cmd.args[0], cmd.args[1])
                msg = f"SET {cmd.args[0]}-{cmd.args[1]}"
                client.sendall(str.encode(msg))

            case CommandType.GET:
                val = db.get(cmd.args[0])
                msg = f"GET {cmd.args[0]}-{val}"
                client.sendall(str.encode(msg))


class CmdHandler:
    cmd: Command

    parser: CmdParser
    executor: CmdExecutor

    def __init__(self, logger: logging.Logger):
        self.parser = CmdParser(logger)
        self.executor = CmdExecutor(logger)

    def parse(self, cmd: str) -> Command:
        self.cmd = self.parser.parse_cmd(cmd)
        return self.cmd

    def execute(self, client: socket.socket, db: store.Store):
        self.executor.execute(client, self.cmd, db)
