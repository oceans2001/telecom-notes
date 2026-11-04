# PIZZERIA - client (subtask 4: argv, otherwise stdin)
# Run: python client.py Pepperoni 2        (direct)
#      python client.py Pepperoni 2 10001  (through the coupon proxy)
#      python client.py                    (asks on keyboard)
import socket
import struct
import sys

packer1 = struct.Struct('!12si')
packer2 = struct.Struct('!?i8s')
PORT = int(sys.argv[3]) if len(sys.argv) > 3 else 10000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", PORT))

print("Sending: MENU")
client.sendall(b"MENU")
data = client.recv(1024)
print("Menu:")
for item in data.decode().split("|"):
    pizza, price = item.split(":")
    print(f"  {pizza} - {price} HUF")

if len(sys.argv) >= 3:
    pizza, qty = sys.argv[1], int(sys.argv[2])
else:
    pizza = input("Enter pizza: ").strip()
    qty = int(input("Enter amount of pizzas: "))

print(f"Ordering {qty} x {pizza}")
client.sendall(packer1.pack(pizza.encode(), qty))

ok, total, order_id = packer2.unpack(client.recv(packer2.size))
print(f"Order {'accepted!' if ok else 'failed!'} Total: {total} HUF, order ID: {order_id.decode()}")

client.close()
