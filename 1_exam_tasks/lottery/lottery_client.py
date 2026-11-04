# LOTTERY - client (Task IV a-d, Task V c)
# Run: python3 lottery_client.py tcp|udp text|struct random|stdin|json|argv [args] [history] [port=10001]
#   random                 -> 5 random numbers, random bet
#   stdin                  -> asks from keyboard
#   json picks.json        -> {"numbers": [...], "bet": 100}
#   argv 3 7 12 1 20 100   -> 5 numbers + bet from command line
import socket
import struct
import sys
import random
import hashlib
import json

args = sys.argv[1:]
TRANSPORT = args[0] if args else "tcp"
FORMAT = args[1] if len(args) > 1 else "text"
SOURCE = args[2] if len(args) > 2 else "random"
USE_HISTORY = "history" in args
PORT = 10000
for a in args:                       # optional "port=10001" to go through the proxy
    if a.startswith("port="):
        PORT = int(a.split("=")[1])
SERVER = ("localhost", PORT)
HISTORY_ADDR = ("localhost", 10005)

req = struct.Struct('!5ii')
resp = struct.Struct('!5iii')

# ---------- Task IV: where the picks come from ----------
if SOURCE == "random":
    picks = random.sample(range(1, 21), 5)
    bet = random.randint(1, 10) * 10
elif SOURCE == "stdin":
    picks = [int(x) for x in input("5 numbers (1-20, space separated): ").split()]
    bet = int(input("Bet: "))
elif SOURCE == "json":
    with open(args[3]) as f:
        cfg = json.load(f)
    picks, bet = cfg["numbers"], cfg["bet"]
elif SOURCE == "argv":
    nums = [int(x) for x in args[3:9]]
    picks, bet = nums[:5], nums[5]
print(f"Picks: {picks}, bet: {bet}")

# ---------- encode / decode ----------
def encode_request(picks, bet):
    if FORMAT == "text":
        body = f"{','.join(str(n) for n in picks)}:{bet}"
        return f"{body}:{hashlib.md5(body.encode()).hexdigest()}".encode()
    body = req.pack(*picks, bet)
    return body + hashlib.md5(body).digest()

def decode_response(data):
    if FORMAT == "text":
        body, got = data.decode().rsplit(":", 1)
        ok = hashlib.md5(body.encode()).hexdigest() == got
        nums, hits, win = body.split(":")
        return [int(x) for x in nums.split(",")], int(hits), int(win), ok
    body, digest = data[:-16], data[-16:]
    ok = hashlib.md5(body).digest() == digest
    *drawn, hits, win = resp.unpack(body)
    return drawn, hits, win, ok

msg = encode_request(picks, bet)
print("Sending:", msg)

# ---------- Task I: TCP or UDP ----------
if TRANSPORT == "tcp":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER)
    sock.sendall(msg)
    data = sock.recv(1024)
    sock.close()
else:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)
    sock.sendto(msg, SERVER)
    try:
        data, _ = sock.recvfrom(4096)
    except socket.timeout:
        print("No answer from server")
        sys.exit(1)
    sock.close()

print("Received:", data)
drawn, hits, win, ok = decode_response(data)
print(f"Checksum {'OK' if ok else 'WRONG'}")
print(f"Drawn: {drawn}, hits: {hits}, you win: {win}")

# ---------- Task V c: client reports to history server ----------
if USE_HISTORY:
    h = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    h.settimeout(2)
    record = {"picks": picks, "bet": bet, "drawn": drawn, "win": win}
    h.sendto(json.dumps(record).encode(), HISTORY_ADDR)
    try:
        print("History:", h.recvfrom(1024)[0].decode())
    except (socket.timeout, ConnectionError):
        print("History timeout")
    h.close()
