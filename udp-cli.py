#-*- coding: utf-8 -*- 

import sys
import socket

target_server = ('127.0.0.1', 80)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto("AABBCC", target_server)

data, addr = client.recvfrom(4096)

print data

