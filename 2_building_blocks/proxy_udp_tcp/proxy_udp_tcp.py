# Counter - UDP client -> proxy :10001 -> TCP server :10000 (protocol translation)
# Mirror of proxy_tcp_udp.py:
#   client side = UDP SERVER  (bind, recvfrom, sendto(addr))  - no accept, no b'' check
#   server side = TCP CLIENT  (connect once, sendall, recv)
# Start order: python ../tcp_select_struct/server_select.py -> python proxy_udp_tcp.py
#              -> python client_udp.py 10001
import socket
import struct

packer = struct.Struct('!ci')
PROXY_ADDR = ("localhost", 10001)
SERVER_ADDR = ("localhost", 10000)

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # UDP SERVER: bind needed
udp_sock.bind(PROXY_ADDR)
print("UDP proxy listening on", PROXY_ADDR)

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP CLIENT: connect once
tcp_sock.connect(SERVER_ADDR)
print("Connected to TCP server", SERVER_ADDR)
# NOTE: all UDP clients share this ONE TCP connection -> server sees them as one client.
# If the server must tell clients apart: keep a dict addr -> own TCP socket.

while True:                                       # only ONE loop: just a stream of datagrams
    data, addr = udp_sock.recvfrom(packer.size)   # from ANY client, addr = who sent it
    op, num = packer.unpack(data)
    print(f"{addr} -> server: {op.decode()} {num}")
    tcp_sock.sendall(data)                        # forward over TCP

    reply = tcp_sock.recv(packer.size)
    if not reply:                                 # TCP server closed the connection
        print("server closed the connection")
        break
    ans, val = packer.unpack(reply)
    print(f"server -> {addr}: {ans.decode()} {val}")
    udp_sock.sendto(reply, addr)                  # back to THE client that asked

tcp_sock.close()
udp_sock.close()
