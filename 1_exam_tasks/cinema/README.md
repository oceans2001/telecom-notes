# Cinema (sample exam)  - TCP, text + struct('7s6s'), file, select, stealing proxy
Run order:  server -> proxy -> client
    python server.py screenings.txt
    python proxy.py                         (subtask 4, listens on 10001)
    python client.py Dune 17:30             (direct)
    python client.py Dune 17:30 10001       (through proxy)
Files: server.py (sub 1-3), client.py, proxy.py (sub 4), screenings.txt
