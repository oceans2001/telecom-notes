# PATTERN: select server with
#   1) per-client state   (dict: socket -> data about that client)
#   2) broadcast          (send to ALL / all OTHER clients)
#   3) timer event        (something happens after N seconds)
# Demo protocol (text): "NAME alice" | "MSG hello" | "WHO"
# Run: python3 select_broadcast_state_timer.py 30    (server closes after 30 s)
# Test: nc localhost 10000   (type lines) or a small client
import socket
import select
import sys
import time

DURATION = int(sys.argv[1]) if len(sys.argv) > 1 else 30
deadline = time.time() + DURATION
closed = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 10000))
server.listen(5)
print(f"Server on 10000, closing in {DURATION} s")

inputs = [server]
clients = {}                                   # 1) socket -> {"name": ..., "count": ...}

def broadcast(text, exclude=None):            # 2) to every client except one
    for c in inputs:
        if c is not server and c is not exclude:
            try:
                c.sendall(text.encode())
            except OSError:
                pass                           # dead socket, will be removed on recv
    print("[broadcast]", text.strip())

while True:
    # 3) timer: checked every loop (select timeout = 1 s -> at least once per second)
    if not closed and time.time() >= deadline:
        closed = True
        broadcast("SERVER CLOSED\n")
        print("Deadline reached")

    readable, _, _ = select.select(inputs, [], inputs, 1)
    for s in readable:
        if s is server:
            conn, addr = server.accept()
            inputs.append(conn)
            clients[conn] = {"name": f"{addr[0]}:{addr[1]}", "count": 0}
            print("New client:", addr)
            continue

        data = s.recv(1024)
        if not data:
            info = clients.pop(s)              # remove its state too
            inputs.remove(s)
            s.close()
            print("Left:", info["name"])
            broadcast(f"{info['name']} left\n")
            continue

        line = data.decode().strip()
        state = clients[s]                     # THIS client's state
        state["count"] += 1
        print(f"{state['name']} ({state['count']}) -> {line}")

        if closed:
            s.sendall(b"CLOSED\n")
        elif line.startswith("NAME "):
            state["name"] = line[5:]
            s.sendall(f"hello {state['name']}\n".encode())
        elif line.startswith("MSG "):
            broadcast(f"{state['name']}: {line[4:]}\n", exclude=s)
            s.sendall(b"SENT\n")
        elif line == "WHO":
            names = ",".join(c["name"] for c in clients.values())
            s.sendall(f"{names}\n".encode())
        else:
            s.sendall(b"UNKNOWN\n")

# NOTE for UDP: no sockets per client -> keep state in a dict keyed by addr:
#   state = clients.setdefault(addr, {"count": 0})
