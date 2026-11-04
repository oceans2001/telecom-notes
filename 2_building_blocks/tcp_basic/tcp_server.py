# TCP-сервер для ОДНОГО клиента (без select).
# Запуск: python3 tcp_server.py localhost 10000
# Демо-протокол: клиент шлёт текст, сервер отвечает struct('!ci').
import socket
import struct
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 10000   # argv всегда str -> int!

packer = struct.Struct('!ci')        # одинаковый формат у клиента и сервера

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # ДО bind
server.bind((HOST, PORT))
server.listen(1)
print(f"Server listening on {HOST}:{PORT}")

conn, addr = server.accept()          # conn - сокет ЭТОГО клиента
print("Client connected:", addr)

while True:
    data = conn.recv(1024)
    if not data:                      # b'' -> клиент закрыл соединение
        print("Client left")
        break
    msg = data.decode()
    print("Received:", msg)

    reply = packer.pack(b'O', len(msg))        # в 's'/'c' только bytes!
    conn.sendall(reply)
    print("Sent: O", len(msg))

conn.close()
server.close()
