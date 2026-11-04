import sys 
import struct

parameter1 = struct.Struct('9s i f')
parameter2 = struct.Struct('f ? c')
parameter3 = struct.Struct('c i 9s')
parameter4 = struct.Struct('f 9s ?')

with open(sys.argv[1], "rb") as f:
    print(parameter1.unpack(f.read(parameter1.size)))

with open(sys.argv[2], "rb") as f:
    print(parameter2.unpack(f.read(parameter2.size)))

with open(sys.argv[3], "rb") as f:
    print(parameter3.unpack(f.read(parameter3.size)))

with open(sys.argv[4], "rb") as f:
    print(parameter4.unpack(f.read(parameter4.size)))

p1 = struct.Struct('16s i ?')
print(p1.pack(b"elso", 84, True))

p2 = struct.Struct('f ? c')
print(p2.pack(87.5, False, b'X'))

p3 = struct.Struct('i 14s f')
print(p3.pack(75, b"masodik", 94.9))

p4 = struct.Struct('c i 17s')
print(p4.pack(b'Z', 106, b"harmadik"))

