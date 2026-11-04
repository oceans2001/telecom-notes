# PIZZERIA - subtask 5: kitchen log server (UDP + MD5 + append to orders.json)
# Run: python kitchen.py
import socket
import hashlib
import json

def append_json(path, record):
    try:
        with open(path) as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    history.append(record)
    with open(path, "w") as f:
        json.dump(history, f, indent=2)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 10002))
print("Kitchen server on localhost:10002")

while True:
    data, addr = server.recvfrom(4096)
    body, got_sum = data.decode().rsplit(":", 1)
    calc_sum = hashlib.md5(body.encode()).hexdigest()

    if calc_sum == got_sum:
        order_id, pizza, quantity, total = body.split(";")
        append_json("orders.json", {"order_id": order_id, "pizza": pizza,
                                    "quantity": int(quantity), "total": int(total)})
        answer = "SAVED"
    else:
        answer = "CORRUPTED"

    server.sendto(answer.encode(), addr)
    print(f"{addr}: {body} | got {got_sum} | calc {calc_sum} -> {answer}")
