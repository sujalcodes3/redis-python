import socket
import time

# commands = [
#     "set key value",
#     "get key1",
#     "set dev mal",
#     "get dev",
#     "set fdg oij",
#     "get fdg",
#     "set owieu sdj",
#     "get owieu",
#     "set qpzm zmqp",
#     "get qpzm",
#     "set eixn imxe",
#     "get eixn",
#     "set vbfh hfbv",
#     "get vbfh",
#     "set uiop poiu",
#     "get uiop",
#     "set bnm mnb",
#     "get bnm",
#     "set fal laf",
#     "get fal",
# ]

commands = [
    "set key1 value1\r\n",
    "get key1\r\n",
    "set key2 value2\r\n",
    "get key2\r\n",
    "set key3 value3\r\n",
    "get key3\r\n",
    "set key4 value4\r\n",
    "get key4\r\n",
    "set key5 value5\r\n",
    "get key5\r\n",
    "set key6 value6\r\n",
    "get key6\r\n",
    "set key7 value7\r\n",
    "get key7\r\n",
    "set key8 value8\r\n",
    "get key8\r\n",
    "set key9 value9\r\n",
    "get key9\r\n",
    "set key10 value10\r\n",
    "get key10\r\n",
]


def benchmark(host, port, commands, n=10000):
    start_time = time.time()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        for _ in range(n):
            for command in commands:
                client.sendall(command.encode())
                client.recv(1024)
                # Uncomment to see responses:
                # print(response.decode())
    elapsed_time = time.time() - start_time
    print(f"{n} requests completed in {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    # commands = ["set key value\r\n", "get key\r\n"]
    benchmark("127.0.0.1", 8080, commands)
