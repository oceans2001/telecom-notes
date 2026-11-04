# Counter - proxy that steals 20% of every '+' and fakes answers so the client won't notice
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
    stolen = 0                                    # per client: the server counter is shared,
                                                  # so for a fair fake keep it simple per session
    while True:
        data = client_conn.recv(packer.size)
        if not data:
            break
        op, num = packer.unpack(data)             # 1. unpack
        print(f"client -> proxy:  {op.decode()} {num}")
        tax = 0
        if op == b'+':                            # 2. change
            tax = num // 5
            num -= tax
            stolen += tax
        server_sock.sendall(packer.pack(op, num)) # 3. pack AGAIN and send
        print(f"proxy -> server:  {op.decode()} {num} (tax {tax}, stolen {stolen})")

        ans, val = packer.unpack(server_sock.recv(packer.size))
        print(f"server -> proxy:  {ans.decode()} {val}")
        if ans == b'O':
            val += stolen                         # fake: add back what we stole
        client_conn.sendall(packer.pack(ans, val))
        print(f"proxy -> client:  {ans.decode()} {val}")
    print("total stolen:", stolen)
    server_sock.close()
    client_conn.close()
