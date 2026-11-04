# LIBRARY - server (subtasks 1-3: TCP, books from file, select)
# Run: python3 server.py books.txt
#
# Protocol:
#   client -> server : b"LIST"                     (text)
#   server -> client : b"Dune;Herbert|1984;Orwell"  (text, books by |, fields by ;)
#   client -> server : b"Dune"                      (text, title)
#   server -> client : struct('2s6s')  OK + loan ID  /  NO + 000000
import socket
import struct
import select
import sys
import random
import string

HOST, PORT = "localhost", 10000
packer = struct.Struct('2s6s')

# --- subtask 2: data from file  title;author;copies ---
books = {}                                   # title -> [author, copies]
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        title, author, copies = line.split(";")
        books[title] = [author, int(copies)]
print("Loaded books:", books)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
print(f"Library server on {HOST}:{PORT}")

inputs = [server]

while True:
    readable, _, _ = select.select(inputs, [], inputs, 1)
    for s in readable:
        if s is server:
            conn, addr = server.accept()
            inputs.append(conn)
            print("New client:", addr)
            continue

        data = s.recv(1024)                  # ONE recv per event
        if not data:
            print("Client left:", s.getpeername())
            inputs.remove(s)
            s.close()
            continue

        msg = data.decode()
        print(f"{s.getpeername()} -> {msg}")

        if msg == "LIST":
            text = "|".join(f"{t};{a}" for t, (a, c) in books.items())
            s.sendall(text.encode())
            print("Sent list:", text)
        else:
            title = msg
            if title in books and books[title][1] > 0:
                books[title][1] -= 1
                loan_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
                s.sendall(packer.pack(b"OK", loan_id.encode()))
                print(f"OK {loan_id} ({title}: {books[title][1]} copies left)")
            elif title in books:
                s.sendall(packer.pack(b"NO", b"000000"))
                print(f"NO 000000 ({title}: no copies left)")
            else:
                s.sendall(packer.pack(b"NO", b"000000"))
                print(f"NO 000000 ({title}: book not found)")
