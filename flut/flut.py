import socket
import random

conn = None
print('connecting...')
while True:
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(0.25)
        conn.connect(('151.217.40.82', 1234))
        break
    except Exception as error:
        conn.close()
        print('timeout?', error)
print('connected.')
conn.setblocking(False)

print('loop....')
rand = random.Random()
while True:
    x = rand.randint(0, 199)
    y = rand.randint(0, 199)
    command = 'PX {' + str(x) + '} {' + str(y) + '} {FFFFFF}\n'
    # print('command', command)
    data = command.encode('utf-8')
    # print(data)
    try:
        conn.sendall(data)
    except BlockingIOError:
        pass
    # print('recv...')
    data = None
    try:
        data = conn.recv(4096)
    except BlockingIOError:
        pass
    if data is not None and len(data) > 0:
        print('data len:', len(data))
        # print('data:', data.decode('utf-8'))


# how to flut
#
# Connect via TCP to this address/port and use the following commandz:
# send pixel: 'PX {x} {y} {GG or RRGGBB or RRGGBBAA as HEX}\n'
# set offset for future pixels: 'OFFSET {x} {y}\n'
# request pixel: 'PX {x} {y}\n'
# request resolution: 'SIZE\n'
# request client connection count: 'CONNECTIONS\n'
# request this help message: 'HELP\n'
