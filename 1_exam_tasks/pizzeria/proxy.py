# PIZZERIA - subtask 6: coupon proxy (-20% on menu and on accepted orders)
# Chain: client -> proxy :10001 -> server :10000
# One client at a time, clients come one after another.
import socket
import struct

packer1 = struct.Struct('!12si')
packer2 = struct.Struct('!?i8s')
PROXY_ADDR = ("localhost", 10001)
SERVER_ADDR = ("localhost", 10000)

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_sock.bind(PROXY_ADDR)
listen_sock.listen(1)
print("Coupon proxy on", PROXY_ADDR)

saved = 0                                         # ONCE, before the loop

while True:                                       # client after client
    client_conn, client_addr = listen_sock.accept()
    print("Client connected:", client_addr)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect(SERVER_ADDR)

    while True:
        # --- step 1: MENU -> server, modify TEXT answer ---
        data1 = client_conn.recv(1024)
        if not data1:
            break
        server_sock.sendall(data1)
        reply1 = server_sock.recv(1024)
        print("Menu from server:", reply1.decode())

        parts = []                                # collect, join ONCE, send ONCE
        for item in reply1.decode().split("|"):
            pizza, price = item.split(":")
            parts.append(f"{pizza}:{int(price) * 80 // 100}")
        text = "|".join(parts)
        print("Menu to client:  ", text)
        client_conn.sendall(text.encode())

        # --- step 2: order -> server unchanged ---
        data2 = client_conn.recv(packer1.size)
        if not data2:
            break
        server_sock.sendall(data2)
        pizza, qty = packer1.unpack(data2)
        print(f"Order: {qty} x {pizza.decode().rstrip(chr(0))}")

        # --- step 3: modify STRUCT answer: unpack, change, pack AGAIN ---
        ok, total, order_id = packer2.unpack(server_sock.recv(packer2.size))
        if ok:
            new_total = total * 80 // 100          # // keeps it int for 'i'
            discount = total - new_total
            saved += discount
            print(f"Server total: {total} -> client total: {new_total} "
                  f"(saved {discount}, total saved {saved})")
            total = new_total
        else:
            print("Order failed, forwarded unchanged")
        client_conn.sendall(packer2.pack(ok, total, order_id))

    server_sock.close()                           # only these two
    client_conn.close()
