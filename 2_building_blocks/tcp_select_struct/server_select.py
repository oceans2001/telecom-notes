# Counter - TCP server, many clients with select, shared counter
import socket
import struct
import select

packer = struct.Struct('!ci')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("localhost", 10000))
sock.listen(5)
print("Counter TCP server on 10000")

inputs = [sock]
counter = 0                                   # created ONCE -> shared

while True:
    readable, _, _ = select.select(inputs, [], inputs, 1)
    for s in readable:
        if s is sock:
            conn, addr = sock.accept()
            inputs.append(conn)
            print("new client:", addr)
            continue
        data = s.recv(packer.size)
        if not data:
            print("client left:", s.getpeername())
            inputs.remove(s)
            s.close()
            continue
        op, num = packer.unpack(data)
        if op == b'+':
            counter += num
        elif op == b'-':
            counter -= num
        elif op == b'?':
            pass
        else:
            s.sendall(packer.pack(b'E', 0))
            continue
        print(f"{s.getpeername()}: {op.decode()} {num} -> {counter}")
        s.sendall(packer.pack(b'O', counter))
