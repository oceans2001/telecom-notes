# TCP-клиент.
# Запуск: python3 tcp_client.py localhost 10000
import socket
import struct
import sys
import time
import random

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 10000

packer = struct.Struct('!ci')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))          # bind клиенту НЕ нужен
print(f"Connected to {HOST}:{PORT}")

for text in ["hello", "network", "exam"]:
    time.sleep(random.randint(1, 2))  # пауза, чтобы видеть чередование клиентов
    print("Sending:", text)
    client.sendall(text.encode())     # str -> bytes

    reply = client.recv(packer.size)  # ровно размер struct
    code, value = packer.unpack(reply)    # unpack ВСЕГДА tuple
    print("Received:", code.decode(), value)

client.close()
