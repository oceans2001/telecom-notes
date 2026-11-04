# Counter - UDP client with timeout.  python client_udp.py 10001   (10000 = direct UDP server)
import socket
import struct
import sys
import time
import random

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 10001
SERVER = ("localhost", PORT)
commands = [(b'+', 10), (b'+', 5), (b'-', 3), (b'?', 0), (b'*', 2)]
packer = struct.Struct('!ci')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)
for op, num in commands:
    time.sleep(random.randint(1, 2))
    sock.sendto(packer.pack(op, num), SERVER)
    try:
        data, _ = sock.recvfrom(packer.size)
        answer, value = packer.unpack(data)
        print(f"{op.decode()} {num} -> {answer.decode()} {value}")
    except (socket.timeout, ConnectionError):
        print("no answer")
sock.close()
