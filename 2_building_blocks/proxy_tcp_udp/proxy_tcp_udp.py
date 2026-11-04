# Counter - TCP client -> proxy :10001 -> UDP server :10000 (protocol translation)
import socket
import struct

packer = struct.Struct('!ci')
SERVER_ADDR = ("localhost", 10000)

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_sock.bind(("localhost", 10001))
listen_sock.listen(1)

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP CLIENT: no bind
udp_sock.settimeout(2)

while True:
    client_conn, client_addr = listen_sock.accept()
    print("client connected:", client_addr)
    while True:
        data = client_conn.recv(packer.size)
        if not data:
            break
        op, num = packer.unpack(data)
        print(f"client -> server: {op.decode()} {num}")
        udp_sock.sendto(data, SERVER_ADDR)
        try:
            reply, _ = udp_sock.recvfrom(packer.size)
            ans, val = packer.unpack(reply)
            print(f"server -> client: {ans.decode()} {val}")
        except (socket.timeout, ConnectionError):
            print("server timeout")
            reply = packer.pack(b'E', 0)          # client must always get an answer
        client_conn.sendall(reply)
    client_conn.close()
