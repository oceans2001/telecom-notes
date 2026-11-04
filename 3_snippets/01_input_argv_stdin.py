# INPUT: command line + keyboard
# Run: python3 01_input_argv_stdin.py localhost 10000 3 7 12
import sys

print("all argv:", sys.argv)                 # ['01_...py', 'localhost', '10000', '3', '7', '12']

# --- argv with defaults (program works even without arguments) ---
host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 10000    # str -> int!
numbers = [int(x) for x in sys.argv[3:]]                    # rest as int list
print(host, port, numbers)

# --- strict argv check with usage message ---
if len(sys.argv) < 3:
    print(f"usage: python3 {sys.argv[0]} <host> <port> [numbers...]")
    # sys.exit(1)                              # 1 = error exit code

# --- stdin (keyboard) ---
# input() ALWAYS returns str
# name  = input("Name: ").strip()
# money = float(input("Amount: "))                          # ValueError if not a number
# nums  = [int(x) for x in input("Numbers: ").split()]     # "3 7 12" -> [3, 7, 12]
# code  = input("Currency: ").strip().upper()              # " eur" -> "EUR"

# --- safe number input: ask again until valid ---
def ask_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("not a number, try again")
# bet = ask_int("Bet: ")
