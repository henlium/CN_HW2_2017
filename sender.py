"""
sender module
"""

import socket

AGENT_IP = "127.0.0.1"
SEND_PORT = 8787
SEND_ADDRESS = (AGENT_IP, SEND_PORT)
RECV_PORT = 8788
RECV_ADDRESS = (AGENT_IP, RECV_PORT)

SEND_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RECV_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RECV_SOCK.bind(RECV_ADDRESS)

while True:
    msg = raw_input()
    if msg:
        SEND_SOCK.sendto(msg, SEND_ADDRESS)
        print "send:", msg
        while True:
            ack, address = RECV_SOCK.recvfrom(2048)
            if ack:
                print "ACK:", ack
                break