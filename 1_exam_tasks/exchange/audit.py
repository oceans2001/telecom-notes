# CURRENCY EXCHANGE - subtask 5: audit server (UDP + MD5 + JSON append)
# Run: python3 audit.py
import socket
import hashlib
import json

AUDIT_ADDR = ("localhost", 10002)
LOG_FILE = "audit.json"

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
sock.bind(AUDIT_ADDR)
print("Audit server on", AUDIT_ADDR)

while True:
    data, addr = sock.recvfrom(4096)
    body, got_sum = data.decode().rsplit(":", 1)
    calc_sum = hashlib.md5(body.encode()).hexdigest()
    print(f"{addr}: {body} | got {got_sum} | calc {calc_sum}")

    if calc_sum == got_sum:
        code, huf, got, ok = body.split(";")
        append_json(LOG_FILE, {"currency": code, "huf": float(huf),
                               "received": float(got), "success": ok == "True"})
        answer = "LOGGED"
    else:
        answer = "CORRUPTED"

    sock.sendto(answer.encode(), addr)
    print("->", answer)
