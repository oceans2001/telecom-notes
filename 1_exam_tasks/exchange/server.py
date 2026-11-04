# CURRENCY EXCHANGE - server (subtasks 1,2,3,5)
# Run: python3 server.py rates.json
# Start order: audit.py -> server.py -> client.py
#
# Protocol (client <-> server, TCP):
#   client -> server : b"RATES"                         (text)
#   server -> client : b"EUR:395.5|USD:362.0|GBP:461.2" (text)
#   client -> server : struct('3sf')  currency, HUF amount
#   server -> client : struct('?f')   success, received amount
# Audit (server -> audit, UDP):  "EUR;10000.00;25.28;True:<md5>"
import socket
import struct
import select
import sys
import json
import hashlib

HOST, PORT = "localhost", 10000
AUDIT_ADDR = ("localhost", 10002)
req = struct.Struct('3sf')        # no '!' -> native alignment: 3 + 1 pad + 4 = 8 bytes
resp = struct.Struct('?f')        # 1 + 3 pad + 4 = 8 bytes

# --- subtask 2: rates + reserves from JSON ---
with open(sys.argv[1]) as f:
    raw = json.load(f)
currencies = {code: [info["rate"], info["reserve"]] for code, info in raw.items()}
print("Loaded:", currencies)

# --- subtask 5: UDP CLIENT towards audit server (no bind!) ---
audit_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
audit_sock.settimeout(2)

def send_audit(code, huf, got, ok):
    body = f"{code};{huf:.2f};{got:.2f};{ok}"
    checksum = hashlib.md5(body.encode()).hexdigest()
    msg = f"{body}:{checksum}"
    audit_sock.sendto(msg.encode(), AUDIT_ADDR)
    print("Sent to audit:", msg)
    try:
        reply, _ = audit_sock.recvfrom(4096)
        print("Audit replied:", reply.decode())
    except (socket.timeout, ConnectionError):
        print("audit timeout")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
print(f"Exchange server on {HOST}:{PORT}")

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
        print(f"{s.getpeername()} -> {data}")

        # text vs struct: decide on RAW BYTES, before any decode()
        if data == b"RATES":
            text = "|".join(f"{code}:{rate}" for code, (rate, reserve) in currencies.items())
            s.sendall(text.encode())
            print("Sent rates:", text)
            continue

        if len(data) != req.size:                    # garbage would crash unpack
            print("Bad message")
            s.sendall(resp.pack(False, 0.0))
            continue

        code, huf = req.unpack(data)
        code = code.decode()
        print(f"Client wants {code} for {huf:.2f} HUF")

        if code not in currencies:
            s.sendall(resp.pack(False, 0.0))
            print("FAIL: unknown currency")
            send_audit(code, huf, 0.0, False)
            continue

        rate, reserve = currencies[code]             # copies - only for reading
        got = huf / rate
        if reserve >= got:
            currencies[code][1] -= got               # change the dict itself
            s.sendall(resp.pack(True, got))
            print(f"OK: {got:.2f} {code}, reserve left {currencies[code][1]:.2f}")
            send_audit(code, huf, got, True)
        else:
            s.sendall(resp.pack(False, 0.0))
            print(f"FAIL: not enough {code} (need {got:.2f}, have {reserve:.2f})")
            send_audit(code, huf, 0.0, False)
