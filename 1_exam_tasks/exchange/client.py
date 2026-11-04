# CURRENCY EXCHANGE - client (subtask 4: input from stdin)
# Run: python3 client.py
import socket
import struct

HOST, PORT = "localhost", 10000
req = struct.Struct('3sf')
resp = struct.Struct('?f')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Sending: RATES")
client.sendall(b"RATES")
data = client.recv(1024)
print("Received rates:")
for item in data.decode().split("|"):
    code, rate = item.split(":")
    print(f"  {code} = {rate} HUF")

code = input("Currency: ").strip().upper()
huf = float(input("Amount in HUF: "))
print(f"Buying {code} for {huf} HUF")
client.sendall(req.pack(code.encode(), huf))

ok, got = resp.unpack(client.recv(resp.size))
if ok:
    print(f"Exchange successful, received: {got:.2f} {code}")
else:
    print("Exchange failed, received: 0.00")

client.close()
