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
TO = float(tmp[4].rstrip())
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

data = F.read(1020)
buf.append(bytes(int_to_bytes(0)) + bytes(data))
ts = []

while True:
    for x in buf:
        SEND_SOCK.sendto(x, SEND_ADDRESS)
        ts.append(int(round(time.time() * 1000)))
    while True:
        ready = select.select([RECV_SOCK], [], [], 0.001)
        if ready[0]:
            data, address = RECV_SOCK.recvfrom(1024)
            ack = int(data[3:])
            print("recv\tack\t", ack)
            if ack >= base:
                for i in range(0, ack - base + 1):
                    buf.pop(0)
                    ts.pop(0)
            # not done
        else:
            if (int(round(time.time() * 1000)) - ts[0]) / 1000 > TO:
                break
