# Currency Exchange  - TCP, text + struct('3sf'/'?f'), JSON input, select, stdin, UDP audit + MD5 + JSON append
Run order:  audit -> server -> client
    python audit.py
    python server.py rates.json
    python client.py                        (asks currency + HUF on keyboard)
Key idea: text and struct messages on one connection -> decide on RAW bytes (data == b"RATES") before decode.
