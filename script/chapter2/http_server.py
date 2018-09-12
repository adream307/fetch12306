#!/usr/bin/env python
'''
http_server.py
print the input arguments and set cookies
'''
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
import random

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8800


class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print "GET method"
		if self.headers.has_key('Cookie'):
			print "Request Cookies %s" % self.headers['Cookie']
		params=parse_qs(urlparse(self.path).query)
		for (d,x) in params.items():
			print "%s:%s" % (d,x)
		self.send_response(200)
		self.send_header('Content-type','text/html')
		cookie_send='SessionID=%0.17f' % random.random()
		print "Respond Cookies %s" % cookie_send
		self.send_header('Set-Cookie',cookie_send)
		self.end_headers()
		# Send the message to browser
		self.wfile.write("cookies test!")
		return
	def do_POST(self):
		print "POST method"
		if self.headers.has_key('Cookie'):
			print "Request Cookies %s" % self.headers['Cookie']
		params=parse_qs(urlparse(self.path).query)
		for (d,x) in params.items():
			print "%s:%s" % (d,x)
		length = int(self.headers.getheader('content-length'))
		field_data = self.rfile.read(length)
		params=parse_qs(field_data)
		for (d,x) in params.items():
			print "%s:%s" % (d,x)
		self.send_response(200)
		self.send_header('Content-type','text/html')
		cookie_send='SessionID=%0.17f' % random.random()
		print "Respond Cookies %s" % cookie_send
		self.send_header('Set-Cookie',cookie_send)
		self.end_headers()
		# Send the message to browser
		self.wfile.write("cookies test!")
		return


def run_server():
	try:
		server_address=(DEFAULT_HOST, DEFAULT_PORT)
		server= HTTPServer(server_address,RequestHandler)
		print "Custom HTTP server started on port: %s" % DEFAULT_PORT
		server.serve_forever()
	except Exception, err:
		print "Error:%s" %err
	except KeyboardInterrupt:
		print "Server interrupted and is shutting down..."
		server.socket.close()

if __name__ == "__main__":
	run_server()


