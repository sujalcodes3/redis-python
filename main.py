import argparse
import logging

import client
import server

parser = argparse.ArgumentParser(prog="redis application")
parser.add_argument('-t', '--type')
args = parser.parse_args()

logger = logging.getLogger(__name__)
logging.basicConfig(
        filename="redis.logs",
        filemode="w",
        format="{%(levelname)s:%(message)s}",
        encoding="utf-8",
        level=logging.DEBUG)

match args.type:
    case "server":
        srv = server.Server(8081, logger)
        srv.start_and_listen()

    case "client":
        cln = client.Client(logger)
        cln.start_and_connect(8081, False)
