# Text message + MD5 over UDP - client, third message corrupted on purpose
import socket
import hashlib

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

for text in ["hello world", "time: 12:30", "network"]:
    checksum = hashlib.md5(text.encode()).hexdigest()   # 1st encode: for md5
    if text == "network":
        text = text.replace("o", "X")                   # corrupt AFTER checksum
    msg = f"{text}:{checksum}".encode()                 # 2nd encode: for sending
    sock.sendto(msg, ("localhost", 10000))
    try:
        data, _ = sock.recvfrom(4096)
        print(f"sent: {text} -> {data.decode()}")
    except socket.timeout:
        print("no answer")
sock.close()
