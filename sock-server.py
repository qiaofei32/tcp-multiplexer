#!/usr/bin/env python
# coding: utf-8
import re
import sys
import socket
import threading

BUFFER_SIZE = 4096
VERBOSE = 3

PROTOCOL = "MySQL"
REMOTE_ADDR, REMOTE_PORT = "localhost", 3306
LOCAL_ADDR, LOCAL_PORT = "0.0.0.0", 9000

log_lock = threading.Lock()
def log(msg, level=1):
	if level >= VERBOSE:
		with log_lock:
			print msg

def socket_proxy(sock_in, sock_out):
	addr_in = '%s:%d' % sock_in.getpeername()
	addr_out = '%s:%d' % sock_out.getpeername()

	while True:
		try:
			data = sock_in.recv(BUFFER_SIZE)
		except Exception, e:
			log('Socket read error of %s: %s' % (addr_in, str(e)), 1)
			break

		if not data:
			log('Socket closed by ' + addr_in)
			break
		try:
			sock_out.sendall(data)
		except Exception, e:
			log('Socket write error of %s: %s' % (addr_out, str(e)), 1)
			break

		log('%s => %s (%d bytes)' % (addr_in, addr_out, len(data)), 1)

	sock_in.close()
	sock_out.close()

def new_clients(sock_in):
	sock_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# upstream_data = sock_in.recv(BUFFER_SIZE)
	# log("%s to %s:%d" % (PROTOCOL, REMOTE_ADDR, REMOTE_PORT), 3)
	#
	# try:
	# 	sock_out.connect((REMOTE_ADDR, REMOTE_PORT))
	# 	sock_out.sendall(upstream_data)
	# except (KeyboardInterrupt, SystemExit):
	# 	sys.exit(1)
	# except socket.error, e:
	# 	sock_out.close()
	# 	log('Remote error: %s' % str(e), 1)
	# 	return
	
	sock_out.connect((REMOTE_ADDR, REMOTE_PORT))
	
	threading.Thread(target=socket_proxy, args=(sock_in, sock_out)).start()
	threading.Thread(target=socket_proxy, args=(sock_out, sock_in)).start()

sock_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_main.bind((LOCAL_ADDR, LOCAL_PORT))
sock_main.listen(10)
log('Listening at %s:%d ...' % (LOCAL_ADDR, LOCAL_PORT), 3)

while True:
	try:
		sock_in, addr_in = sock_main.accept()
	except (KeyboardInterrupt, SystemExit):
		log('Closing...', 1)
		sock_main.close()
		sys.exit(1)

	threading.Thread(target=new_clients, args=(sock_in,)).start()
	log('New clients from %s:%d' % addr_in, 3)
