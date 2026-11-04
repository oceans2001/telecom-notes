# Text message + MD5 over UDP - server.  "text:md5" -> OK / CORRUPTED
import socket
import hashlib

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("localhost", 10000))

while True:
    data, addr = sock.recvfrom(4096)
    text, got_sum = data.decode().rsplit(":", 1)      # text may contain ':' itself
    calc = hashlib.md5(text.encode()).hexdigest()
    answer = "OK" if calc == got_sum else "CORRUPTED"
    sock.sendto(answer.encode(), addr)
    print(f"received: {text}\n  got  {got_sum}\n  calc {calc}\n  -> {answer}")
