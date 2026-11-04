# Pizzeria  - EVERYTHING: TCP, text + struct, file, select, argv/stdin, UDP kitchen + MD5 + JSON, modifying proxy
Run order:  kitchen -> server -> proxy -> client
    python kitchen.py
    python server.py menu.txt
    python proxy.py                         (coupon proxy on 10001)
    python client.py Pepperoni 2            (direct)
    python client.py Pepperoni 2 10001      (through proxy)
    python client.py                        (keyboard input)
Proxy modifies a TEXT message (menu) and a STRUCT message (total).
