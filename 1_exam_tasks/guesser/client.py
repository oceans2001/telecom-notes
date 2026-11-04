# ASSIGNMENT III - Barkoba client, binary search, no stdin
# Run: python3 client.py localhost 10000
import socket
import struct
import sys
import random
import time

packer = struct.Struct('ci')

def ask(sock, op, num):
    sock.sendall(packer.pack(op, num))
    reply, _ = packer.unpack(sock.recv(packer.size))
    return reply

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((sys.argv[1], int(sys.argv[2])))

low, high = 1, 100                    # answer is always inside [low, high]
while low < high:                     # more than one candidate left
    time.sleep(random.randint(1, 5))
    mid = (low + high) // 2
    answer = ask(sock, b'>', mid)
    print(f"[{low}, {high}] > {mid}? {answer.decode()}")
    if answer == b'I':                # bigger than mid -> mid is out
        low = mid + 1
    elif answer == b'N':              # not bigger -> mid may still be it
        high = mid
    else:                             # V: someone else won
        print("Game over")
        sock.close()
        sys.exit()

time.sleep(random.randint(1, 5))
result = ask(sock, b'=', low)         # low == high, one candidate
print(f"= {low}? {result.decode()}")
sock.close()
