# Counter - TCP client.  python3 client_tcp.py 10000   (or 10001 through a proxy)
import socket
import struct
import sys
import time
import random

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
commands = [(b'+', 10), (b'+', 5), (b'-', 3), (b'?', 0), (b'*', 2)]
packer = struct.Struct('!ci')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", PORT))
for op, num in commands:
    time.sleep(random.randint(1, 2))
    sock.sendall(packer.pack(op, num))
    answer, value = packer.unpack(sock.recv(packer.size))
    print(f"{op.decode()} {num} -> {answer.decode()} {value}")
sock.close()
