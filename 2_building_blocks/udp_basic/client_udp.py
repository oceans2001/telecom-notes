# Counter - UDP client with timeout
import socket
import struct
import time
import random

commands = [(b'+', 10), (b'+', 5), (b'-', 3), (b'?', 0), (b'*', 2)]
packer = struct.Struct('!ci')
SERVER = ("localhost", 10000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)
for op, num in commands:
    time.sleep(random.randint(1, 2))
    sock.sendto(packer.pack(op, num), SERVER)
    try:
        data, _ = sock.recvfrom(packer.size)
        answer, value = packer.unpack(data)
        print(f"{op.decode()} {num} -> {answer.decode()} {value}")
    except socket.timeout:
        print("no answer")
sock.close()                                   # once, after the loop
