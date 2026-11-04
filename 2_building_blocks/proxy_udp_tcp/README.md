# UDP client -> proxy -> TCP server (mirror of proxy_tcp_udp)

| TCP -> UDP proxy                         | UDP -> TCP proxy                          |
|------------------------------------------|-------------------------------------------|
| listen_sock: bind + listen               | udp_sock: bind only                       |
| client_conn = accept()                   | none - datagrams from anyone              |
| data = client_conn.recv()                | data, addr = udp_sock.recvfrom()          |
| if not data: break                       | none - UDP clients never "leave"          |
| udp_sock.sendto(data, SERVER_ADDR)       | tcp_sock.sendall(data)                    |
| recvfrom + timeout                       | tcp_sock.recv()                           |
| client_conn.sendall(reply)               | udp_sock.sendto(reply, addr)              |

Run (3 terminals):
    python ../tcp_select_struct/server_select.py
    python proxy_udp_tcp.py
    python client_udp.py 10001        (start 2 at once - shared counter)
