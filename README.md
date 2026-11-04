# FINAL EXAM PACK

1_exam_tasks/       full solutions of exam-like tasks  <- START HERE
2_building_blocks/  small working pieces: TCP, UDP, select, proxies, MD5, file transfer
3_snippets/         tiny runnable examples: input, files, JSON, struct, checksums, random, text, timeout

Lab machines: run with `python` or `py` (not python3). Windows: rename with `move`, not `mv`.

## Which task is closest?
| exam says | open |
|---|---|
| list / buy / borrow / book something, struct answer, file, select | 1_exam_tasks/cinema, library |
| + proxy that steals / changes the answer | cinema/proxy.py, pizzeria/proxy.py |
| proxy changes a TEXT message | pizzeria/proxy.py (menu) |
| text AND struct messages on one connection | exchange/server.py, pizzeria/server.py |
| JSON input file | exchange/server.py |
| stdin / argv input | pizzeria/client.py, exchange/client.py |
| random / stdin / json / argv - "choose one" | lottery/lottery_client.py |
| TCP or UDP version of the same task | lottery/ (both servers, one client) |
| MD5 / CRC beside the message | lottery/, 3_snippets/06_checksums.py |
| log / history / audit server over UDP + JSON append | exchange/audit.py, pizzeria/kitchen.py, lottery/history_server.py |
| history server as a proxy | lottery/history_proxy.py |
| game, game over for everyone, new round | guesser/ |
| proxy TCP -> UDP | 2_building_blocks/proxy_tcp_udp |
| send a file in chunks / ACK | 2_building_blocks/udp_file_transfer |
| notify all clients / timer | 2_building_blocks/select_broadcast_timer |

## Plan in the exam
1. Write down every message: who -> whom, text or struct, exact format, ports.
2. Copy the closest solution, rename, change only data / parsing / logic / answer.
3. print every step. Save a copy after every working subtask (sub1/, sub2/ ...).
4. Subtasks 1-2 first (= pass). Proxy: first forward unchanged, then modify.
5. Start order: end of the chain first (log -> server -> proxy -> client).

## Checklist before submitting
- [ ] struct 's'/'c', sendall, sendto get BYTES (b"...", .encode())
- [ ] after .decode() compare with str; binary message: compare raw bytes BEFORE decode
- [ ] `x.decode()` alone does nothing -> `x = x.decode()`
- [ ] select: inside the client branch always `s` (not conn), ONE recv per event
- [ ] TCP recv/sendall; UDP recvfrom/sendto(data, addr); except (socket.timeout, ConnectionError)
- [ ] bind only where you WAIT (server, proxy listening side); UDP client: no bind
- [ ] int(sys.argv[..]), int()/float() for input(); quantity > 0
- [ ] unpack -> tuple; to CHANGE a dict use d[key][i] -= x
- [ ] shared data and counters created BEFORE the loop; += not =
- [ ] proxy: listen_sock outside the loop and never closed; pack AGAIN after changing
- [ ] build a message in a loop: collect into a list, join + send ONCE after the loop
- [ ] client ALWAYS gets an answer (fail / timeout), otherwise it hangs
- [ ] same struct format on both sides; '!' only if allowed; float -> {x:.2f}
- [ ] no '\x00' or backslash inside {} of an f-string (old Python)
