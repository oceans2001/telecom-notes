# STRUCT: formats, sizes, alignment, strings, variable length
# Run: python3 04_struct.py
import struct

# c = 1 char (bytes)   Ns = string of N bytes   i = int (4)   f = float (4)
# d = double (8)       ? = bool (1)             h = short (2) H = unsigned short
# q = long long (8)    b = signed byte (1)      B = unsigned byte
#
# prefix: none/@ = native + ALIGNMENT    ! = network (big-endian, no padding)
#         < little-endian, no padding    > big-endian, no padding
for fmt in ["ci", "!ci", "3sf", "!3sf", "?f", "7s6s", "10s i ?", "!10si?"]:
    print(f"{fmt:10} size = {struct.calcsize(fmt)}")
# BOTH sides must use EXACTLY the same format string!

p = struct.Struct('!c10sif')
data = p.pack(b'B', b"alice", 7, 99.5)        # s and c need BYTES
print(data, len(data), p.size)

op, name, item, amount = p.unpack(data)       # always a tuple
name = name.decode().strip('\x00')            # b'alice\x00\x00...' -> 'alice'
print(op, name, item, amount)

# string longer than the field is silently CUT
print(struct.pack('3s', b"EURO"))             # b'EUR'

# float precision: 'f' is 4 bytes -> 0.1 is not exact
(x,) = struct.unpack('!f', struct.pack('!f', 0.1))
print(x, f"{x:.2f}")                          # use 'd' if you need exact-ish floats

# one value -> still a tuple
(n,) = struct.unpack('!i', struct.pack('!i', 42))
n2 = struct.unpack('!i', struct.pack('!i', 42))[0]
print(n, n2)

# --- variable number of values: send the count first ---
nums = [3, 7, 12, 1, 20]
msg = struct.pack('!i', len(nums)) + struct.pack(f'!{len(nums)}i', *nums)
(count,) = struct.unpack('!i', msg[:4])
values = list(struct.unpack(f'!{count}i', msg[4:4 + 4 * count]))
print(count, values)

# --- struct + extra bytes (e.g. md5 digest) at the end ---
body = struct.pack('!ii', 1, 2)
packet = body + b"0123456789abcdef"            # 16 extra bytes
body2, tail = packet[:-16], packet[-16:]
print(struct.unpack('!ii', body2), tail)

# --- detect message type by first byte (all messages start with 'c') ---
msg = struct.pack('!ci', b'B', 5)
kind = msg[:1]                                 # b'B'  (msg[0] would be int 66!)
print(kind, msg[0])
