# Counter - transparent TCP proxy that logs everything. client:10001 -> server:10000
import socket
import struct

packer = struct.Struct('!ci')

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_sock.bind(("localhost", 10001))
listen_sock.listen(1)

while True:
    client_conn, client_addr = listen_sock.accept()
    print("client connected:", client_addr)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect(("localhost", 10000))
    while True:
        data = client_conn.recv(packer.size)
        if not data:
            break
        op, num = packer.unpack(data)
        print(f"client -> server: {op.decode()} {num}")
        server_sock.sendall(data)                 # forward ORIGINAL bytes
        reply = server_sock.recv(packer.size)
        ans, val = packer.unpack(reply)
        print(f"server -> client: {ans.decode()} {val}")
        client_conn.sendall(reply)
    server_sock.close()
    client_conn.close()
