# LOTTERY - TCP server with select (Task I a, II, III, V b)
# Run: python3 lottery_server_tcp.py [text|struct] [history]
import socket
import select
import struct
import sys
import random
import hashlib
import json

HOST, PORT = "localhost", 10000
HISTORY_ADDR = ("localhost", 10005)
FORMAT = sys.argv[1] if len(sys.argv) > 1 else "text"
USE_HISTORY = "history" in sys.argv

req = struct.Struct('!5ii')       # 5 picks + bet
resp = struct.Struct('!5iii')     # 5 drawn + hits + win

# ---------- encode / decode for both formats ----------
def decode_request(data):
    """returns (picks, bet) or None if checksum is wrong"""
    if FORMAT == "text":
        body, got = data.decode().rsplit(":", 1)
        if hashlib.md5(body.encode()).hexdigest() != got:
            return None
        nums, bet = body.split(":")
        return [int(x) for x in nums.split(",")], int(bet)
    body, digest = data[:-16], data[-16:]          # struct + 16 byte md5 digest
    if hashlib.md5(body).digest() != digest:
        return None
    *picks, bet = req.unpack(body)
    return picks, bet

def encode_response(drawn, hits, win):
    if FORMAT == "text":
        body = f"{','.join(str(n) for n in drawn)}:{hits}:{win}"
        return f"{body}:{hashlib.md5(body.encode()).hexdigest()}".encode()
    body = resp.pack(*drawn, hits, win)
    return body + hashlib.md5(body).digest()

# ---------- Task V b: server reports to history server ----------
hist_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hist_sock.settimeout(2)

def report_history(addr, picks, bet, drawn, win):
    record = {"client": f"{addr[0]}:{addr[1]}", "picks": picks, "bet": bet,
              "drawn": drawn, "win": win}
    hist_sock.sendto(json.dumps(record).encode(), HISTORY_ADDR)
    try:
        reply, _ = hist_sock.recvfrom(1024)
        print("History:", reply.decode())
    except (socket.timeout, ConnectionError):
        print("History timeout")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
print(f"Lottery TCP server on {HOST}:{PORT}, format={FORMAT}, history={USE_HISTORY}")

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

        addr = s.getpeername()
        print(f"{addr} -> {data}")
        parsed = decode_request(data)
        if parsed is None:
            print("Checksum mismatch, ignoring")
            s.sendall(encode_response([0] * 5, 0, 0))
            continue

        picks, bet = parsed
        drawn = random.sample(range(1, 21), 5)
        hits = len(set(picks) & set(drawn))
        win = hits * bet
        print(f"picks={picks} bet={bet} drawn={drawn} hits={hits} win={win}")
        s.sendall(encode_response(drawn, hits, win))

        if USE_HISTORY:
            report_history(addr, picks, bet, drawn, win)
