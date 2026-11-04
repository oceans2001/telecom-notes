# CINEMA - server (subtasks 1-3: TCP, screenings from file, select)
# Run: python3 server.py screenings.txt
#
# Protocol:
#   client -> server : b"GET_SCREENINGS"
#   server -> client : b"Dune;Hall 1;17:30|Oppenheimer;Hall 2;19:00|..."
#   client -> server : b"Dune;17:30"
#   server -> client : struct('7s6s')  SUCCESS + ticket ID / FAIL + 000000
import socket
import struct
import select
import sys
import random
import string

HOST, PORT = "localhost", 10000
packer = struct.Struct('7s6s')

# key = (title, start) -> one film can have several screenings
screenings = {}                              # (title, start) -> [hall, free seats]
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        title, hall, start, free = line.split(";")
        screenings[(title, start)] = [hall, int(free)]
print("Loaded screenings:", screenings)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
print(f"Cinema server on {HOST}:{PORT}")

inputs = [server]

while True:
    readable, _, _ = select.select(inputs, [], inputs, 1)
    for s in readable:
        if s is server:
            conn, addr = server.accept()
            inputs.append(conn)
            print("New client:", addr)
            continue

        data = s.recv(1024)
        if not data:
            print("Client left:", s.getpeername())
            inputs.remove(s)
            s.close()
            continue

        msg = data.decode()
        print(f"{s.getpeername()} -> {msg}")

        if msg == "GET_SCREENINGS":
            text = "|".join(f"{t};{hall};{start}" for (t, start), (hall, free) in screenings.items())
            s.sendall(text.encode())
            print("Sent screenings:", text)
        elif msg.count(";") == 1:
            title, start = msg.split(";")
            key = (title, start)
            if key in screenings and screenings[key][1] > 0:
                screenings[key][1] -= 1
                ticket = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
                s.sendall(packer.pack(b"SUCCESS", ticket.encode()))
                print(f"SUCCESS {ticket} ({title} {start}: {screenings[key][1]} seats left)")
            else:
                s.sendall(packer.pack(b"FAIL", b"000000"))
                print(f"FAIL 000000 ({title} {start})")
        else:
            s.sendall(packer.pack(b"FAIL", b"000000"))
            print("Bad request")
