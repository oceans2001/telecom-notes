# BINARY FILES: fixed-size records, write, read all, seek to record N
# Run: python3 05_binary_files.py
import struct

rec = struct.Struct('8s f ?')                       # 8 + 4 + 1 = 13 bytes
records = [("web01", 12.5, True), ("db01", 0.0, False), ("dns01", 3.2, True)]

with open("demo.bin", "wb") as f:                   # wb = write binary
    for name, latency, ok in records:
        f.write(rec.pack(name.encode(), latency, ok))

# read ALL records until end of file
with open("demo.bin", "rb") as f:
    while True:
        chunk = f.read(rec.size)
        if not chunk:                               # b'' -> end of file
            break
        name, latency, ok = rec.unpack(chunk)
        host = name.decode().strip('\x00')
        print(f"{host}: {latency:.1f} {ok}")

# jump directly to record with index 2
with open("demo.bin", "rb") as f:
    f.seek(rec.size * 2)
    print("record 2:", rec.unpack(f.read(rec.size)))

# number of records = file size / record size
import os
print("records in file:", os.path.getsize("demo.bin") // rec.size)

# raw bytes of any file (pictures etc.) in chunks
with open("demo.bin", "rb") as f:
    while chunk := f.read(5):                       # Python 3.8+
        print(chunk)
