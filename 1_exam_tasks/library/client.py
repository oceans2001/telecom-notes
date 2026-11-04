# LIBRARY - client (subtask 4: title from command line)
# Run: python3 client.py Dune
import socket
import struct
import sys

HOST, PORT = "localhost", 10000
packer = struct.Struct('2s6s')
book = sys.argv[1] if len(sys.argv) > 1 else "Dune"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Sending: LIST")
client.sendall(b"LIST")
data = client.recv(1024)
print("Received books:")
for item in data.decode().split("|"):
    title, author = item.split(";")
    print(f"  {title}, {author}")

print("Borrowing:", book)
client.sendall(book.encode())

result, loan_id = packer.unpack(client.recv(packer.size))
if result == b"OK":
    print(f"Loan successful, loan ID: {loan_id.decode()}")
else:
    print(f"Loan failed, loan ID: {loan_id.decode()}")

client.close()
