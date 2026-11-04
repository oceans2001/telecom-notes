# UDP file transfer - client: 200 byte chunks, stop-and-wait, resend on timeout
# Run: python3 client.py photo.jpg
import socket
import struct
import sys
import hashlib

SERVER = ("localhost", 10000)
CHUNK = 200
RETRIES = 5
seq_packer = struct.Struct('!i')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)

def send_reliable(seq, chunk):
    packet = seq_packer.pack(seq) + chunk
    for attempt in range(RETRIES):
        sock.sendto(packet, SERVER)
        try:
            reply, _ = sock.recvfrom(16)
            if reply == b"OK" + seq_packer.pack(seq):
                return
        except socket.timeout:
            print(f"timeout on seq {seq}, resend ({attempt + 1})")
    else:                                    # loop ended without return
        print("server not responding")
        sys.exit(1)

seq = chunks = total = 0
md5 = hashlib.md5()
with open(sys.argv[1], "rb") as f:
    while True:
        chunk = f.read(CHUNK)
        if not chunk:
            break
        send_reliable(seq, chunk)
        md5.update(chunk)
        chunks += 1
        total += len(chunk)
        seq += 1
send_reliable(seq, b"")                      # end of file marker

print(f"sent {chunks} chunks, {total} bytes, md5 {md5.hexdigest()}")
sock.close()
