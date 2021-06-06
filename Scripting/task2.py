#!/usr/bin/env python

import socket
import re
import sys
import time

def Main():
	server_IP = sys.argv[1]
	server_port = 1337
	old_num = 0

	while server_port != 9765:
		try:
			if server_port == 1337:
				print(f"Connecting to {server_IP} waiting for port {server_port} to become alive")

			s = socket.socket()
			s.connect((server_IP,server_port))
			get_req = f"GET / HTTP/1.1\r\nHost: {server_IP}:{server_port}\r\n\r\n"
			s.send(get_req.encode('utf8'))

			while true:
				r = s.recv(1024)
				if (len(r) < 1):
					break
				data = r.decode('utf8')

			op, new_num, next_port = assign_data(data)
			old_num = math_op(op, old_num, new_num)
			print(f"Current number is {old_num} moving to {next_port}")
			server_port = next_port

			s.close()

		except:
			s.close()
			time.sleep(3)
			pass

	print(f"Final answer is {round(old_num,2)}")

def math_op(op, old_num, new_num):
	if op == 'add':
		return old_num + new_num
	if op == 'minus':
		return old_num - new_num
	if op == 'multiply':
		return old_num * new_num	
	if op == 'divide':
		return old_num / new_num
	else:
		return None

def assign_data(data):
	arr = re.split(' |\*|\n', data)
	arr = list(filter(None, arr))
	op = arr[-3]
	new_num = float(arr[-2])
	next_port = int(arr[-1])

	return op, new_num, next_port

if __name__ == '__main__':
	Main()