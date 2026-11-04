# UDP file transfer - server (Practice 5, Exercise IV + reliability)
# Each datagram: struct('!i') sequence number + up to 200 bytes of data.
# Empty data = end of file. Server answers b"OK" + same seq number.
# Duplicate (resent) chunk -> answer OK again, but DON'T write twice.
# Run: python3 server.py [drop]     ("drop" = randomly lose 20% of OKs for testing)
import socket
import struct
import sys
import random
import hashlib

seq_packer = struct.Struct('!i')
DROP = "drop" in sys.argv

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("localhost", 10000))
print("UDP file server on 10000, drop =", DROP)

n = 0
while True:                                         # file after file
    expected = 0
    chunks = total = 0
    md5 = hashlib.md5()
    with open(f"received{n}.bin", "wb") as out:
        while True:                                 # chunk after chunk
            packet, addr = sock.recvfrom(4096)
            (seq,) = seq_packer.unpack(packet[:seq_packer.size])
            chunk = packet[seq_packer.size:]

            if seq == expected:                     # new chunk
                if not chunk:                       # end marker
                    sock.sendto(b"OK" + seq_packer.pack(seq), addr)
                    break
                out.write(chunk)
                md5.update(chunk)
                chunks += 1
                total += len(chunk)
                expected += 1
            else:
                print(f"duplicate seq {seq}, not written")

            if DROP and random.random() < 0.2:
                print(f"dropped OK for {seq}")
                continue
            sock.sendto(b"OK" + seq_packer.pack(seq), addr)

    print(f"file {n}: {chunks} chunks, {total} bytes, md5 {md5.hexdigest()}")
    n += 1
