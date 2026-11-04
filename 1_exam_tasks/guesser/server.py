# ASSIGNMENT III - Barkoba (number guessing), server with select
# Run: python3 server.py localhost 10000
# Message both ways: struct('ci') WITHOUT '!' (as the task requires)
#   client: '<' '>' '='  + number
#   server: I(yes) N(no) Y(win) K(out) V(game over) + 0
import socket
import struct
import select
import sys
import random

packer = struct.Struct('ci')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((sys.argv[1], int(sys.argv[2])))
server.listen(5)

inputs = [server]
secret = random.randint(1, 100)
game_over = False
print("secret:", secret)

while True:
    readable, _, _ = select.select(inputs, [], inputs, 1)
    for s in readable:
        if s is server:
            conn, addr = server.accept()
            inputs.append(conn)
            print("new client:", addr)
            continue

        data = s.recv(packer.size)
        if not data:
            print("client left:", s.getpeername())
            inputs.remove(s)
            s.close()
            if len(inputs) == 1 and game_over:        # everybody left -> new game
                secret = random.randint(1, 100)
                game_over = False
                print("new game, secret:", secret)
            continue

        sign, num = packer.unpack(data)
        if game_over:
            reply = b'V'
        elif sign == b'<':
            reply = b'I' if secret < num else b'N'
        elif sign == b'>':
            reply = b'I' if secret > num else b'N'
        elif sign == b'=':
            if secret == num:
                reply = b'Y'
                game_over = True
            else:
                reply = b'K'
        else:
            reply = b'N'

        s.sendall(packer.pack(reply, 0))
        print(f"{s.getpeername()}: {sign.decode()} {num} -> {reply.decode()}")
