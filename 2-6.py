# -*- coding: utf-8-*-

import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, recieve_first):
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    server.bind((local_host, local_port))
  except:
    print "[!!] Failed to listen on %s:%d" % (local_host, local_port)
    print "[!!] Check for other listening sockets or correct permisstions."
    sys.exit(0)

  print "[*] Listening on %s:%d" % (local_host, local_port)
  server.listen(5)
  while True:
    client_socket, addr = server.accept()
    print "[==>] Recieved incoming connection from %s:%d" % (addr[0],addr[1])
    proxy_thread = threading.Thread(
           target=proxy_handler,
           args=(client_socket, remote_host, remote_port, recieve_first))
    proxy_thread.start()


def main():
  if len(sys.argv[1:]) != 5:
    print "Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [recieve_first]"
    print "print Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
    sys.exit(0)

  local_host = sys.argv[1]
  local_port = sys.argv[2]
  remote_host = sys.argv[3]
  remote_port = sys.argv[4]
  recieve_first = sys.argv[5]

  if "True" in recieve_first:
    receieve_first = True
  else:
    receieve_first = False

  server_loop(local_host, local_port, remote_host, remote_port, recieve_first)


def proxy_handler(local_host, local_port, remote_host, remote_port, recieve_first):
  remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  remote_socket.connetct(( remote_host, remote_port))

  if recieve_first:
    remote_buffer = recieve_from(remote_socket)
    hexdump(remote_buffer)
    remote_buffrer = response_handler(remote_buffer)

    if len(remote_buffer):
      print "[<==] Sending %d bytes to localhost." % len(remote_buffer)
      client_socket.send(remote_buffer)

  while True:
    local_buffer = recieve_from(client_socket)

    if len(local_buffer):
      print "[==>] Recieved %d bytes from localhost." % len(local_buffer)
      hexdump(local_buffer)

      local_buffer = request_handler(local_buffer)
      remote_socket.send(local_buffer)
      print "[==>] Sent to remote."

    remote_buffer = recieve_from(remote_socket)

    if len(remote_biffer):
      print "[<==] Recieved %d bytes from remote." % len(remote_buffer)
      hexdump(remote_buffer)
      remote_buffer = response_handler(remote_buffer)
      client_socket.send(remote_buiffer)
      print "[<==] Sent to localhost"

    if not len(local_buffer) or not len(remote_buffer):
      client_socket.close()
      remote_socket.close()
      print "[*] No more data. Closing connections."

      break

main()
