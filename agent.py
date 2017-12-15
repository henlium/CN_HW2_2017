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

cntpkt = 0
cntloss = 0

while True:
    ready = select.select(LISTEN, [], [], 0.01)
    if LS_SOCK in ready[0]:
        data, address = LS_SOCK.recvfrom(2048)
        if data == bytes("FIN", "ascii"):
            print("get\tfin")
            SEND_SOCK.sendto(data, RECVR_ADDRESS)
            print("fwd\tfin")
        else:
            pktnum = bytes_to_int(data[0:4])
            print("get\tdata\t", pktnum)
            dice = random.random()
            if dice >= LossRate:
                cntpkt += 1
                SEND_SOCK.sendto(data, RECVR_ADDRESS)
                print("fwd\tdata\t", pktnum, "\tloss rate =", cntloss / cntpkt)
            else:
                cntpkt += 1
                cntloss += 1
                print("drop\tdata\t", pktnum, "\tloss rate =", cntloss / cntpkt)
    if LR_SOCK in ready[0]:
        data, address = LR_SOCK.recvfrom(2048)
        if data == bytes("FINACK", "ascii"):
            print("get\tfinack")
            SEND_SOCK.sendto(data, SENDER_ADDRESS)
            print("fwd\tfinack")
        else:
            acknum = int(data[3:])
            print("get\tack\t", acknum)
            SEND_SOCK.sendto(data, SENDER_ADDRESS)
            print("fwd\tack\t", acknum)