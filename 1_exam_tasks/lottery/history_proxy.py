# LOTTERY - Task V a: history server acting as a proxy (TCP, text format)
# Chain: client -> proxy :10001 -> lottery_server_tcp.py :10000
# Run: python3 lottery_server_tcp.py text ; python3 history_proxy.py
#      python3 lottery_client.py tcp text random port=10001
import socket
import json

PROXY_ADDR = ("localhost", 10001)
SERVER_ADDR = ("localhost", 10000)
LOG_FILE = "history.json"

def append_json(path, record):
    try:
        with open(path) as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    history.append(record)
    with open(path, "w") as f:
        json.dump(history, f, indent=2)

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_sock.bind(PROXY_ADDR)
listen_sock.listen(1)
print("History proxy on", PROXY_ADDR)

while True:
    client_conn, client_addr = listen_sock.accept()
    print("Client:", client_addr)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect(SERVER_ADDR)

    request = client_conn.recv(1024)
    if request:
        print("client -> server:", request)
        server_sock.sendall(request)
        reply = server_sock.recv(1024)
        print("server -> client:", reply)

        # read both messages for the log (proxy forwards bytes unchanged)
        nums, bet = request.decode().rsplit(":", 1)[0].split(":")
        drawn, hits, win = reply.decode().rsplit(":", 1)[0].split(":")
        append_json(LOG_FILE, {
            "picks": [int(x) for x in nums.split(",")], "bet": int(bet),
            "drawn": [int(x) for x in drawn.split(",")], "win": int(win)})
        print("Logged to", LOG_FILE)

        client_conn.sendall(reply)

    server_sock.close()
    client_conn.close()
