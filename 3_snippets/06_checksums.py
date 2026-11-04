# CHECKSUMS: MD5 / SHA / CRC32, text and binary, files, verify
# Run: python3 06_checksums.py
import hashlib
import zlib

data = b"Hello"                                   # input is ALWAYS bytes

print(hashlib.md5(data).hexdigest())              # str, 32 hex chars  -> for text protocols
print(hashlib.md5(data).digest())                 # bytes, 16 bytes    -> for binary protocols
print(hashlib.sha1(data).hexdigest())             # 40 chars
print(hashlib.sha256(data).hexdigest())           # 64 chars
crc = zlib.crc32(data)                            # int (0 .. 2**32-1)
print(crc, hex(crc), f"{crc:08x}")                # '{:08x}' = always 8 hex chars

# --- text message with checksum:  "payload:checksum" ---
payload = "time: 12:30"
msg = f"{payload}:{hashlib.md5(payload.encode()).hexdigest()}"
text, got = msg.rsplit(":", 1)                    # cut at the LAST ':'
print("md5 ok:", hashlib.md5(text.encode()).hexdigest() == got)

# --- same with CRC32 ---
msg = f"{payload}|{zlib.crc32(payload.encode())}"
text, got = msg.rsplit("|", 1)
print("crc ok:", zlib.crc32(text.encode()) == int(got))   # got is str -> int!

# --- binary: struct body + checksum bytes ---
import struct
body = struct.pack('!ci', b'+', 10)
packet = body + hashlib.md5(body).digest()                # + 16 bytes
b, d = packet[:-16], packet[-16:]
print("binary md5 ok:", hashlib.md5(b).digest() == d)

packet = body + struct.pack('!I', zlib.crc32(body))       # + 4 bytes ('I' unsigned!)
b, (c,) = packet[:-4], struct.unpack('!I', packet[-4:])
print("binary crc ok:", zlib.crc32(b) == c)

# --- checksum of a file, chunk by chunk (same result as whole file) ---
def file_md5(path):
    m = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(4096):
            m.update(chunk)
    return m.hexdigest()
print(file_md5(__file__))

# --- corrupt on purpose to test the receiver ---
payload = "network"
checksum = hashlib.md5(payload.encode()).hexdigest()
payload = payload.replace("o", "X")              # change AFTER computing the checksum
print(f"{payload}:{checksum}")
