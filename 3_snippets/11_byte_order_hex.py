# BYTE ORDER + HEX + socket utilities
# Run: python3 11_byte_order_hex.py
import struct
import socket

print(hex(8080))                                  # 0x1f90
print(struct.pack('>H', 8080).hex())              # 1f90  big-endian
print(struct.pack('<H', 8080).hex())              # 901f  little-endian
print(struct.pack('!H', 8080).hex())              # 1f90  network = big
print(struct.unpack('>H', struct.pack('<H', 8080))[0])   # wrong order -> 36895
print(socket.htons(8080), socket.ntohs(socket.htons(8080)))
print(int("1f90", 16))                            # hex string -> int
print(bytes.fromhex("1f90"), b"\x1f\x90".hex())

# names / ports
print(socket.gethostbyname("localhost"))
print(socket.getservbyport(80), socket.getservbyport(22))
# socket.gethostbyaddr("8.8.8.8")                 # needs network

# IP as 4 bytes (multicast, raw protocols)
print(socket.inet_aton("192.168.1.1"), socket.inet_ntoa(b"\xc0\xa8\x01\x01"))

# subnets quickly (Kathara / theory)
import ipaddress
net = ipaddress.ip_network("188.100.22.12/20", strict=False)
print(net, net.num_addresses - 2, net.network_address + 1, net.broadcast_address - 1)
print(ipaddress.ip_address("188.100.17.5") in net)
