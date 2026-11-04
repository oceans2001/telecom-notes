# CINEMA - client
# Run directly:      python3 client.py Dune 17:30
# Run through proxy: python3 client.py Dune 17:30 10001
import socket
import struct
import sys

title = sys.argv[1] if len(sys.argv) > 1 else "Dune"
start = sys.argv[2] if len(sys.argv) > 2 else "17:30"
PORT = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
HOST = "localhost"
packer = struct.Struct('7s6s')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Sending: GET_SCREENINGS")
client.sendall(b"GET_SCREENINGS")
data = client.recv(1024)
print("Received screenings:")
for item in data.decode().split("|"):
    t, hall, st = item.split(";")
    print(f"  {t}, {hall}, {st}")

print(f"Buying ticket: {title} {start}")
client.sendall(f"{title};{start}".encode())

reply = client.recv(packer.size)
result, ticket = packer.unpack(reply)
result = result.decode().strip('\x00')       # 'FAIL\x00\x00\x00' -> 'FAIL'
ticket = ticket.decode()
if result == "SUCCESS":
    print(f"Purchase successful, ticket ID: {ticket}")
else:
    print(f"Purchase failed, ticket ID: {ticket}")

client.close()
