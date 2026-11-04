# LOTTERY - UDP server (Task I b). One socket for all clients, no select needed.
# Run: python3 lottery_server_udp.py [text|struct]
import socket
import struct
import sys
import random
import hashlib

HOST, PORT = "localhost", 10000
FORMAT = sys.argv[1] if len(sys.argv) > 1 else "text"
req = struct.Struct('!5ii')
resp = struct.Struct('!5iii')

def decode_request(data):
    if FORMAT == "text":
        body, got = data.decode().rsplit(":", 1)
        if hashlib.md5(body.encode()).hexdigest() != got:
            return None
        nums, bet = body.split(":")
        return [int(x) for x in nums.split(",")], int(bet)
    body, digest = data[:-16], data[-16:]
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

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print(f"Lottery UDP server on {HOST}:{PORT}, format={FORMAT}")

while True:
    data, addr = sock.recvfrom(4096)
    print(f"{addr} -> {data}")
    parsed = decode_request(data)
    if parsed is None:
        print("Checksum mismatch")
        sock.sendto(encode_response([0] * 5, 0, 0), addr)
        continue
    picks, bet = parsed
    drawn = random.sample(range(1, 21), 5)
    hits = len(set(picks) & set(drawn))
    win = hits * bet
    print(f"picks={picks} bet={bet} drawn={drawn} hits={hits} win={win}")
    sock.sendto(encode_response(drawn, hits, win), addr)
