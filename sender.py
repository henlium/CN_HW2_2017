"""
sender module
"""
import select
import socket
import time

def int_to_bytes(value):
    result = []
    for i in range(0, 4):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()
    return result

F = open("SENDER.conf", 'r')
tmp = F.readlines()
RECV_PORT = int(tmp[1].rstrip())
FILENAME = tmp[2].rstrip()
threshold = 16
TO = float(tmp[3].rstrip())
F.close()
F = open("AGENT.conf", 'r')
tmp = F.readlines()
AGENT_IP = tmp[0].rstrip()
SEND_PORT = int(tmp[1].rstrip())
F.close()

SEND_ADDRESS = (AGENT_IP, SEND_PORT)
RECV_ADDRESS = (AGENT_IP, RECV_PORT)

SEND_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RECV_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RECV_SOCK.bind(RECV_ADDRESS)

F = open(FILENAME, 'rb')

# data = []
window_size = 1
buf = []
base = 0
last = 0

buf = []
i = 0
while True:
    data = F.read(1020)
    if data:
        buf.append(bytes(int_to_bytes(i)) + bytes(data))
        i += 1
    else:
        break
Fend = i - 1
print(Fend)
F.close()

SEND_SOCK.sendto(buf[base], SEND_ADDRESS)
print("send\tdata\t", base, "\twinSize = ", window_size)
ts = time.time()
sent = -1

while True:
    # see if ack comes in
    ready = select.select([RECV_SOCK], [], [], 0.001)
    if ready[0]: # ack comes
        data, address = RECV_SOCK.recvfrom(1024)
        ack = int(data[3:])
        print("recv\tack\t", ack)
        if ack >= base and ack <= last: # it's the ack we're looking for
            if ack == Fend:
                break
            # move window
            base = ack + 1
            if window_size < threshold :
                window_size = window_size * 2
            else:
                window_size += 1
            start = last + 1
            for i in range(start, base + window_size):
                if i <= Fend:
                    SEND_SOCK.sendto(buf[i], SEND_ADDRESS)
                    if i <= sent:
                        print("resnd\tdata\t", i, "\twinSize = ", window_size)
                        last = i
                    else:
                        print("send\tdata\t", i, "\twinSize = ", window_size)
                        last = i
                        sent = i
            ts = time.time()
    # if time out
    elif time.time() - ts > TO:
        threshold = max(window_size // 2, 1)
        print("time\tout,\t\tthreshold =", threshold)
        window_size = 1
        SEND_SOCK.sendto(buf[base], SEND_ADDRESS)
        last = base
        print("resnd\tdata\t", base, "\twinSize =", window_size)
        ts = time.time()
ts = time.time()
SEND_SOCK.sendto(bytes("FIN", "ascii"), SEND_ADDRESS)
print("send\tfin")
while True:
    ready = select.select([RECV_SOCK], [], [], 0.001)
    if ready[0]:
        data, address = RECV_SOCK.recvfrom(1024)
        if data == bytes("FINACK", "ascii"):
            print("recv\tfinack")
            break
    else:
        if time.time() - ts > TO:
            SEND_SOCK.sendto(bytes("FIN", "ascii"), SEND_ADDRESS)
            ts = time.time()
            print("resnd\tfin")
