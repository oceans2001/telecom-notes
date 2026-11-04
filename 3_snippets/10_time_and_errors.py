# TIME + ERROR HANDLING
# Run: python3 10_time_and_errors.py
import time
from datetime import datetime

# --- timestamps ---
start = time.time()                                 # seconds since 1970 (float)
time.sleep(0.2)
print(f"elapsed {time.time() - start:.2f} s")
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # human-readable, good for logs
print(datetime.now().isoformat(timespec="seconds"))

# --- deadline: something happens after N seconds ---
deadline = time.time() + 1.0
while time.time() < deadline:
    time.sleep(0.3)
    print("still open, left:", round(deadline - time.time(), 1))
print("closed")
# in a select server: check time.time() >= deadline at the top of while True
# (select timeout 1 s guarantees the loop runs at least every second)

# --- compare "hh:mm" strings ---
print("17:30" < "20:45")                            # works for zero-padded hh:mm

# --- errors you will meet ---
for raw in ["42", "4.2", "abc"]:
    try:
        print(int(raw))
    except ValueError:
        print("not an int:", raw)

d = {"a": 1}
print(d.get("b", 0))                                # no KeyError
try:
    d["b"]
except KeyError as e:
    print("missing key", e)

try:
    a, b = "x;y;z".split(";")
except ValueError:
    print("wrong number of fields")
