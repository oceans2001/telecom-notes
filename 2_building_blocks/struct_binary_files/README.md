# Assignment II - struct + binary files

```
python3 protkollInputGenerator.py 9sif   && mv database.bin db1.bin
python3 protkollInputGenerator.py 'f?c'  && mv database.bin db2.bin
python3 protkollInputGenerator.py ci9s   && mv database.bin db3.bin
python3 protkollInputGenerator.py 'f9s?' && mv database.bin db4.bin
python3 client.py db1.bin db2.bin db3.bin db4.bin
```
Task1: unpack the first record of each file. Task2: pack given values and print bytes.
Formats WITHOUT '!' (native alignment, same as the generator): '9s i f' is 9 + 3 pad + 4 + 4 = 20 bytes.
