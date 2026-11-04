# TEXT PROTOCOLS: build / parse messages with separators
# Run: python3 08_text_protocol.py

# --- list -> "3,7,12" and back ---
nums = [3, 7, 12]
msg = ",".join(str(n) for n in nums)                 # join works only with str!
back = [int(x) for x in msg.split(",")]
print(msg, back)

# --- records with | and fields with ; ---
films = {"Dune": ["Hall 1", "17:30"], "Barbie": ["Hall 2", "20:45"]}
text = "|".join(f"{t};{h};{s}" for t, (h, s) in films.items())
print(text)
for item in text.split("|"):
    t, h, s = item.split(";")
    print(f"  {t}, {h}, {s}")

# --- command + arguments: "BUY Dune 17:30" ---
msg = "BUY Dune 17:30"
cmd, *rest = msg.split()                             # cmd='BUY', rest=['Dune','17:30']
print(cmd, rest)
cmd, arg = "LIST".split(" ", 1) if " " in "LIST" else ("LIST", "")
print(cmd, repr(arg))

# --- key=value pairs: "name=alice;bet=100" ---
pairs = dict(kv.split("=") for kv in "name=alice;bet=100".split(";"))
print(pairs, int(pairs["bet"]))

# --- last field is special (checksum): rsplit ---
body, chk = "a:b:c:9f3e".rsplit(":", 1)
print(body, chk)

# --- validate before unpacking, otherwise ValueError ---
msg = "Dune17:30"
parts = msg.split(";")
if len(parts) != 2:
    print("bad message:", msg)

# --- bytes vs str ---
data = b"LIST"
print(data == b"LIST", data.decode() == "LIST")      # both True
print(data == "LIST")                                # False! bytes != str
