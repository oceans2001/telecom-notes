# JSON: file <-> dict, string <-> dict, sending over the network, append log
# Run: python3 03_json.py
import json

# load / dump  = FILE      loads / dumps = STRING ("s" = string)
data = {"EUR": {"rate": 395.5, "reserve": 100.0}, "list": [1, 2, 3], "ok": True, "none": None}

with open("demo.json", "w") as f:
    json.dump(data, f, indent=2)                      # dict -> file

with open("demo.json") as f:
    loaded = json.load(f)                             # file -> dict
print(loaded["EUR"]["rate"], loaded["list"][0])       # nested access
# JSON true/false/null -> Python True/False/None
# JSON keys are ALWAYS strings: {1: "a"} is saved as {"1": "a"}

# --- iterate nested JSON ---
for code, info in loaded.items():
    if isinstance(info, dict):
        print(code, info["rate"], info.get("reserve", 0))    # .get = default if missing

# --- JSON over a socket (very handy: send any dict/list in one message) ---
msg = json.dumps({"picks": [3, 7], "bet": 100}).encode()     # dict -> str -> bytes
# sock.sendall(msg)
received = json.loads(msg.decode())                          # bytes -> str -> dict
print(received["picks"])
# a list of records works too: json.dumps([{"id": 1}, {"id": 2}])

# --- APPEND to a JSON file (keep old records) - way A: read, add, rewrite ---
def append_json(path, record):
    try:
        with open(path) as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):  # no file yet / empty file
        history = []
    history.append(record)
    with open(path, "w") as f:
        json.dump(history, f, indent=2)

append_json("demo_history.json", {"client": "A", "win": 20})
append_json("demo_history.json", {"client": "B", "win": 0})

# --- way B: JSON Lines (one JSON per line, real "a" append) ---
with open("demo_history.jsonl", "a") as f:
    f.write(json.dumps({"client": "C", "win": 5}) + "\n")
with open("demo_history.jsonl") as f:
    records = [json.loads(line) for line in f if line.strip()]
print(records)

# --- dict with tuple keys can't go to JSON -> convert ---
seats = {("Dune", "17:30"): 5}
json_ready = {f"{t};{s}": v for (t, s), v in seats.items()}
print(json.dumps(json_ready))
