# Counter - UDP server (no listen/accept/select, no b'' on leave)
import socket
import struct

packer = struct.Struct('!ci')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("localhost", 10000))
print("Counter UDP server on 10000")
counter = 0

while True:
    data, addr = sock.recvfrom(packer.size)
    op, num = packer.unpack(data)
    if op == b'+':
        counter += num
    elif op == b'-':
        counter -= num
    elif op == b'?':
        pass
    else:
        sock.sendto(packer.pack(b'E', 0), addr)
        continue
    print(f"{addr}: {op.decode()} {num} -> {counter}")
    sock.sendto(packer.pack(b'O', counter), addr)
