# Building blocks - small, complete, working pairs (one idea per folder)

| folder | what it shows | run |
|---|---|---|
| tcp_basic | one client, text in, struct out | tcp_server.py, tcp_client.py |
| tcp_select_struct | many clients (select), struct('!ci'), shared counter | server_select.py, client_tcp.py 10000 |
| udp_basic | same counter over UDP, timeout | server_udp.py, client_udp.py |
| proxy_tcp_tcp | proxy_spy = forward + log; proxy_tax = CHANGE request and FAKE answer | server: ../tcp_select_struct/server_select.py, client: client_tcp.py 10001 |
| proxy_tcp_udp | TCP client -> proxy -> UDP server | server: ../udp_basic/server_udp.py, client: client_tcp.py 10001 |
| md5_text_udp | "text:md5", rsplit, corrupted message | server.py, client.py |
| udp_file_transfer | file in 200 B chunks, seq numbers, ACK, resend, no duplicates | server.py [drop], client.py photo.jpg |
| select_broadcast_timer | per-client state, send to ALL clients, event after N seconds | server.py 30 |
| struct_binary_files | Assignment II: unpack records from .bin files, pack values | see README inside |

Counter protocol: '!ci'  "+ 10" "- 3" "? 0" -> "O <value>", unknown -> "E 0"
