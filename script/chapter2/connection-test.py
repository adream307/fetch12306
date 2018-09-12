#!/usr/bin/env python
import socket
import errno
import sys
import time

HOST='www.163.com'
PORT=80
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
s.setblocking(0)
s.sendall('GET / HTTP/1.1\r\n')
s.sendall('Host: '+ HOST +'\r\n')
s.sendall('User-Agent: Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0\r\n')
s.sendall('Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n')
s.sendall('Accept-Language: en-US,en;q=0.5\r\n')
s.sendall('Accept-Encoding: gzip,deflat\r\n')
#s.sendall('Connection: close\r\n')
s.sendall('Connection: keep-alive\r\n')
s.sendall('\r\n')
length=0
previous=0
while True:
	try:
		msg=s.recv(1024)
		if msg.__len__()==0: break
		length = length+msg.__len__()
		print 'read %d bytes' % length
	except socket.error, e:
		err = e.args[0]
		if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
			if length==previous: 
				sys.stdout.write('#')
				sys.stdout.flush()
			previous=length
			time.sleep(1)
			continue
		else: sys.exit(1)
print 'press Enter to return'
sys.stdin.readline()
s.close()
