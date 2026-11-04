# Lottery - протокол и варианты

Сервер для каждого запроса тянет 5 разных чисел 1..20. Выигрыш = попадания * ставка.

## Формат "text" (Task II a + c: bytes через ':' + MD5)
client -> server : `3,7,12,1,20:100:<md5 всего до последнего ':'>`
server -> client : `5,9,12,3,20:2:200:<md5>`   (выпавшие : попадания : выигрыш)

## Формат "struct" (Task II b + c)
client -> server : `struct('!5ii')` (5 чисел + ставка) + 16 байт `md5.digest()`
server -> client : `struct('!5iii')` (5 выпавших + попадания + выигрыш) + 16 байт digest

## Варианты history (Task V)
- a) `history_proxy.py` - TCP proxy между клиентом и сервером, логирует (только формат text)
- b) сервер сам шлёт каждую игру в `history_server.py` (UDP) - флаг `history` у сервера
- c) клиент после результата шлёт данные в `history_server.py` - флаг `history` у клиента

history protocol (отличается от Task I): UDP, JSON-строка, ответ `b"SAVED"`.

## Запуск
```
python3 history_server.py                                   # для b / c
python3 lottery_server_tcp.py text history                  # TCP, text, вариант b
python3 lottery_server_udp.py struct                        # UDP, struct
python3 lottery_client.py tcp text random
python3 lottery_client.py tcp text stdin
python3 lottery_client.py udp struct json picks.json
python3 lottery_client.py tcp text argv 3 7 12 1 20 100
python3 lottery_client.py tcp text random history           # вариант c

python3 history_proxy.py                                    # вариант a: proxy :10001 -> :10000
python3 lottery_client.py tcp text random port=10001        # через proxy
```
