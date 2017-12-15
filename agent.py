"""
agent module
"""
import random
import select
import socket

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

F = open("SENDER.conf", 'r')
tmp = F.readlines()
SENDER_IP = tmp[0].rstrip()
SENDER_PORT = int(tmp[1].rstrip())
F.close()
F = open("AGENT.conf", 'r')
tmp = F.readlines()
LS_PORT = int(tmp[1].rstrip())
LR_PORT = int(tmp[2].rstrip())
LossRate = float(tmp[3].rstrip())
F.close()
F = open("RECEIVER.conf", 'r')
tmp = F.readlines()
RECVR_IP = tmp[0].rstrip()
RECVR_PORT = int(tmp[1].rstrip())
F.close()

LS_ADDRESS = (SENDER_IP, LS_PORT)
LR_ADDRESS = (RECVR_IP, LR_PORT)
SENDER_ADDRESS = (SENDER_IP, SENDER_PORT)
RECVR_ADDRESS = (RECVR_IP, RECVR_PORT)

LS_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
LS_SOCK.bind(LS_ADDRESS)
LS_SOCK.setblocking(False)
LR_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
LR_SOCK.bind(LR_ADDRESS)
LR_SOCK.setblocking(False)
SEND_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
LISTEN = [LS_SOCK, LR_SOCK]

while True:
    ready = select.select(LISTEN, [], [], 0.01)
    if LS_SOCK in ready[0]:
        data, address = LS_SOCK.recvfrom(2048)
        print("get\tdata\t", bytes_to_int(data[0:4]))
        dice = random.random()
        if dice >= LossRate:
            SEND_SOCK.sendto(data, RECVR_ADDRESS)
        else:
            print("drop")
    if LR_SOCK in ready[0]:
        data, address = LR_SOCK.recvfrom(2048)