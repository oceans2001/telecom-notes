# CINEMA - subtask 4: scalper proxy (man-in-the-middle)
# Chain: client -> proxy :10001 -> server :10000
# Start order: server -> proxy -> client (python3 client.py Dune 17:30 10001)
# One client at a time, clients come one after another.
import socket
import struct
import random

PROXY_ADDR = ("localhost", 10001)
SERVER_ADDR = ("localhost", 10000)
packer = struct.Struct('7s6s')

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_sock.bind(PROXY_ADDR)
listen_sock.listen(1)
print("Proxy listening on", PROXY_ADDR)

stolen = []

while True:                                          # client after client
    client_conn, client_addr = listen_sock.accept()
    print("Client connected:", client_addr)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect(SERVER_ADDR)
    print("Connected to server")

    while True:
        # step 1: GET_SCREENINGS -> relay unchanged both ways
        msg = client_conn.recv(1024)
        if not msg:
            break
        print("client -> server:", msg.decode())
        server_sock.sendall(msg)
        reply = server_sock.recv(1024)
        print("server -> client:", reply.decode())
        client_conn.sendall(reply)

        # step 2: purchase request -> relay unchanged
        msg = client_conn.recv(1024)
        if not msg:
            break
        print("client -> server:", msg.decode())
        server_sock.sendall(msg)

        # step 3: purchase response -> unpack, maybe steal, pack again
        reply = server_sock.recv(packer.size)
        result, ticket = packer.unpack(reply)
        result = result.decode().strip('\x00')
        ticket = ticket.decode()

        if result == "SUCCESS":
            if random.random() < 0.5:
                print("Forwarded ticket:", ticket)
                client_conn.sendall(reply)
            else:
                stolen.append(ticket)
                print("Stolen ticket:", ticket, "| all stolen:", stolen)
                client_conn.sendall(packer.pack(b"FAIL", b"000000"))
        else:
            print("Forwarded failed purchase: FAIL, 000000")
            client_conn.sendall(reply)

    server_sock.close()
    client_conn.close()
    print("Client finished, waiting for the next one")
