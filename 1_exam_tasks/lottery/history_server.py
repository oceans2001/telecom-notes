# LOTTERY - history server (Task V b and c): UDP, JSON text in, append to history.json
# Run: python3 history_server.py
import socket
import json

ADDR = ("localhost", 10005)
LOG_FILE = "history.json"

def append_json(path, record):
    try:
        with open(path) as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    history.append(record)
    with open(path, "w") as f:
        json.dump(history, f, indent=2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ADDR)
print("History server on", ADDR)

while True:
    data, addr = sock.recvfrom(4096)
    record = json.loads(data.decode())          # bytes -> str -> dict
    print(f"{addr}: {record}")
    append_json(LOG_FILE, record)
    sock.sendto(b"SAVED", addr)
