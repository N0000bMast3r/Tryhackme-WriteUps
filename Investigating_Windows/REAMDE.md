> Investigating Windows

# RDP Credentials : `Administrator`:`letmein123!`

1. Whats the version and year of the windows machine?

```
Windows Server 2016 
```

2. Which user logged in last?

We can use Event Viewer to view the logs.

# Steps

1. Event Viewer -> Windows Logs -> Securtiy
2. For user logon, we have to search for 4624 and 4648 event IDs. For failed logon, we have to search for 4625. For logoff events, we have to search for 4634 and 4647. Let's filter it and we can see that `administrator` is the one!

3. When did John log onto the system last?

net user john | findstr "Last"


```
 03/02/2019 5:48:32 PM
```

4. What IP does the system connect to when it first starts?

Windows registry is a type of database that contains information & settings regarding installed software and hardware of a system. “Registry Editor” is used to view this registry information from your system. HKEY_LOCAL_MACHINE: Contain information about installed hardware, software and their related settings. Looking at `HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run` we can find a registry `UpdateSvc`. 

```
C:\TMP\p.exe -s \\10.34.2.3 'net user' > C:\TMP\o2.txt
```

5. What two accounts had administrative privileges (other than the Administrator user)?

net localgroup Administrators

```
Administrator
Guest
Jenny
```

6. Whats the name of the scheduled task that is malicous.

Let's use Task Scheduler for this one! Clicking `Task Scheduler Library` we can see some Tasks. And we can see a task named `Clean File system` which looks malicious.

7. What file was the task trying to run daily?
```
Triggers: Daily
```

8. What port did this file listen locally for?

```
Actions : C:\TMP\ns.ps1 -l 1348
```

9. When did Jenny last logon? 

```
net user jenny| findstr "Last"
Last logon                   Never
```

10. At what date did the compromise take place?

Looking through Event Viewer we can find that the system has been compromised at `03/02/2019`

11. At what time did Windows first assign special privileges to a new logon?

Inspecting through Event Viewer we got the hit!

```
03/02/2019 4:04:47 PM
```

12. What tool was used to get Windows passwords?

We already viewed the scheduled tasks. And among them there was a task named `GameOver` which used mim.exe which uses the syntax of mimikatz and stores the password in `C:\TMP\o.txt`.

13. What was the attackers external control and command servers IP?

Windows hosts file is used for maps the server or hostname to IP addresses.
In windows the location of the hosts file is C:\Windows\System32\drivers\etc\hosts

```
10.2.2.2        update.microsoft.com
127.0.0.1  www.virustotal.com
127.0.0.1  www.www.com
127.0.0.1  dci.sophosupd.com
10.2.2.2        update.microsoft.com
127.0.0.1  www.virustotal.com
127.0.0.1  www.www.com
127.0.0.1  dci.sophosupd.com
10.2.2.2        update.microsoft.com
127.0.0.1  www.virustotal.com
127.0.0.1  www.www.com
127.0.0.1  dci.sophosupd.com
76.32.97.132 google.com => Answer
76.32.97.132 www.google.com
```

14. What was the extension name of the shell uploaded via the servers website?

Microsoft uses IIS (Internet Informaion Services) as a default web server on the Windows. inetpub is the default folder situated under C:\inetpub. It contains the webserver’s content. wwwroot is a subfolder placed under the inetpub (C:\inetpub\wwwroot) holds all the content like of a webpages.

```
.jsp
```

15. What was the last port the attacker opened?

Windows firewall’s Inbound Rules defend the network against the incoming traffic. It is always helpful to save your system from malware or DDOS related attacks. It also contains the details of the port and address of the local and remote server.

```
1337
```

16. Check for DNS poisoning, what site was targeted?

```
google.com
```