"""
Receiver module
"""
import socket

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

F = open("RECEIVER.conf", 'r')
tmp = F.readlines()
LISTEN_PORT = int(tmp[1].rstrip())
FILENAME = tmp[2].rstrip()
F.close()
F = open("AGENT.conf", 'r')
tmp = F.readlines()
IP = tmp[0].rstrip()
AGENT_PORT = int(tmp[2].rstrip())
F.close()

LISTEN_ADDRESS = (IP, LISTEN_PORT)
AGENT_ADDRESS = (IP, AGENT_PORT)

LISTEN_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
LISTEN_SOCK.bind(LISTEN_ADDRESS)
SEND_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

seq = 0
last_seq = -1

F = open(FILENAME, 'wb')

buffer = []

while True:
    data, address = LISTEN_SOCK.recvfrom(1024)
    if data == bytes("FIN", "ascii"):
        print("recv\tfin")
        SEND_SOCK.sendto(bytes("FINACK", "ascii"), AGENT_ADDRESS)
        print("send\tfinack")
        print("flush")
        for d in buffer:
            F.write(d[4:])
        buffer = []
        break
    elif bytes_to_int(data[0:4]) == seq:
        if len(buffer) >= 32: # buffer overflow
            print("drop\tdata\t", bytes_to_int(data[0:4]))
            ACK = bytes("ACK", "ascii") + bytes(str(last_seq), "ascii")
            SEND_SOCK.sendto(ACK, AGENT_ADDRESS)
            print("send\tack\t", last_seq)
            print("flush")
            for d in buffer:
                F.write(d[4:])
            buffer = []
            continue
        print("recv\tdata\t", seq)
        buffer.append(data)
        ACK = bytes("ACK", "ascii") + bytes(str(seq), "ascii")
        SEND_SOCK.sendto(ACK, AGENT_ADDRESS)
        print("send\tack\t", seq)
        last_seq = seq
        seq += 1
    else:
        print("drop\tdata\t", bytes_to_int(data[0:4]))
        ACK = bytes("ACK", "ascii") + bytes(str(last_seq), "ascii")
        SEND_SOCK.sendto(ACK, AGENT_ADDRESS)
        print("send\tack\t", last_seq)
