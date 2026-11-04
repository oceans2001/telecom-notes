# TIMEOUT + RETRY (UDP, or TCP recv with a limit)
# Run: python3 09_timeout_retry.py   (nobody listens on 10099 -> shows timeouts)
import socket

SERVER = ("localhost", 10099)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.5)                          # seconds; works for TCP sockets too

# --- single try ---
sock.sendto(b"ping", SERVER)
try:
    data, _ = sock.recvfrom(1024)
    print("answer:", data)
except (socket.timeout, ConnectionError):     # Mac may raise ConnectionRefusedError on UDP
    print("no answer")

# --- retry N times, for/else: else runs only if loop ended WITHOUT break ---
for attempt in range(3):
    sock.sendto(b"ping", SERVER)
    try:
        data, _ = sock.recvfrom(1024)
        print("answer:", data)
        break
    except (socket.timeout, ConnectionError):
        print(f"attempt {attempt + 1}: timeout, resend")
else:
    print("server not responding, giving up")

# --- TCP: connect may fail ---
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    tcp.connect(SERVER)
except ConnectionRefusedError:
    print("TCP: nobody listens on", SERVER)
tcp.close()
sock.close()
