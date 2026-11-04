# TEXT FILES: read config lines, write, append
# Run: python3 02_text_files.py

# create a demo file
with open("demo_items.txt", "w") as f:               # "w" = overwrite
    f.write("Dune;Hall 1;17:30;5\n")
    f.write("Barbie;Hall 1;20:45;0\n")
    f.write("\n")                                      # empty line - must be skipped

# --- read line by line into a dict ---
items = {}
with open("demo_items.txt") as f:
    for line in f:
        line = line.strip()                            # remove '\n' and spaces
        if not line:
            continue
        title, hall, start, seats = line.split(";")
        items[(title, start)] = [hall, int(seats)]     # tuple key, int value
print(items)

# --- skip a header line (CSV-like files) ---
# with open("x.csv") as f:
#     next(f)                                         # skip first line
#     for line in f: ...

# --- whole file at once ---
with open("demo_items.txt") as f:
    lines = [l.strip() for l in f if l.strip()]
print(lines)

# --- append one line (log) ---
with open("demo_log.txt", "a") as f:                  # "a" = append, keeps old content
    f.write("client bought Dune 17:30\n")

# --- write the dict back (e.g. save updated seats) ---
with open("demo_items.txt", "w") as f:
    for (title, start), (hall, seats) in items.items():
        f.write(f"{title};{hall};{start};{seats}\n")
