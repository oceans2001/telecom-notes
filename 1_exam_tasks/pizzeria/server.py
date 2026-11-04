# PIZZERIA - server (subtasks 1, 2, 3, 5)
# Run: python server.py menu.txt
#   client -> server : b"MENU"                              (text)
#   server -> client : b"Margherita:2500|Pepperoni:3200"     (text)
#   client -> server : struct('!12si')  pizza, quantity
#   server -> client : struct('!?i8s')  accepted, total, order ID
#   server -> kitchen (UDP): "ID;pizza;qty;total:md5"  only for accepted orders
import socket
import struct
import random
import string
import sys
import select
import hashlib

packer1 = struct.Struct('!12si')
packer2 = struct.Struct('!?i8s')

# --- subtask 5: UDP client towards the kitchen (no bind) ---
KITCHEN_ADDR = ("localhost", 10002)
kitchen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
kitchen_sock.settimeout(2)

def send_to_kitchen(order_id, pizza, quantity, total):
    body = f"{order_id};{pizza};{quantity};{total}"
    checksum = hashlib.md5(body.encode()).hexdigest()
    msg = f"{body}:{checksum}"
    kitchen_sock.sendto(msg.encode(), KITCHEN_ADDR)
    print("Sent to kitchen:", msg)
    try:
        reply, _ = kitchen_sock.recvfrom(4096)
        print("Kitchen replied:", reply.decode())
    except (socket.timeout, ConnectionError):
        print("kitchen timeout")

# --- subtask 2: menu from file  name;price;portions ---
menu = {}
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        name, price, portions = line.split(";")
        menu[name] = [int(price), int(portions)]
print("Menu loaded:", menu)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("localhost", 10000))
sock.listen(5)
print("Pizza server on localhost:10000")

inputs = [sock]

while True:
    readables, _, _ = select.select(inputs, [], inputs, 1)
    for s in readables:
        if s is sock:
            conn, addr = sock.accept()
            inputs.append(conn)
            print("Connected:", addr)
            continue

        data = s.recv(1024)                       # ONE recv per event
        if not data:
            print("Client left:", s.getpeername())
            inputs.remove(s)
            s.close()
            continue
        print("Received:", data)                  # raw bytes - order is binary!

        if data == b"MENU":                       # compare BEFORE decode
            text = "|".join(f"{name}:{price}" for name, (price, portions) in menu.items())
            s.sendall(text.encode())
            print("Menu sent:", text)
            continue

        if len(data) != packer1.size:             # garbage would crash unpack
            s.sendall(packer2.pack(False, 0, b"00000000"))
            print("Bad message")
            continue

        pizza, quantity = packer1.unpack(data)
        pizza = pizza.decode().rstrip("\x00")

        if pizza in menu and quantity > 0 and menu[pizza][1] >= quantity:
            menu[pizza][1] -= quantity                         # change the dict itself
            total = quantity * menu[pizza][0]
            order_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            s.sendall(packer2.pack(True, total, order_id.encode()))
            print(f"Order OK: {quantity} x {pizza} = {total} HUF, ID {order_id}, "
                  f"{menu[pizza][1]} left")
            send_to_kitchen(order_id, pizza, quantity, total)  # AFTER answering client
        else:
            s.sendall(packer2.pack(False, 0, b"00000000"))
            print(f"Order FAILED: {quantity} x {pizza}")
