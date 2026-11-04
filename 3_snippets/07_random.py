# RANDOM: numbers, ids, probability, choice
# Run: python3 07_random.py
import random
import string

print(random.randint(1, 20))                         # one int, both ends included
print(random.sample(range(1, 21), 5))                # 5 DIFFERENT numbers (lottery)
print(random.choices(range(1, 7), k=3))              # 3 with repeats (dice)
print(random.choice(["rock", "paper", "scissors"]))  # one element
print(random.uniform(1.0, 2.0))                      # random float
print(round(random.uniform(1.0, 2.0), 2))

ticket = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
print(ticket)                                        # 'K7Q2XA'

if random.random() < 0.5:                            # 50 % chance (0.2 = 20 %)
    print("steal")

items = [1, 2, 3, 4]
random.shuffle(items)                                # in place
print(items)

# random pause 1-3 s (makes clients interleave)
import time
# time.sleep(random.randint(1, 3))
# time.sleep(random.uniform(0.5, 1.5))
