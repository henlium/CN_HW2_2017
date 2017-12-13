"""
agent module
"""
import socket

SENDER_IP = "127.0.0.1"
SENDER_PORT = 8787
SENDER_RECV_PORT = 8788
SENDER_ADDRESS = (SENDER_IP, SENDER_PORT)
SENDER_RECV_ADDRESS = (SENDER_IP, SENDER_RECV_PORT)

SENDER_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SENDER_SOCK.bind(SENDER_ADDRESS)

while True:
    data, address = SENDER_SOCK.recvfrom(2048)
    if data:
        print "received:", data, "from", SENDER_PORT
